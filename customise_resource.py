#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 8/31/16
"""
import itertools
import os
from datetime import datetime
from twisted.python import filepath
from twisted.web import resource
from twisted.web.static import File, getTypeAndEncoding, formatFileSize
from twisted.python.compat import escape, _PY3, nativeString

from html_generator import HtmlGenerator

if _PY3:
    from urllib.parse import quote, unquote
else:
    from urllib import quote, unquote


class CustomiseFile(File):
    def __init__(self, path, defaultType="text/html", ignoredExts=(), registry=None, allowExt=0,
                 renderTemplate=None, staticResourcePath=None):
        """
        :param staticResourcePath: The resource folder path. Only needed for the web page nodes.
                                    For resource nodes should be None.
        :param renderTemplate: The html template file path. Should be a relative path to the staticResourcePath.
                                    For resource nodes this can be None.
        """
        super(CustomiseFile, self).__init__(path, defaultType, ignoredExts, registry, allowExt)
        if staticResourcePath is None:
            assert renderTemplate is None
        self.renderTemplate = renderTemplate
        self.staticResourcePath = staticResourcePath

    def directoryListing(self):
        if self.staticResourcePath:
            return CustomiseDirectoryLister(self.path,
                                            self.renderTemplate,
                                            self.staticResourcePath,
                                            self.listNames(),
                                            self.contentTypes,
                                            self.contentEncodings,
                                            self.defaultType)


class CustomiseDirectoryLister(resource.Resource):
    """
    Print the content of a directory.

    @ivar template: page template used to render the content of the directory.
        It must contain the format keys B{header} and B{tableContent}.
    @type template: C{str}

    @ivar linePattern: template used to render one line in the listing table.
        It must contain the format keys B{class}, B{href}, B{text}, B{size},
        B{type} and B{encoding}.
    @type linePattern: C{str}

    @ivar contentEncodings: a mapping of extensions to encoding types.
    @type contentEncodings: C{dict}

    @ivar defaultType: default type used when no mimetype is detected.
    @type defaultType: C{str}

    @ivar dirs: filtered content of C{path}, if the whole content should not be
        displayed (default to C{None}, which means the actual content of
        C{path} is printed).
    @type dirs: C{NoneType} or C{list}

    @ivar path: directory which content should be listed.
    @type path: C{str}
    """

    linePattern = """<tr class="%(class)s">
    <td><a href="%(href)s">%(text)s</a></td>
    <td>%(size)s</td>
    <td>%(type)s</td>
    <td>%(encoding)s</td>
    <td>%(ctime)s</td>
</tr>
"""

    def __init__(self, pathname, renderTemplate, staticResourcePath, dirs=None,
                 contentTypes=File.contentTypes,
                 contentEncodings=File.contentEncodings,
                 defaultType='text/html'):
        resource.Resource.__init__(self)
        self.contentTypes = contentTypes
        self.contentEncodings = contentEncodings
        self.defaultType = defaultType
        # dirs allows usage of the File to specify what gets listed
        self.dirs = dirs
        self.path = pathname
        self.renderTemplate = renderTemplate
        self.template = HtmlGenerator(staticResourcePath)

    def _getFilesAndDirectories(self, directory):
        """
        Helper returning files and directories in given directory listing, with
        attributes to be used to build a table content with
        C{self.linePattern}.

        @return: tuple of (directories, files)
        @rtype: C{tuple} of C{list}
        """
        files = []
        dirs = []

        for path in directory:
            if _PY3:
                if isinstance(path, bytes):
                    path = path.decode("utf8")

            url = quote(path, "/")
            escapedPath = escape(path)
            childPath = filepath.FilePath(self.path).child(path)

            if childPath.isdir():
                dirs.append({'text': escapedPath + "/", 'href': url + "/",
                             'size': '', 'type': '[Directory]',
                             'encoding': '', 'ctime': ''})
            else:
                mimetype, encoding = getTypeAndEncoding(path, self.contentTypes,
                                                        self.contentEncodings,
                                                        self.defaultType)
                try:
                    size = childPath.getsize()
                except OSError:
                    continue
                files.append({
                    'text': escapedPath, "href": url,
                    'type': '[%s]' % mimetype,
                    'encoding': (encoding and '[%s]' % encoding or ''),
                    'size': formatFileSize(size),
                    'ctime': self.getCreateTime(childPath.path)})
        return dirs, files

    def getCreateTime(self, file_path):
        create_time = os.path.getctime(file_path)
        dt = datetime.fromtimestamp(create_time)
        return str(dt)

    def _buildTableContent(self, elements):
        """
        Build a table content using C{self.linePattern} and giving elements odd
        and even classes.
        """
        tableContent = []
        rowClasses = itertools.cycle(['odd', 'even'])
        for element, rowClass in zip(elements, rowClasses):
            element["class"] = rowClass
            tableContent.append(self.linePattern % element)
        return tableContent

    def render(self, request):
        """
        Render a listing of the content of C{self.path}.
        """
        request.setHeader(b"content-type", b"text/html; charset=utf-8")
        if self.dirs is None:
            directory = os.listdir(self.path)
            directory.sort()
        else:
            directory = self.dirs

        dirs, files = self._getFilesAndDirectories(directory)

        tableContent = "".join(self._buildTableContent(dirs + files))

        header = "Directory listing for %s" % (
            escape(unquote(nativeString(request.uri))),)

        done = self.template.generatePage(self.renderTemplate, {"header": header, "tableContent": tableContent})
        done = done.encode("utf8")

        return done

    def __repr__(self):
        return '<DirectoryLister of %r>' % self.path

    __str__ = __repr__
