##################################################################################
#  SENSIML CONFIDENTIAL                                                          #
#                                                                                #
#  Copyright (c) 2017  SensiML Corporation.                                      #
#                                                                                #
#  The source code contained or  described  herein and all documents related     #
#  to the  source  code ("Material")  are  owned by SensiML Corporation or its   #
#  suppliers or licensors. Title to the Material remains with SensiML Corpora-   #
#  tion  or  its  suppliers  and  licensors. The Material may contain trade      #
#  secrets and proprietary and confidential information of SensiML Corporation   #
#  and its suppliers and licensors, and is protected by worldwide copyright      #
#  and trade secret laws and treaty provisions. No part of the Material may      #
#  be used,  copied,  reproduced,  modified,  published,  uploaded,  posted,     #
#  transmitted, distributed,  or disclosed in any way without SensiML's prior    #
#  express written permission.                                                   #
#                                                                                #
#  No license under any patent, copyright,trade secret or other intellectual     #
#  property  right  is  granted  to  or  conferred upon you by disclosure or     #
#  delivery of the Materials, either expressly, by implication,  inducement,     #
#  estoppel or otherwise.Any license under such intellectual property rights     #
#  must be express and approved by SensiML in writing.                           #
#                                                                                #
#  Unless otherwise agreed by SensiML in writing, you may not remove or alter    #
#  this notice or any other notice embedded in Materials by SensiML or SensiML's #
#  suppliers or licensors in any way.                                            #
#                                                                                #
##################################################################################


import logging
import os
import re
from tempfile import NamedTemporaryFile
from appdirs import user_config_dir
import json
from qgrid import show_grid

import numpy as np
import pandas as pd
from pandas import DataFrame

from sensiml.datamanager import Functions, PlatformDescriptions, PipelineSeeds, \
    Projects, Segmenters
from sensiml.datamanager.knowledgepack import get_knowledgepack, get_knowledgepacks
from sensiml.datasets import DataSets
from sensiml.connection import Connection
from sensiml.base.exceptions import *
from sensiml.pipeline import Pipeline
from sensiml.base.snippets import Snippets, function_help
from sensiml.datamanager.captures import CaptureExistsError


config_dir = user_config_dir(__name__.split('.')[0], False)

logger = logging.getLogger('KB')


def print_list(func):
    """ This is a wrapper for printing out lists of objects stored in KB Cloud """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if len(result.keys()) == 0 and kwargs.get('silent', False)==False:
            print("No {} stored on KB Cloud for this project.".format(
                func.__name__.split('_')[1]))
            return None
        if kwargs.get('get_objects', False) is True:
            return result
        return DataFrame(list(result.keys()), columns=['Name'])

    return wrapper


