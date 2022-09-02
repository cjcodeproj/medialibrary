#!/usr/bin/env python
'''XML Namespace Constants'''

#
# This should actually check for a value error
#


def xs_bool(in_string):
    '''Takes an XSD boolean value and converts it to a Python bool'''
    if in_string in ['true', '1']:
        return True
    return False


def xs_text_strip(in_string):
    '''Strip outer whitespace from a string in an XML element.'''
    chunk = in_string.strip()
    if chunk:
        return chunk
    return None
