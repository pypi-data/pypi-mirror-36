#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

from otcclient.core.OtcConfig import OtcConfig
from otcclient.core.otcpluginbase import otcpluginbase
from otcclient.utils import utils_output
import sys

class table(otcpluginbase):

    def otctype(self):
        return "utils_output"

    @staticmethod
    def print_output(respjson, **kwargs):
        mainkey = kwargs.get('mainkey', None)
        subkey= kwargs.get('subkey', None)
        listkey = kwargs.get('listkey', None)

        if (sys.version_info > (3, 0)):
            if isinstance(respjson, (bytes, str)):
                if len(respjson.strip()) == 0:
                    return
        else:
            if isinstance(respjson, str):
                if len(respjson.strip()) == 0:
                    return


        if mainkey is None and listkey is None:
            print (respjson)
            raise Exception("Output error!")
        if not (OtcConfig.QUERY is None):
            utils_output.handleQuery(respjson, OtcConfig.QUERY)
        elif subkey is None and listkey is None:
            utils_output.printJsonTableTransverse(respjson, "table", mainkey)
        elif subkey is None:
            utils_output.printLevel2(respjson, "table", mainkey, listkey)
        else:
            utils_output.printLevel2(respjson, "table", mainkey, listkey,subkey=subkey)
