#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 9/1/16
"""
import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Put the html template, css files, js files under this path.
STATIC_RESOURCE_PATH = os.path.join(_CURRENT_DIR, 'static')

# The template file used to render, should be under STATIC_RESOURCE_PATH.
TEMPLATE_FILE = 'index.html'
