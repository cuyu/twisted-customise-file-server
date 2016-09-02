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
from settings import STATIC_RESOURCE_PATH


class CustomiseServer(object):
    def __init__(self, static_file_path, port=8080):
        """
        :param static_file_path: The dir you want to display all the files in it on the web page.
        :param port: Web server port.
        """
        self.static_file_path = static_file_path
        self.port = port

    def run(self):
        resource = CustomiseFile(self.static_file_path)
        resource.putChild(STATIC_RESOURCE_PATH.split(os.sep)[-1], CustomiseFile(STATIC_RESOURCE_PATH))
        site = server.Site(resource)
        reactor.listenTCP(self.port, site)
        reactor.run()
