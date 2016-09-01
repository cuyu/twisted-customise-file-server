#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 9/1/16
"""
import os

from twisted.web import server
from twisted.internet import reactor

from customise_resource import CustomiseFile

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_STATIC_DIR = os.path.join(_CURRENT_DIR, 'static')


class CustomiseServer(object):
    def __init__(self, static_resource_path=_DEFAULT_STATIC_DIR):
        """
        :param static_resource_path: The dir that you put the css and js files. Should be full path.
        """
        self.static_resource_path = static_resource_path

    def run(self, static_file_path, template_file='index.html', port=8080):
        """
        :param static_file_path: The dir you want to display all the files in it on the web page.
        :param port: Web server port.
        """
        resource = CustomiseFile(static_file_path, renderTemplate=template_file,
                                 staticResourcePath=self.static_resource_path)
        resource.putChild(self.static_resource_path.split(os.sep)[-1], CustomiseFile(self.static_resource_path))
        site = server.Site(resource)
        reactor.listenTCP(port, site)
        reactor.run()
