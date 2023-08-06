#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems xxxxxxx


from otcclient.core.OtcConfig import OtcConfig 
from otcclient.utils import utils_http

from otcclient.core.otcpluginbase import otcpluginbase
from otcclient.core.pluginmanager import getplugin
from otcclient.core.argmanager import arg, otcfunc 

class dms(otcpluginbase):
    ar = {}    
    
    @staticmethod
    def otcOutputHandler(): 
        return getplugin(OtcConfig.OUTPUT_FORMAT)
 
    def otctype(self):
        return "func" 


    @staticmethod
    @otcfunc(plugin_name=__name__,
            desc="Description of all the queues",
            examples=[
                       {"List queues":"otc dms describe_queues"}                       
                       ],
            args = [ ]
             )    
    def describe_queues():
        url = "https://" + OtcConfig.DEFAULT_HOST + "/v1.0/" + OtcConfig.PROJECT_ID +  "/queues"    
        ret = utils_http.get(url)
        print (url)
        print (ret)        
        
        return ret


