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

'''
media.tools.meta.authorship module
'''

import datetime
import argparse
from media.data.media.meta.authorship import (
        AuthorshipRecord, Author, Catalog, CreationRecord)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Generate authorship record for files.')
    parser.add_argument('--author', help='Author of record')
    parser.add_argument('--email', help='Author email address')
    parser.add_argument('--title', help='Title of record')
    args = parser.parse_args()

    author_record = AuthorshipRecord()
    catalog = Catalog()
    author_info = Author()
    if args.title:
        author_record.title = args.title
    if args.author or args.email:
        if args.author:
            author_info.name = args.author
        if args.email:
            author_info.email = args.email
        catalog.authors.append(author_info)
    if catalog:
        author_record.catalog = catalog

    creation = CreationRecord()
    creation.tstamp = datetime.date.today()
    if author_info.name:
        creation.authors.append(author_info)
    author_record.changelog.append(creation)

    print(author_record.to_xml())
