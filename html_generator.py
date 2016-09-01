#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 9/1/16
"""
from jinja2 import Environment, FileSystemLoader

from settings import STATIC_RESOURCE_PATH, TEMPLATE_FILE


class HtmlGenerator(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(STATIC_RESOURCE_PATH))

    def generatePage(self, variables):
        """
        Generate the real html contents according the given html file and give the variables.
        :param variables: A dict contains variables corresponding to the given html file.
        :return: A unicode string of rendered html content.
        """
        template = self.env.get_template(TEMPLATE_FILE)
        return template.render(**variables)
