#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 8/31/16
"""

from costomise_file_server.customise_server import CustomiseServer

if __name__ == '__main__':
    server = CustomiseServer('/tmp')
    server.run()