class SensiML(object):
    """Entrance to SensiML Analytic Suite"""

    def __init__(self, server="https://sensiml.cloud/",
                    path='connect.cfg', **kwargs):
        self._project = None
        self._pipeline = None
        self._knowledgepack_list = None
        auth_url=server+"oauth/"

        self._connection = Connection(server=server, auth_url=auth_url, path=path, **kwargs)
        self.projects = Projects(self._connection)
        self.datasets = DataSets()
        self.functions = Functions(self._connection)
        self.platforms = PlatformDescriptions(self._connection)
        self.seeds = PipelineSeeds(self._connection)
        self.snippets = Snippets(self.list_functions(
            kp_functions=False, qgrid=False), self.functions.function_list, self.seeds)
        self._feature_files = None

    @property
    def knowledgepack_list(self):
        if self._knowledgepack_list is None:
            self.knowledgepack_list = get_knowledgepacks(self._connection)

        return self._knowledgepack_list

    @knowledgepack_list.setter
    def knowledgepack_list(self, value):
        if value is None:
            self._knowledgepack_list = None
        else:
            self._knowledgepack_list = value.rename(columns={'name':'Name',
                                    'project_name':'Project',
                                    'sandbox_name':'Pipeline',
                                    'uuid':'kp_uuid'})

    def logout(self, name=None):
        """Logs out of the current connection."""
        if name is None:
            name = self._connection.server_name

        Connection.logout(name)

    def get_function(self, name):
        """Gets a function method call"""
        return self.functions.function_list[name]

    def function_description(self, name):
        """Gets a description of a pipeline function."""
        print(self.functions.create_function_call(name).__doc__)

    def function_help(self, name):
        """Prints a shortened description of a function. """
        print(function_help(self.functions.function_list[name]))

    def list_functions(self, functype=None, subtype=None, kp_functions=False, qgrid=True):
        """Lists all of the functions available on kb cloud

        Returns:
            Dataframe

        Args:
            functype (str, None): Return only functions with the specified type. ie. "Segmenter"
            subtype (str, None): Return only functions with the specified subtype. ie. "Sensor"
            kp_functions (boolean, True): Return only functions that run on tbe loaded to a device.
            Excludes functions such as feature selection and model training.
        """
        df =  DataFrame([{'NAME': f.name, 'TYPE': f.type, "DESCRIPTION": f.description.lstrip('\n').lstrip(' '), "SUBTYPE": f.subtype, "KP FUNCTION": f.has_c_version} for f in self.functions.get_functions()]).\
            sort_values(by=['TYPE', 'SUBTYPE']).reset_index(drop=True)[
            ['NAME', 'TYPE', 'SUBTYPE', 'DESCRIPTION', 'KP FUNCTION']]

        if functype:
            df = df[df['TYPE'] == functype]

        if subtype:
            df = df[df['SUBTYPE'] == subtype]

        if kp_functions:
            df = df[df['KP FUNCTION'] == True][
                ['NAME', 'TYPE', 'SUBTYPE', 'DESCRIPTION']]

        if qgrid:
            return show_grid(df.reset_index(drop=True))
        else:
            return df.reset_index(drop=True)


    def delete_project(self):
        """Deletes a project """
        if self._project is not None:
            self._project.delete()

    def list_projects(self):
        """Lists all of the projects on kb cloud

        Returns:
            DataFrame: projects on kb cloud
        """
        projects = self.projects.get_projects()

        return DataFrame({
            'Name': [p.name for p in projects],
        })

    def list_segmenters(self):
        if self._project is None:
            print("project must be set to list segmenters.")
            return None

        segmenters = Segmenters(self._connection, self._project).get_segmenters()
        if not len(segmenters):
            print("No segmenters stored on the cloud.")
            return None
        return DataFrame(segmenters)[['name', 'id', 'custom','parent']]

    def list_seeds(self):
        """Lists all of the pipeline seeds on kb cloud

        Returns:
            DataFrame: pipeline seeds on kb cloud
        """
        return DataFrame({
            'Name': [s.name for s in self.seeds],
            'Description': [s.description for s in self.seeds],
        })

    def list_knowledgepacks(self, unnamed=False):
        """Lists all of the knowledgepacks associated with a team

        Returns:
            DataFrame: knowledgepacks on kb cloud
        """
        if self.knowledgepack_list is None:
            print("No Knowledgepacks stored for this team on the cloud.")
            return None

        if unnamed:
            return self.knowledgepack_list[['Name','Project','Pipeline','kp_uuid']]

        return self.knowledgepack_list[self.knowledgepack_list['Name']!=''][['Name','Project','Pipeline','kp_uuid']]

    def get_knowledgepack(self, uuid):
        """retrieve knowledgepack by uuid from the server associated with current project

        Args:
            uuid (str): unique identifier for knowledgepack

        Returns:
            TYPE: a knowledgepack object
        """

        return get_knowledgepack(uuid, self._connection)


    @property
    def project(self):
        """The active project"""
        return self._project

    @print_list
    def list_featurefiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._feature_files.build_featurefile_list()

    @print_list
    def list_datafiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._feature_files.build_featurefile_list()

    @print_list
    def list_captures(self, get_objects=False):
        """List all captures for the active project

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._captures.build_capture_list()

    @print_list
    def list_sandboxes(self, get_objects=False):
        """List all sandboxes for the active project.

        Args:
            get_objects (bool, False): Also return the sandbox objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._sandboxes.build_sandbox_list()

    @print_list
    def list_queries(self, get_objects=False):
        """List all queries for the active project.

        Args:
            get_objects (bool, False): Also return the query objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._queries.build_query_list()

    @project.setter
    def project(self, name):
        self._project = self.projects.get_or_create_project(name)

    @property
    def pipeline(self):
        """The active pipeline"""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, name):
        if self._project is None:
            raise Exception(
                'Project must be set before a pipeline can be created')

        self._pipeline = Pipeline(self, name=name)




    def create_query(self, name, columns=[], metadata_columns=[], metadata_filter='', segmenter=None, label_column='', combine_labels=None, force=False):
        """Create a query to use as input data in a pipeline.

        Args:
            name (str): Name of the query.
            columns (list, optional): Columns to add to the query result.
            metadata_columns (list, optional): Metadata to add to the query result.
            metadata_filter (str, optional): Filter to apply to the query.
            segmenter (int, optional): Segmenter to filter query by.
            force (bool, False): If True overwrite the query on kb cloud.

        Returns:
            object: Returns a query object that was created.
        """
        query = self.project.queries.get_query_by_name(name)
        new = False
        if query is not None and not force:
            raise QueryExistsException(
                'Query already exists. Set force=True to overwrite.')
        elif query is not None and force:
            query.columns.clear()
            query.metadata_columns.clear()
            query.metadata_filter = ''
            query.label_column = ''
        else:
            query = self.project.queries.new_query()
            query.name = name
            new = True


        for col in columns:
            logger.debug('query_column:' + str(col))
            query.columns.add(col)

        for col in metadata_columns:
            logger.debug('query_metadata_column:' + str(col))
            query.metadata_columns.add(col)

        if metadata_filter:
            logger.debug('query_metadata_filter:' + str(metadata_filter))
            query.metadata_filter = metadata_filter

        if label_column:
            query.label_column = label_column

        if combine_labels:
            query.combine_labels = combine_labels

        query.segmenter = segmenter

        if new:
            query.insert()
        else:
            query.update()

        return query

    def get_query(self, name):
        if self.project is None:
            print("Project must be set first")
            return

        return self.project.queries.get_query_by_name(name)

    def upload_data_file(self, name, path, force=False):
        """Upload data source from local CSV file"""
        logger.debug('set_feature_file:' + name + ':' + path)
        print('Uploading file "{}" to KB Cloud.'.format(name))
        if name[-4:] != '.csv':
            name = "{}.csv".format(name)

        feature_file = self._project._feature_files.get_featurefile_by_name(name)
        if feature_file is None:
            new = True
            feature_file = self._project.featurefiles.new_featurefile()
        else:
            new = False
            if not force:
                raise FeatureFileExistsException()

        feature_file.filename = name
        feature_file.path = path
        if new:
            feature_file.insert()
        else:
            feature_file.update()

        print('Upload of file "{}"  to KB Cloud completed.'.format(name))

        return self

    def upload_dataframe(self, name, dataframe, force=False):
        """Set data source from a pandas DataFrame."""
        logger.debug('set_data:' + name)

        with NamedTemporaryFile(delete=False) as temp:
            dataframe.to_csv(temp.name, index=False)
            logger.debug('set_dataframe:' + name + ':' + temp.name)
            self.upload_data_file(name, temp.name, force=force)

        os.remove(temp.name)

        return self

    def clear_session_cache(self):
        for _, _, filenames in os.walk(config_dir):
            for filename in filenames:
                if re.match(r'_token.json$', filename):
                    os.unlink(filename)


    def upload_project(self, name, dclprojpath):
        if name in self.list_projects()['Name'].values:
            print("Project with this name already exists.")
            return

        self.project = name
        capture_metadata = None
        basedir = os.path.dirname(dclprojpath)
        segment_map = {}

        with open(dclprojpath, 'r') as f:
            dclproj = json.load(f)

        plugin_config = dclproj.get('ProjectCapturePluginConfig', None)
        if plugin_config is not None:
            self.project.plugin_config = plugin_config
            print('Capture Config Found, Updating...')
            self.project.update()

        for segmenter in dclproj.get('ProjectSegmenters'):

            if segmenter.get('parameters', None):
                params = json.loads(segmenter.get('parameters'))
                call = self.functions.create_function_call(params['name'])
                for k, v in params['inputs'].items(): setattr(call, k, v)
            else:
                call=None

            new_segmenter = self.project.add_segmenter(segmenter.get('name'),
                                    call,
                                    preprocess=segmenter.get('preprocess'),
                                    custom=segmenter.get('custom'))

            segment_map[segmenter['name']]=new_segmenter['id']
            segment_map[segmenter['id']]=new_segmenter['id']


        for capture in dclproj.get('CaptureFiles'):
            print("Uploading Capture data, metadata and lables for {}".format(capture))
            try:

                capture_metadata ={}
                file_metadata = []
                if os.path.exists(os.path.join(basedir, 'metadata', os.path.basename(capture)[:-3]+'dcl')):
                    with open(os.path.join(basedir, 'metadata', os.path.basename(capture)[:-3]+'dcl'), 'r') as f:
                        capture_metadata = json.load(f)
                        file_metadata = capture_metadata.pop('FileMetadata')

                capture_obj = self.project.captures.create_capture(os.path.basename(capture),
                                                    os.path.join(basedir, capture),
                                                    capture_info=capture_metadata
                                                    )
                for metadata in file_metadata:
                    metadata_obj = capture_obj.metadataset.new_metadata()
                    metadata_obj.sample_start = metadata['capture_sample_sequence_start']
                    metadata_obj.sample_end =  metadata['capture_sample_sequence_end']
                    metadata_obj.value =  metadata['value']
                    metadata_obj.name =  metadata['name']
                    metadata_obj.segmenter = segment_map.get(metadata['segmenter'], None)
                    metadata_obj.insert()

                for segment_dir in os.listdir(os.path.join(basedir,'segments')):
                    if not os.path.exists(os.path.join(basedir, 'segments',
                                                    segment_dir, os.path.basename(capture)[:-3]+'sdcl')):
                        continue

                    with open(os.path.join(basedir,'segments', segment_dir, os.path.basename(capture)[:-3]+'sdcl'), 'r') as f:
                        segment_labels = json.load(f).pop('DetectedSegments')

                    for segment in segment_labels:
                        for metadata in segment['LabelData']:
                            metadata_obj = capture_obj.metadataset.new_metadata()
                            metadata_obj.sample_start = metadata['capture_sample_sequence_start']
                            metadata_obj.sample_end =  metadata['capture_sample_sequence_end']
                            metadata_obj.value =  metadata['value']
                            metadata_obj.name =  metadata['name']
                            metadata_obj.segmenter = segment_map[metadata['segmenter']]
                            metadata_obj.insert()

            except CaptureExistsError:
                print("{} already uploaded to this project.".format(capture))
