#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 8/31/16
"""

from twisted.web import server
from twisted.internet import reactor

from customise_resource import CustomiseFile

if __name__ == '__main__':
    resource = CustomiseFile('/tmp/')
    site = server.Site(resource)
    reactor.listenTCP(8080, site)
    reactor.run()
