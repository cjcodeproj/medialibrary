#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


# pylint: disable=too-few-public-methods

'''Authorship record information for media data.'''

from datetime import date, datetime
import xml.etree.ElementTree as ET
from media.xml.namespaces import Namespaces


class AuthorshipRecord():
    """
    Record showing the authorship of a piece of vtmedia data.
    """
    def __init__(self, in_element=None):
        self.title = ''
        self.catalog = None
        self.summary = None
        self.changelog = []
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'title':
                self.title = child.text.strip()
            elif tagname == 'catalog':
                self.catalog = Catalog(child)
            elif tagname == 'summary':
                self.summary = Summary(child)
            elif tagname == 'changelog':
                for chg_element in child:
                    chg_tag = Namespaces.ns_strip(chg_element.tag)
                    if chg_tag == 'change':
                        self.changelog.append(ChangeRecord(chg_element))
                    elif chg_tag == 'creation':
                        self.changelog.append(CreationRecord(chg_element))

    def to_element(self):
        """
        Construct an Element object from data.
        """
        authorship = ET.Element('authorshipRecord')
        authorship.set('xmlns', Namespaces.ns['authorship'])
        if self.title:
            ET.SubElement(authorship, 'title').text = self.title
        if self.catalog:
            authorship.append(self.catalog.to_element())
        if self.summary:
            authorship.append(self.summary.to_element())
        if self.changelog:
            changelog = ET.Element('changelog')
            for chg in self.changelog:
                changelog.append(chg.to_element())
            authorship.append(changelog)
        return authorship

    def to_xml(self):
        """
        Return direct XML output from Element object.
        """
        author = self.to_element()
        ET.indent(author)
        return ET.tostring(author, xml_declaration=True).decode()


class Catalog():
    """
    Catalog information for the metarecord, including
    a unique identifier, author, and license information.
    """
    def __init__(self, in_element=None):
        self.identity = ''
        self.authors = []
        self.license = None
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'id':
                self.identity = child.text.strip()
            elif tagname == 'authors':
                for auth_element in child:
                    auth_tag = Namespaces.ns_strip(auth_element.tag)
                    if auth_tag == 'author':
                        self.authors.append(Author(auth_element))
            elif tagname == 'license':
                self.license = License(child)

    def to_element(self):
        """
        Construct an Element object for the data.
        """
        catalog = ET.Element('catalog')
        if self.identity:
            ET.SubElement(catalog, 'id').text = self.identity
        if self.authors:
            alist = ET.Element('authors')
            for auth in self.authors:
                alist.append(auth.to_element())
            catalog.append(alist)
        if self.license:
            catalog.append(self.license.to_element())
        return catalog

    def to_xml(self):
        """
        Return direct XML string.
        """
        return ET.tostring(self.to_element())


class Summary():
    """
    Summary information for an authorship record.
    """
    def __init__(self, in_element=None):
        self.lang = ''
        self.abstract = ''
        self.internal_notes = ''
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'lang':
                self.lang = child.text.strip()
            elif tagname == 'abstract':
                self.abstract = child.text.strip()
            elif tagname == 'internalNotes':
                self.internal_notes = child.text.strip()

    def to_element(self):
        """
        Construct an element object from the data.
        """
        summary = ET.Element('summary')
        if self.lang:
            ET.SubElement(summary, 'lang').text = self.lang
        if self.abstract:
            ET.SubElement(summary, 'abstract').text = self.abstract
        if self.internal_notes:
            ET.SubElement(summary, 'internalNotes').text = self.internal_notes
        return summary

    def to_xml(self):
        """
        Return raw XML string.
        """
        return ET.tostring(self.to_element())


class Author():
    """
    Identity of the author(s) of a media record.
    """
    def __init__(self, in_element=None):
        self.name = ''
        self.email = ''
        self.url = ''
        self.fingerprint = ''
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'name':
                self.name = child.text.strip()
            elif tagname == 'email':
                self.email = child.text.strip()
            elif tagname == 'url':
                self.url = child.text.strip()
            elif tagname == 'fingerprint':
                self.fingerprint = child.text.strip()

    def to_element(self):
        """
        Construct an Element object from the data.
        """
        author = ET.Element('author')
        if self.name:
            ET.SubElement(author, 'name').text = self.name
        if self.email:
            ET.SubElement(author, 'email').text = self.email
        if self.url:
            ET.SubElement(author, 'url').text = self.url
        if self.fingerprint:
            ET.SubElement(author, 'fingerprint').text = self.fingerprint
        return author

    def to_xml(self):
        """
        Return raw XML string.
        """
        return ET.tostring(self.to_element())


