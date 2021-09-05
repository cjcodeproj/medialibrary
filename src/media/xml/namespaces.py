#!/usr/bin/env python
'''XML Namespace Constants'''


class Namespaces():
    '''Static data on XML Namespaces'''
    ns = {
            "media": "http://vectortron.com/xml/media/media",
            "movie": "http://vectortron.com/xml/media/movie"
        }

    @classmethod
    def nsf(cls, in_tag):
        '''return the fully qualified namespace to the prefix format'''
        return '{' + Namespaces.ns[in_tag] + '}'

    @classmethod
    def ns_strip(cls, in_tag):
        '''Strip the namespace from an element'''
        out = in_tag.split("}", 1)
        return out[1]
