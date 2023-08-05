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
#  estoppel or otherwise.Any license under such intellectual property righprintts#
#  must be express and approved by SensiML in writing.                           #
#                                                                                #
#  Unless otherwise agreed by SensiML in writing, you may not remove or alter    #
#  this notice or any other notice embedded in Materials by SensiML or SensiML's #
#  suppliers or licensors in any way.                                            #
#                                                                                #
##################################################################################


import json
import os
import sys
import re
from uuid import UUID


from pandas import DataFrame
from numpy import int64
import urllib
import logging
from time import sleep
import warnings

import sensiml.base.utility as utility
from sensiml.datamanager.confusion_matrix import ConfusionMatrix, ConfusionMatrixException
from sensiml.datamanager.deviceconfig import DeviceConfig
from sensiml.datamanager.platformdescription import PlatformDescription
from sensiml.method_calls.functioncall import FunctionCall


logger = logging.getLogger(__name__)

class KnowledgePackException(Exception):
    """Base exception for KnowledgePacks"""

class KnowledgePack(object):
    """Base class for a KnowledgePack"""

    def __init__(self, connection, project_uuid, sandbox_uuid):
        """Initializes a KnowledgePack instance

        Args:
            project (Project): the parent project of the KnowledgePack
            sandbox (Sandbox): the parent sandbox of the KnowledgePack
        """
        self._uuid = ''
        self._connection = connection
        self._project_uuid = project_uuid
        self._sandbox_uuid = sandbox_uuid
        self._project_name = ''
        self._sandbox_name = ''
        self._configuration_index = ''
        self._name = ''
        self._model_index = ''
        self._execution_time = ''
        self._neuron_array = ''
        self._model_results = ''
        self._pipeline_summary = ''
        self._query_summary = ''
        self._feature_summary = ''
        self._device_configuration = ''
        self._transform_summary = ''
        self._knowledgepack_summary = ''
        self._sensor_summary = ''
        self._cost_summary = ''
        self._class_map = ''
        self._device_config = DeviceConfig()

    @property
    def uuid(self):
        return self._uuid

    @property
    def sandbox_uuid(self):
        return self._sandbox_uuid

    @property
    def project_uuid(self):
        return self._project_uuid
    @property
    def sandbox_name(self):
        return self._sandbox_name

    @property
    def project_name(self):
        return self._project_name

    @property
    def name(self):
        return self._name

    @property
    def execution_time(self):
        return self._execution_time

    @property
    def neuron_array(self):
        """The model's neuron array"""
        return self._neuron_array

    @property
    def model_results(self):
        """The model results associated with the KnowledgePack (in JSON form)"""
        return self._model_results

    @property
    def pipeline_summary(self):
        """A summary specification of the pipeline which created the KnowledgePack"""
        return self._pipeline_summary

    @property
    def query_summary(self):
        """A summary specification of the query used by the pipeline which created the KnowledgePack"""
        return self._query_summary

    @property
    def feature_summary(self):
        """A summary of the features generated by the KnowledgePack"""
        return self._feature_summary

    @property
    def configuration_index(self):
        return self._configuration_index

    @property
    def model_index(self):
        return self._model_index

    @property
    def device_configuration(self):
        return self._device_configuration

    @property
    def transform_summary(self):
        """A summary of transform parameters used by the KnowledgePack"""
        return self._transform_summary

    @property
    def sensor_summary(self):
        """A summary of sensor streams usd by the KnowledgePack"""
        return self._sensor_summary

    @property
    def class_map(self):
        """A summary of the integer classes/categories used by the KnowledgePack and the corresponding application
        categories"""
        return self._class_map

    @property
    def reverse_class_map(self):
        """A summary of the category/integer class used by the KnowledgePack and the corresponding application
        categories"""
        if self._class_map:
            return {v:k for k,v in self._class_map.items()}
        return {}

    @property
    def cost_dict(self):
        """A summary of device costs incurred by the KnowledgePack"""
        return self._cost_summary

    @property
    def knowledgepack_summary(self):
        """A summary of device costs incurred by the KnowledgePack"""
        return self._knowledgepack_summary

    @property
    def cost_report(self):
        """A print(ed tabular report of the device cost incurred by the KnowledgePack"""
        print(self.get_report('cost'))

    def get_report(self, report_type):
        """Sends a request for a report to the server and returns the result.

        Args:
            report_type (string): string name of report, ex: 'cost'

        Returns:
            (string): string representation of desired report

        """
        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/report/{3}/'.format(self._project_uuid, self._sandbox_uuid, self.uuid, report_type)
        response = self._connection.request('get', url, headers={'Accept':'text/plain'})
        return response.text

    def get_sketch(self):
        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/sketch/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)

        response = self._connection.request('get', url,)
        response_data, err = utility.check_server_response(response)
        if err is False:
            return response_data

    def recognize_features(self, data):
        """Sends a single vector of features to the KnowledgePack for recognition.

        Args:
            data (dict): dictionary containing

              - a feature vector in the format 'Vector': [126, 32, 0, ...]
              - 'DesiredResponses' indicating the number of neuron responses to return

        Returns:
            (dict): dictionary containing

            - CategoryVector (list): numerical categories of the neurons that fired
            - MappedCategoryVector (list): original class categories of the neurons that fired
            - NIDVector (list): ID numbers of the neurons that fired
            - DistanceVector (list): distances of the feature vector to each neuron that fired

        """
        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/recognize_features/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)
        response = self._connection.request('post', url, data)
        response_data, err = utility.check_server_response(response)
        if err is False:
            return response_data

    def recognize_signal(self, dataframe=None, capture=None, featurefile=None, datafile=None, stop_step=False,
                                segmenter=True, platform='kbengine', get_result=True,
                                kb_description=None):
        """Sends a DataFrame of raw signals to be run through the feature generation pipeline and recognized.

        Args:
            dataframe (DataFrame): contains sensor axes required for feature generation and, optionally, metadata and
              labels (depricated)
            capture (str): Filename of a capture file to use in the recognition
            featurefile (str): Filename of a feature file to use in the recognition
            stop_step (int): for debugging, if you want to stop the pipeline at a particular step, set stop_step
              to its index
            segmenter (bool or FunctionCall): to suppress or override the segmentation algorithm in the original
              pipeline, set this to False or a function call of type 'segmenter' (defaults to True)

        Returns:
            (dict): dictionary of results and summary statistics from the executed pipeline and recognition
        """
        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/recognize_signal/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)


        if dataframe is not None:
            msg = "\nWARNING: Passing input data as a dataframe to recognize_signal is no longer supprted.\n\n"+\
            "Recommend practice to upload a dataframe is\n\n\t\tdsk.upload_dataframe('file_name.csv', df)\n\n"+\
            "To use the uploaded dataframe in your pipeline\n\n\t\trecognize_signal(datafile='datafile_name.csv')"

            print(msg)
            return

        if capture:
            data_for_recognition = {'capture':capture}
        elif featurefile:
            data_for_recognition = {'featurefile':featurefile}
        elif datafile:
            data_for_recognition = {'featurefile':datafile}
        else:
            print("You must select a capture, featurefile  or datafile to run recognition against.")
            return None
        data_for_recognition['stop_step'] = stop_step
        data_for_recognition['platform'] = platform
        data_for_recognition['kb_description'] = json.dumps(kb_description)
        if isinstance(segmenter, bool):
            data_for_recognition['segmenter'] = segmenter
        elif isinstance(segmenter, FunctionCall):
            data_for_recognition['segmenter'] = segmenter._to_dict()
        else:
            raise KnowledgePackException("Segmenter input requires a valid segmentation call object or None.")

        try:
            response = self._connection.request('post', url, data_for_recognition)
            response_data, err = utility.check_server_response(response)
            if err is False:
                if get_result:
                    results = utility.wait_for_pipeline_result(self, lock=True, silent=True)
                    print("Results retrieved.")
                    return results[0], results[1]
                else:
                    return response_data['data']
        except MemoryError:
            warnings.warn('ERROR: Your system has run out of RAM while performing this operation. Try freeing up some RAM or using less data before attempting this again.')
            return None

    def stop_recognize_signal(self):
        """Sends a kill signal to a pipeline
        """

        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/recognize_signal/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)
        response = self._connection.request('DELETE', url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            return None

    def _handle_result(self, response_data):
        def fix_index(df):
            """Converts a string index to an int for a DataFrame"""
            df.index = df.index.astype(int64)
            return df.sort_index()

        def parse_classification_results(df_result):
            """Parses the results returned by knowledgepack recognize_signal into a DataFrame when a classification has
            occurred."""

            df_result.index.name = None
            ordered_columns = ['DistanceVector', 'NIDVector', 'CategoryVector', 'MappedCategoryVector'] + \
                              [i for i in df_result.columns if i not in ['DistanceVector', 'NIDVector', 'CategoryVector',
                                                                         'MappedCategoryVector']]
            df_result = df_result[[col for col in ordered_columns if col in df_result.columns]]

            return df_result

        summary = {}
        for key in response_data:
            if key not in ['results']:
             summary[key] = DataFrame(response_data[key])

        # Check for a unicode string which can be returned sometimes
        if isinstance(response_data['results'], str):
           return fix_index(DataFrame(json.loads(response_data['results']))), summary

        # Check for the results vector and parse appropriately
        if isinstance(response_data['results'], dict) and response_data['results'].get('vectors', None):
            df_result = parse_classification_results(DataFrame(response_data['results']['vectors']))
        else:
            df_result = fix_index(DataFrame(response_data['results']))

        # If there was labeled data we will have a confusion matrix as well
        if 'metrics' in response_data['results']:
            summary['confusion_matrix'] = ConfusionMatrix(response_data['results']['metrics'])

        return df_result, summary


    def retrieve(self, silent=False):
        """Gets the result of a prior asynchronous execution of the sandbox.

            Returns:
                (DataFrame or ModelResultSet): result of executed pipeline, specified by the sandbox
                (dict): execution summary including execution time and whether cache was used for each
                step; also contains a feature cost table if applicable
        """

        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/recognize_signal/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)
        response = self._connection.request('get', url)
        response, err = utility.check_server_response(response)
        if err is False:
            response_data = response.get('data', {})
            return utility.check_pipeline_status(response_data, self._handle_result, silent=silent)

    def save(self, name):
        """Save a knowledpack with a name.

            Returns:
                (DataFrame or ModelResultSet): result of executed pipeline, specified by the sandbox
                (dict): execution summary including execution time and whether cache was used for each
                step; also contains a feature cost table if applicable
        """

        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/'.format(
            self._project_uuid, self._sandbox_uuid, self.uuid)
        data = {'name':name}
        response = self._connection.request('put', url, data)
        response, err = utility.check_server_response(response)
        if err is False:
            self._name = name
            print("Knowledgepack name updated.")


    def download_library(self, folder='', run_async=True, platform=None, *args, **kwargs):
        """Calls the server to generate static library image based on device config.

        Args:
            folder (str): Folder to save to if not generating a link

        Returns:
            str: Denoting success, or link to file download
        """
        return self._download(folder=folder, bin_or_lib='lib', run_async=run_async,
                            platform=platform, *args, **kwargs)

    def download_binary(self, folder='', run_async=True, platform=None, *args, **kwargs):
        """Calls the server to generate full binary image based on device config.

        Args:
            folder (str): Folder to save to if not generating a link

        Returns:
            str: Denoting success, or link to file download
        """
        return self._download(folder=folder, bin_or_lib='bin', run_async=run_async,
                            platform=platform, *args, **kwargs)

    def get_sandbox_device_config(self):
        url = 'project/{0}/sandbox/{1}/device_config/'.format(
                self._project_uuid, self._sandbox_uuid)
        response = self._connection.request('get', url)
        response_data, err = utility.check_server_response(response, is_octet=True)
        if err is False:
            return response_data.json().get('device_config')

    def _download(self, folder, bin_or_lib, run_async=False, platform=None, *args, **kwargs):
        _path = r'{0}'.format(folder)
        url = 'project/{0}/sandbox/{1}/knowledgepack/{2}/generate_{3}/'.format(
                self._project_uuid, self._sandbox_uuid, self.uuid, bin_or_lib)
        #config = self._sandbox.device_config.copy() # get a regular dictionary

        if platform is not None and type(platform) is PlatformDescription:
            kwargs['config']={ 'target_platform' : platform.id}
        elif platform is not None and type(platform) is not PlatformDescription:
            print("Platform not properly specified. Specify via dsk.platforms()")
            return None

        config = kwargs.pop('config', None)
        if config:
            if 'kb_description' in config and isinstance(config['kb_description'], dict):
                config['kb_description'] = json.dumps(config['kb_description'])
            for key in kwargs:
                if key in ['debug', 'test_data', 'application','sample_rate', 'output_options']:
                    config.update({key:kwargs[key]})
                if key == 'kb_description':
                      config.update({key:json.dumps(kwargs[key])})
        else:
            config = self.get_sandbox_device_config()

        bin_lib = 'Binary' if bin_or_lib == 'bin' else 'Library'
        print("Building Binary with configuration")
        for key in config:
            print("{} : {}".format(key, config[key]))

        if config.get('target_platform', None) is None:
            raise KnowledgePackException("Target platform must be specified.")
        config['async'] = run_async
        response = self._connection.request( 'post', url,  data=config)
        response_data, err = utility.check_server_response(response, is_octet=True)
        if err:
            print('Error')
        if run_async:
            while True:
                response = self._connection.request('get',url)
                response_data, err = utility.check_server_response(response, is_octet=True)
                if (err or
                    'content-disposition' in response_data.headers or
                    response_data.json().get('task_state') in ('FAILURE',)):
                    break
                sys.stdout.write('.')
                sleep(5)
            if 'content-disposition' in response_data.headers:
                if kwargs.get('save_as'):
                    filename = kwargs.get('save_as', None)
                else:
                    filename = re.findall('filename="([^"]+)"', response_data.headers['content-disposition'])[0]
                if filename is None:
                    filename = re.findall('filename="([^"]+)"', response_data.headers['content-disposition'])[0]
                file_path = os.path.join(_path, filename)
                with open(file_path, 'wb') as f:
                    for d in response_data.iter_content(2048):
                        f.write(d)
                print('KnowledgePack saved to {0}'.format(file_path))
            else:
                print(response_data.json().get('task_result'))
        else:
            if 'filename' not in response_data.headers.keys():
                raise KnowledgePackException(response_data.json().get('detail'))

            if err is False:
                full_path = os.path.join(_path, response_data.headers['filename'])
                with open(full_path, 'wb') as f:
                    for d in response_data.iter_content(2048):
                        f.write(d)
                print('KnowledgePack saved to {0}'.format(full_path))
            else:
                raise KnowledgePackException(response_data.json().get('detail'))

    def initialize_from_dict(self, init_dict):
        self._uuid = init_dict['uuid']
        self._name = init_dict['name']
        self._configuration_index = init_dict['configuration_index']
        self._model_index = init_dict['model_index']
        self._execution_time = init_dict['execution_time']
        try:
            self._model_results = json.loads(init_dict['model_results'])
            self._device_configuration = json.loads(init_dict['device_configuration'])
            self._class_map = json.loads(init_dict['class_map'])
            self._cost_summary = json.loads(init_dict['cost_summary'])
            self._pipeline_summary = json.loads(init_dict['pipeline_summary'])
            self._query_summary = json.loads(init_dict['query_summary'])
            self._feature_summary = json.loads(init_dict['feature_summary'])
            self._transform_summary = json.loads(init_dict['transform_summary'])
            self._sensor_summary = json.loads(init_dict['sensor_summary'])
            self._neuron_array = json.loads(init_dict['neuron_array'])
            self._project_name = json.loads(init_dict['project_name'])
            self._sandbox_name = json.loads(init_dict['sandbox_name'])
            self._knowledgepack_summary = json.loads(init_dict.get('knowledgepack_summary', ''))
        except:
            self._model_results = init_dict['model_results']
            self._device_configuration = init_dict['device_configuration']
            self._class_map = init_dict['class_map']
            self._cost_summary = init_dict['cost_summary']
            self._pipeline_summary = init_dict['pipeline_summary']
            self._query_summary = init_dict['query_summary']
            self._feature_summary = init_dict['feature_summary']
            self._transform_summary = init_dict['transform_summary']
            self._sensor_summary = init_dict['sensor_summary']
            self._neuron_array = init_dict['neuron_array']
            self._project_name = init_dict['project_name']
            self._sandbox_name = init_dict['sandbox_name']
            self._knowledgepack_summary = init_dict.get('knowledgepack_summary', None)