class License():
    """
    License information for a record.
    """
    def __init__(self, in_element=None):
        self.code = None
        self.notice = ''
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'code':
                self.code = LicenseCode(child)
            elif tagname == 'notice':
                self.notice = child.text.strip()

    def to_element(self):
        """
        Build the element object with data.
        """
        file_license = ET.Element('license')
        if self.code:
            file_license.append(self.code.to_element())
        if self.notice:
            ET.SubElement(file_license, 'notice').text = self.notice
        return file_license

    def to_xml(self):
        """
        Return the XML as a string.
        """
        return ET.tostring(self.to_element())


class LicenseCode():
    """
    A shortened code representation of a license.
    Could be SPDX, but could be something else down the road.
    """
    def __init__(self, in_element=None):
        self.type = ''
        self.text = ''
        if in_element:
            self.text = in_element.text.strip()
            if 'type' in in_element.attrib:
                self.type = in_element.attrib['type'].strip()

    def to_element(self):
        """
        Built the Element object with data.
        """
        code = ET.Element('code')
        if self.text:
            code.text = self.text
        if self.type:
            code.set('type', self.type)
        return code

    def to_xml(self):
        """
        Return the XML as a string.
        """
        return ET.tostring(self.to_element())


class AbstractChangeRecord():
    """
    Abstract class representing a change record.
    """
    def __init__(self, in_element=None):
        self.tstamp = None
        self.ticket = None
        self.authors = []
        self.notes = ''
        if in_element:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'date':
                self.tstamp = date.fromisoformat(child.text.strip())
            elif tagname == 'timestamp':
                self.tstamp = datetime.fromisoformat(child.text.strip())
            elif tagname == 'ticket':
                self.ticket = ChangeTicket(child)
            elif tagname == 'authors':
                for auth_element in child:
                    auth_tag = Namespaces.ns_strip(auth_element.tag)
                    if auth_tag == 'author':
                        self.authors.append(Author(auth_element))
            elif tagname == 'notes':
                self.notes = child.text.strip()

    def build_element(self, record):
        """
        Build the change record object.
        """
        if self.tstamp:
            date_element = None
            if isinstance(self.tstamp, date):
                date_element = ET.SubElement(record, 'date')
            elif isinstance(self.tstamp, datetime):
                date_element = ET.SubElement(record, 'timestamp')
            date_element.text = self.tstamp.isoformat()
        if self.ticket:
            record.append(self.ticket.to_element())
        if self.authors:
            alist = ET.Element('authors')
            for auth in self.authors:
                alist.append(auth.to_element())
            record.append(alist)
        if self.notes:
            ET.SubElement(record, 'notes').text = self.notes
        return record


class ChangeRecord(AbstractChangeRecord):
    """
    Change record reflecting a single change.
    """
    def to_element(self):
        """
        Generate Element object with data.
        """
        record = ET.Element('change')
        super().build_element(record)
        return record

    def to_xml(self):
        """
        Return XML stirng.
        """
        return ET.tostring(self.to_element())


class CreationRecord(AbstractChangeRecord):
    """
    Change record specifically referencing the
    creation of the data record.
    """
    def to_element(self):
        """
        Generate Element object with data.
        """
        record = ET.Element('creation')
        super().build_element(record)
        return record

    def to_xml(self):
        """
        Return XML string.
        """
        return ET.tostring(self.to_element())


class ChangeTicket():
    """
    A change ticket with optional hyperlink to
    provide further details on a change.
    """
    def __init__(self, in_element=None):
        self.ticket_id = ''
        self.href = ''
        if in_element:
            self.ticket_id = in_element.text.strip()
            if 'href' in in_element.attrib:
                self.href = in_element.attrib['href'].strip()

    def to_element(self):
        """
        Generate Element object populated with data.
        """
        ticket = ET.Element('ticket')
        if self.ticket_id:
            ticket.text = self.ticket_id
        if self.href:
            ticket.set('href', self.href)
        return ticket

    def to_xml(self):
        """
        Return XML string of data.
        """
        return ET.tostring(self.to_element())
