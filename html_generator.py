#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 9/1/16
"""
from jinja2 import Template, Environment, FileSystemLoader


# def urlFor(filepath):


class HtmlGenerator(object):
    def __init__(self, static_folder_path):
        self.env = Environment(loader=FileSystemLoader(static_folder_path))

    def generatePage(self, html_file_path, variables):
        """
        Generate the real html contents according the given html file and give the variables.
        :param html_file_path: The relative file path according to the static_folder_path.
        :param variables: A dict contains variables corresponding to the given html file.
        :return: A unicode string of rendered html content.
        """
        template = self.env.get_template(html_file_path)
        return template.render(**variables)


if __name__ == '__main__':
    t = Template('Hello {{name}}')
    t.render(name='John')
    pass