def get_knowledgepack(kp_uuid, connection):
    """Gets a KnowledgePack by uuid.

        Returns:
            a KnowledgePack instance, list of instances, or None
    """
    url = 'knowledgepack/{0}/'.format(kp_uuid)
    response = connection.request('get', url,)
    response_data, err = utility.check_server_response(response)
    if err is False:
        kp = KnowledgePack(connection, response_data.get('project_uuid'), response_data.get('sandbox_uuid'))
        kp.initialize_from_dict(response_data)
        return kp

def get_knowledgepacks(connection):
    """Gets the KnowledgePack(s) created by the sandbox.

        Returns:
            a KnowledgePack instance, list of instances, or None
    """
    url = 'knowledgepack/'
    response = connection.request('get', url,)
    response_data, err = utility.check_server_response(response)
    if err is False:
        return DataFrame(response_data)


#def activate_knowledgepack(connection, activation_key):
#    """Posts activation_key from device to get activation code.
#        Inputs: Activation Key, read from device (16 characters)
#        Returns: Activation Code, to write to device (64 Characters)
#    """
#    if type(activation_key) is not str or len(activation_key) is not 16:
#        raise KnowledgePackException("Activation Keys must be 16 character strings!")
#    url = 'activate-knowledgepack/'
#    data = {}
#    data['key'] = activation_key
#    response = connection.request('post', url, data )
#    response_data, err = utility.check_server_response(response)
#    if err is False:
#        return str(response_data['code'])


