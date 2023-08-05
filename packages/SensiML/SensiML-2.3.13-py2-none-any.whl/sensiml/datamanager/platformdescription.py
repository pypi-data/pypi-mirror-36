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


import os
import json
from pandas import DataFrame, Series

from sensiml.base import utility



class PlatformDescription(object):
    """Base class for a transform object"""
    _id = 0
    _board = {'board:name': '', 'hw_accel': False}
    _can_build_binary = False
    _platform = ''
    _platform_version = ''
    _description = ''
    _ota_capable = False

    def __init__(self, connection):
        self._connection = connection

    @property
    def board_name(self):
        return self._board['board_name']

    @property
    def id(self):
        return self._id

    @property
    def hw_accel(self):
        return self._board['hw_accel']

    @property
    def can_build_binary(self):
        return self._can_build_binary

    @property
    def platform(self):
        return self._platform

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def platform_version(self):
        return self._platform_version

    @property
    def ota_capable(self):
        return self._ota_capable

    def refresh(self):
        """Calls the REST API and populates the local object properties from the server."""
        url = 'platform/{0}/'.format(self.id)
        response = self._connection.request('get', url,)
        response_data, err = utility.check_server_response(response)
        if err is False:
            self._board = response_data['board']
            self._platform = response_data['platform']
            self._platform_version = response_data['platform_version']
            self._description = response_data['description']
            self._can_build_binary = response_data['can_build_binary']
            self._ota_capable = response_data['ota_capable']

    def initialize_from_dict(self, input_dictionary):
        """Populates a single transform object from a dictionary of properties from the server.

            Args:
                input_dictionary (dict): containing uuid, type, subtype, name, function_in_file, description,
                input_contract, and subtype
        """
        self._id = input_dictionary['id']
        self._board = input_dictionary['board']
        self._platform = input_dictionary['platform']
        self._platform_version = input_dictionary[u'platform_version']
        self._description = input_dictionary['description']
        self._can_build_binary = input_dictionary['can_build_binary']
        self._ota_capable = input_dictionary.get('ota_capable', False)

    def __dict__(self):
        ret = {
            'Id': int(self.id),
            'Board': self.board_name,
            'Hardware Accelerated': 'Yes' if self.hw_accel else 'No',
            'Software Platform': self.platform,
            'Platform Version': self.platform_version,
            'Description': self.description
        }
        return ret

    def __call__(self):
        pd_dict = self.__dict__()
        pseries = Series(pd_dict, index=pd_dict.keys())
        df = DataFrame()
        df = df.append(pseries, ignore_index=True)
        return df.drop(labels=['Id'], axis=1)
