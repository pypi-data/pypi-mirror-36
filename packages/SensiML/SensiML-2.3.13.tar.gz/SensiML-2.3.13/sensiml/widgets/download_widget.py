##################################################################################
#  SENSIML CONFIDENTIAL                                                          #
#                                                                                #
#  Copyright (c) 2017-18  SensiML Corporation.                                   #
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
import IPython
from pandas import DataFrame
from ipywidgets import widgets
from ipywidgets import Layout, Button,VBox, HBox, Box, FloatText, Textarea, Dropdown, Label, IntSlider, Checkbox, Text, Button, SelectMultiple
from IPython.display import display
from ipywidgets import IntText
from json import dumps as jdump
from sensiml.widgets.base_widget import BaseWidget


category_item_layout = Layout(
    #display='flex',
    size=16,
    #border='solid 2px',
    justify_content='flex-start',
    #background_color= 'red',
    overflow='visible'
)



def clean_name(name):
    return ''.join(e if e.isalnum() else '_' for e in name)

class DownloadWidget(BaseWidget):
    def __init__(self, dsk=None, level='Project', folder='knowledgepacks'):
        self._dsk = dsk
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.setup(level=level)

    def setup(self, level):
        self.kb_description = {'parent':{},
                  'sub':{'Report':'Report'}}

        self.kb_dict = {'parent':[],
                        'sub':[]}
        self.level = level



    def select_platform(self, b):
        platform = self._dsk.platforms.get_platform_by_id(self._widget_platform.value)

        if 'curie' in platform.description.lower():
            self._widget_target_os.options=['ISPC']
            self._widget_target_os.value=self._widget_target_os.options[0]
            self._widget_app_options.options=['BLE', 'LED', 'Serial']
        elif 'nordic' in platform.description.lower():
            self._widget_target_os.options=['NordicSDK']
            self._widget_target_os.value=self._widget_target_os.options[0]
            self._widget_app_options.options=['BLE', 'LED', 'Serial']
            self._widget_app_options.value=['BLE']
        elif 'simulator' in platform.description.lower():
            self._widget_target_os.options=['x86']
            self._widget_target_os.value=self._widget_target_os.options[0]
            self._widget_app_options.options=['Serial']
        elif 'quick ai' in platform.description.lower():
            self._widget_target_os.options=['FreeRTOS']
            self._widget_target_os.value=self._widget_target_os.options[0]
            self._widget_app_options.options=['Serial','BLE']

        if not platform.can_build_binary:
            self._widget_target_os.options=['None']
            self._widget_download_type.value='Library'



    def generate_description(self, b):
        parent_name = None
        parent_uuid = None
        description = {}
        self.set_parent_model(None)
        if not self.kb_description['parent']:
            print("No Parent Model Selected.")
            return
        for key in self.kb_description['parent']:
            description = {clean_name(key):{'uuid':self.kb_description['parent'][key],
                                            'results':{},
                                            'source':self._widget_source.value}}
            parent_name = clean_name(key)
            parent_uuid = self.kb_description['parent'][key]
        for parent in self.kb_dict['parent'][0][1:]:
            description[parent_name]['results'].update(
                    {format(parent.description.split('-')[0]): clean_name(parent.value)})
        for key in self.kb_description['sub']:
            if key != 'Report':
                sub_description = {'uuid':self.kb_description['sub'][key],
                                  'parent':parent_name,
                                  'segmenter_from':'parent',}
                description.update({clean_name(key):sub_description})
        board_name = self._dsk.platforms.get_platform_by_id(self._widget_platform.value).board_name

        kp_uuid = parent_uuid
        kp_platform = self._widget_platform.value
        kp_debug = self._widget_debug.value
        kp_test_data = self._widget_test_data.value
        kp_download_type = self._widget_download_type.value
        sample_rate = self._widget_source_rate.value if self._widget_source_rate.value in [200,100,50,25] else 100
        output_options= [x.lower() for x in self._widget_app_options.value]

        if kp_platform == 3 and kp_platform < 99: #Nordic Thingy and not simulator
            if 'ble' not in output_options:
                output_options.insert('ble') # always output via ble
            kp_application = 'thingy_pme'
        elif kp_platform == 4:
            if 'ble' not in output_options:
                output_options.insert('ble') # always output via ble
            kp_application = 'ble_app_sensiml_freertos'
        else:
            if 'led' in output_options:
                kp_application = 'led'
            else:
                kp_application = 'Default'

        if board_name == 'ARM GCC Generic' or board_name == 'x86 GCC Generic':
            kp_application = 'testdata_runner'

        if kp_uuid is not None:
            kp = self._dsk.get_knowledgepack(kp_uuid)
        else:
            return None

        config = {'target_platform':kp_platform,
                  'test_data':kp_test_data,
                  'debug': kp_debug,
                  'application': kp_application,
                  'sample_rate': sample_rate,
                  'output_options': output_options,
                  'kb_description': description}
        print(config)

        if kp_download_type == 'Library':
            kp.download_library(config=config, folder='knowledgepacks')
        if kp_download_type == 'Binary':
            kp.download_binary(config=config, folder='knowledgepacks')

    def set_parent_model(self, b):

        if self._widget_parent_select.value is None:
            return

        kp = self._dsk.get_knowledgepack(self._widget_parent_select.value)
        kp_item = []
        kp_item.append(Label(value=kp.name))

        for key, value in kp.class_map.items():
            kp_item.append(Dropdown(options=self.kb_description['sub'],
                                    description='{} - {}'.format(key, value)))

        self.kb_description['parent'] = {kp.name:kp.uuid}
        self.kb_dict['parent'] = [kp_item]
        self.update_models()

    def get_kp_dict(self):
        if self.level.lower() == 'project':
            kps = self._dsk.project.list_knowledgepacks()
        elif self.level.lower() == 'pipeline':
            kps = self._dsk.pipeline.list_knowledgepacks()
        else:
            kps = self._dsk.list_knowledgepacks()

        if isinstance(kps, DataFrame) and len(kps):
            kps = sorted([(name, value) for name, value in kps[['Name', 'kp_uuid']].values if name], key=lambda s: s[0].lower())

            return kps

        return [('', None)]

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    def get_model_list(self):
        return [Label(value='Parent Model')] + self.flatten(self.kb_dict['parent']) + \
        [Label(value='Sub Model')] + self.flatten(self.kb_dict['sub'])

    def get_feature_file_list(self):
        ff = self._dsk.list_featurefiles(silent=True)
        if ff is not None:
            return list(ff['Name'].values)
        else:
            return []

    def get_platform_names(self):
        pf = {}
        for platform in self._dsk.platforms.platform_list:
            pf['{} {}'.format(platform.platform, platform.platform_version)] =  platform.id

        return pf

    def _refresh(self):
        if self._dsk is None:
            return
        self._widget_platform.options = self.get_platform_names()
        self._widget_platform.value = 10
        self._widget_platform.observe(self.select_platform)
        self.select_platform(None)
        self._widget_test_data.options = [None] + self.get_feature_file_list()
        self._widget_parent_select.options = self.get_kp_dict()
        self._widget_parent_select.value = self._widget_parent_select.options[0][1]
        self._widget_class_map.options = self._get_class_map()

    def _clear(self):
        self._widget_parent_select.options = ['']
        self._widget_parent_select.value = ''
        self._widget_class_map.options = []

    def _update_class_map(self, *args):
         self._widget_class_map.options = self._get_class_map()

    def _get_class_map(self):

        if self._widget_parent_select.value:
            class_map = self._dsk.get_knowledgepack(self._widget_parent_select.value).class_map
            return sorted(['{} - {}'.format(key, value) for key, value in class_map.items()])
        else:
            return ''

    def _refresh_models_list(self, b):
        if self._dsk:
            if self._dsk.pipeline:
                self._widget_parent_select.options=self.get_kp_dict()
                self._widget_parent_select.value= self._widget_parent_select.options[0][1]
                self._widget_class_map.options = self._get_class_map()

    def update_models(self):
        if self._dsk is None:
            return

        if self.kb_dict['parent']:
            for output in self.kb_dict['parent'][0][1:]:
                output.options=[k for k,v in self.kb_description['sub'].items()]

    def _change_rate(self, change):
        if self._widget_source.value == 'Motion':
            self._widget_source_rate.options = [200, 100, 50, 25]
            self._widget_source_rate.value = 100

        if self._widget_source.value == 'Audio':
            self._widget_source_rate.options = [8000]
            self._widget_source_rate.value = 8000

        if self._widget_source.value == 'Custom':
            self._widget_source_rate.options = ['']
            self._widget_source_rate.value = None


    def create_widget(self):

        self._button_generate = Button(icon='download',  tooltip='Generate and Download', layout=Layout(width='15%'))
        self._button_refresh = Button(icon='refresh', layout=Layout(width='15%'), tooltip='Refresh Model List')
        self._widget_platform = Dropdown(description="HW Platform", options = [])
        self._widget_target_os = Dropdown(description="Target OS")
        self._widget_app_options = SelectMultiple(description="Output", options=['BLE','LED','Serial'])
        self._widget_download_type = Dropdown(description="Format", options=['Binary', 'Library'])
        self._widget_source = Dropdown(description="Source", options=['Motion', 'Audio', 'Custom'])
        self._widget_source_rate = Dropdown(description="Sample Rate", value=100, options=[200, 100, 50, 25])
        self._widget_debug = Dropdown(description="Debug", options=[True, False])
        self._widget_test_data = Dropdown(description="Test Data", options=[None])
        self._widget_parent_select = Dropdown(description="Model Name", options = [], layout=Layout(width='85%'))
        self._widget_class_map = SelectMultiple(description="Class Map", options=[''])

        self.kb_items = VBox([
            HBox([self._widget_parent_select, self._button_refresh,


                  self._button_generate,

                  ]),
            self._widget_source,
            self._widget_class_map,
            Label(value='Device Settings', layout=category_item_layout),
            HBox([VBox([self._widget_platform,
            self._widget_target_os,
            self._widget_download_type,
            ]),
            VBox(
            [self._widget_source_rate,
            self._widget_debug,
            self._widget_test_data]),
            self._widget_app_options,
            ]),
            ])


        self._button_generate.on_click(self.generate_description)
        self._button_refresh.on_click(self._refresh_models_list)
        self._widget_source.observe(self._change_rate, names='value')
        self._widget_parent_select.observe(self._update_class_map)

        self._refresh()

        return self.kb_items

