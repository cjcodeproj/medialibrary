#!/usr/bin/env python

#
# Copyright 2022 Chris Josephes
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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET

from media.data.media.medium.productid import (
        ProductId, Barcode, SKU, OtherId
        )
from media.xml.namespaces import Namespaces

CASE1 = '''<?xml version='1.0'?>
<productId xmlns='http://vectortron.com/xml/media/media'>
 <barcode type='upc'>1234567890</barcode>
 <sku retailer='abcd'>12341234</sku>
 <other>
  <name>Proof Of Purchase</name>
  <value>1234A</value>
  <value>1234B</value>
 </other>
 <other>
  <name>Cult Classics Spine Number</name>
  <value>102</value>
 </other>
</productId>
'''


class TestProductId(unittest.TestCase):
    '''
    Unit tests covering product identification values.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.product_id = ProductId(xmlroot)

    def test_object_instance(self):
        '''
        Assert ProductId object is properly created.
        '''
        self.assertIsInstance(self.product_id, ProductId)


class TestBarcode(unittest.TestCase):
    '''
    Unit tests relating to barcodes.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        barcode_element = xmlroot.findall('./media:barcode', Namespaces.ns)[0]
        self.barcode = Barcode(barcode_element)

    def test_barcode_object(self):
        '''
        Assert Barcode object is created.
        '''
        self.assertIsInstance(self.barcode, Barcode)

    def test_barcode_str_value(self):
        '''
        Assert Barcode string return value is correct.
        '''
        self.assertEqual(str(self.barcode), '1234567890 (upc)')

    def test_barcode_value(self):
        '''
        Assert the Barcode internval value is correct.
        '''
        self.assertEqual(self.barcode.value, '1234567890')

    def test_barcode_type(self):
        '''
        Assert Barcode type value is correct.
        '''
        self.assertEqual(self.barcode.type, 'upc')


class TestSku(unittest.TestCase):
    '''
    Unit tests relating to a retailer SKU value.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        sku_element = xmlroot.findall('./media:sku', Namespaces.ns)[0]
        self.sku = SKU(sku_element)

    def test_sku_object(self):
        '''
        Assert SKU object is created.
        '''
        self.assertIsInstance(self.sku, SKU)

    def test_sku_str_value(self):
        '''
        Assert SKU object string return value is correct.
        '''
        self.assertEqual(str(self.sku), '12341234 (abcd)')

    def test_sku_value(self):
        '''
        Asseert the SKU internal value is correct.
        '''
        self.assertEqual(self.sku.value, '12341234')

    def test_sku_retailer(self):
        '''
        Test retailer attribute.
        '''
        self.assertEqual(self.sku.retailer, 'abcd')


class TestOther(unittest.TestCase):
    '''
    Tests for other measurable/identifiable values on a piece
    of media.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        others = xmlroot.findall('./media:other', Namespaces.ns)
        self.other_1 = OtherId(others[0])
        self.other_2 = OtherId(others[1])

    def test_other_object(self):
        '''
        Assert OtherID object exists.
        '''
        self.assertIsInstance(self.other_1, OtherId)

    def test_other_object_name(self):
        '''
        Assert name value is correct.
        '''
        self.assertEqual(self.other_1.name, 'Proof Of Purchase')

    def test_other_object_value_count(self):
        '''
        Assert both values are captured.
        '''
        self.assertEqual(len(self.other_1.values), 2)


if __name__ == '__main__':
    unittest.main()
