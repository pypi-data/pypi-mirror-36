
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *

import uuid

from ..basestore import *
from ..identifiers.datacatalog_uuid import text_uuid_to_binary

from .utils import components_to_pipeline, pipeline_to_uuid
from .token import new_token, generate_salt, validate_token, InvalidToken
class PipelineCreateFailure(CatalogUpdateFailure):
    pass

class DuplicatePipelineError(CatalogUpdateFailure):
    pass

class PipelineUpdateFailure(CatalogUpdateFailure):
    pass

class PipelineStore(BaseStore):
    """Create and manage pipeline records"""
    def __init__(self, mongodb, config={}, session=None):
        super(PipelineStore, self).__init__(mongodb, config, session)
        coll = self.collections.get('pipelines')
        if self.debug:
            coll = '_'.join([coll, str(time_stamp(rounded=True))])
        self.name = coll
        self.coll = self.db[coll]
        self._post_init()
        self.CREATE_OPTIONAL_KEYS = (
            'accepts', 'produces', 'name', 'description', 'collections_levels', 'processing_levels')

    def update_properties(self, dbrec):
        ts = current_time()
        properties = dbrec.get('properties', {})
        properties['created_date'] = properties.get('created_date', ts)
        if properties.get('modified_date', ts) >= ts:
            properties['modified_date'] = ts
        properties['revision'] = properties.get('revision', 0) + 1
        dbrec['properties'] = data_merge(dbrec['properties'], properties)
        return dbrec

    def create(self, components, **kwargs):
        DEFAULTS = {'accepts': [],
                    'produces': [],
                    'collections_levels': 'measurement',
                    'processing_levels': '1'}
        pipe_rec = data_merge(DEFAULTS, kwargs)
        ts = current_time()
        doc = components_to_pipeline(components)
        doc_uuid = pipeline_to_uuid(doc)
        _doc_uuid = pipeline_to_uuid(doc, binary=False)
        pipe_rec['uuid'] = doc_uuid
        pipe_rec['components'] = doc
        pipe_rec['properties'] = {'created_date': ts,
                                  'modified_date': ts,
                                  'revision': 0}
        pipe_rec['_visible'] = True
        pipe_rec['_uuid'] = _doc_uuid
        pipe_rec['_salt'] = generate_salt()

        try:
            result = self.coll.insert_one(pipe_rec)
            result_job = self.coll.find_one({'_id': result.inserted_id})
            result_job['token'] = new_token(result_job)

            # TODO factor this out into a general filter function
            try:
                result_job('_salt')
            except Exception:
                pass

            return result_job
        except DuplicateKeyError:
            raise DuplicatePipelineError('A pipeline with this distinct set of components already exists.')
        except Exception as exc:
            raise PipelineUpdateFailure(
                'Failed to create pipeline record', exc)

    def update(self, pipeline_uuid, token, components=None, input_types=None, output_types=None, data_processing_level=None, data_collection_level=None, name=None, description=None):
        ts = current_time()
        if components is not None:
            # TODO: Transparently hand off to create_pipeline
            raise PipelineUpdateFailure('Cannot update the list of components in a pipeline')
        if isinstance(pipeline_uuid, str):
            pipeline_uuid = text_uuid_to_binary(pipeline_uuid)

        # fetch current record
        pipe_rec = self.coll.find_one({'uuid': pipeline_uuid})
        if pipe_rec is None:
            raise PipelineUpdateFailure('No pipeline with UUID {}'.format(pipeline_uuid))

        # token is pipeline-specific
        try:
            validate_token(token, pipeline_uuid=pipe_rec['_uuid'],
            salt=pipe_rec['_salt'], permissive=False)
        except InvalidToken as exc:
            raise PipelineUpdateFailure(exc)

        new_pipe_rec = {'uuid': pipeline_uuid,
                        'accepts': input_types,
                        'produces': output_types,
                        'levels': {'collections': [data_collection_level],
                                   'processing': str(data_processing_level)},
                        'name': name,
                        'description': description}
        pipe_rec, jdiff = data_merge_diff(pipe_rec, new_pipe_rec)
        self.log(pipeline_uuid, jdiff)
        pipe_rec = self.update_properties(pipe_rec)
        try:
            updated_rec = self.coll.find_one_and_replace({'_id': pipe_rec['_id']}, pipe_rec, return_document=ReturnDocument.AFTER)

            # TODO factor this out into a general filter function
            try:
                updated_rec('_salt')
            except Exception:
                pass

            return updated_rec
        except Exception as exc:
            raise PipelineUpdateFailure(
                'Failed to update pipeline {}'.format(pipeline_uuid), exc)

    def delete(self, uuid, token, force=False):
        """Delete a pipeline by UUID
        By default the record is marked as invisible. If force==True, the
        actual record is deleted (but this is bad for provenance)."""
        if isinstance(uuid, str):
            uuid = text_uuid_to_binary(uuid)

        # fetch current record
        pipe_rec = self.coll.find_one({'uuid': uuid})
        if pipe_rec is None:
            raise PipelineUpdateFailure(
                'No pipeline with UUID {}'.format(uuid))

        # token is pipeline-specific
        try:
            validate_token(token, pipeline_uuid=pipe_rec['_uuid'],
            salt=pipe_rec['_salt'], permissive=False)
        except InvalidToken as exc:
            raise PipelineUpdateFailure(exc)

        if force:
            try:
                return self.coll.remove({'uuid': uuid})
            except Exception as exc:
                raise PipelineUpdateFailure(
                    'Failed to delete pipeline {}'.format(uuid), exc)

