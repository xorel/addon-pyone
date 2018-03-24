# coding: utf-8

# Copyright 2018 www.privaz.io Valletech AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import ssl
import pyone
import os

# Deprecated utility, testing backward compatibility
from pyone.util import one2dict

# Capture OpenNebula Session parameters from environment or hardcoded...
testSession = os.getenv("PYONE_SESSION","oneadmin:onepass")
testEndpoint = os.getenv("PYONE_ENDPOINT", 'https://192.168.121.55/RPC2')

# Disable SSL checks for TEST environment only, and deal with Centos, see issue #13
if "PYTHONHTTPSVERIFY" in os.environ:
    one = pyone.OneServer(testEndpoint, session=testSession)
else:
    one = pyone.OneServer(testEndpoint, session=testSession, context=ssl._create_unverified_context())

class IntegrationTests(unittest.TestCase):

    def test_pool_info(self):
        hostpool = one.hostpool.info()
        self.assertGreater(len(hostpool.HOST), 0)
        host0 = hostpool.HOST[0]
        self.assertEqual(host0.ID, 0)

    def test_auth_error(self):
        with self.assertRaises(pyone.OneAuthenticationException):
            # Disable SSL checks for TEST environment only, and deal with Centos, see issue #13
            if "PYTHONHTTPSVERIFY" in os.environ:
                xone = pyone.OneServer(testEndpoint, session="oneadmin:invalidpass")
            else:
                xone = pyone.OneServer(testEndpoint, session="oneadmin:invalidpass", context=ssl._create_unverified_context())
            xone.hostpool.info()

    def test_market_info(self):
        marketpool = one.marketpool.info()
        self.assertGreater(len(marketpool.MARKETPLACE), 0)
        m0 = marketpool.MARKETPLACE[0]
        self.assertEqual(m0.NAME, "OpenNebula Public")

    def test_vm_pool(self):
        vmpool = one.vmpool.info(-2,-1,-1,-1)
        vm0 = vmpool.VM[0]
        self.assertEqual(vm0.UNAME, "oneadmin")

    def test_invalid_method(self):
        with self.assertRaises(pyone.OneException):
            one.invalid.api.call()

    def test_template_attribute_vector_parameter(self):
        one.host.update(0,  {"LABELS": "HD,LOWPOWER"}, 1)

    def test_xml_template_parameter(self):
        one.host.update(1,
            {
                'TEMPLATE': {
                    'LABELS': 'SSD',
                    'MAX_CPU': '176'
                }
            }, 1)

    def test_empty_dictionary(self):
        with self.assertRaises(Exception):
            one.host.update(0, {}, 1)

    def test_retrieve_template_as_DOM_no_longer_working(self):
        with self.assertRaises(AttributeError):
            host = one.host.info(0)
            template = host.TEMPLATE.toDOM()
            arch = template.getElementsByTagName('ARCH')[0].firstChild.nodeValue
            self.assertEqual(arch, 'x86_64')

    def test_retrieve_template_as_deprecated_dict(self):
        host = one.host.info(0)
        tdict = one2dict(host.TEMPLATE)
        arch = tdict['TEMPLATE']['ARCH']
        self.assertEqual(arch, 'x86_64')

    def test_retrieve_template_as_new_dict(self):
        host = one.host.info(0)
        arch = host.TEMPLATE['ARCH']
        self.assertEqual(arch, 'x86_64')

    def test_international_characters_issue_006(self):
        one.host.update(0,
            {
                'TEMPLATE': {
                    'NOTES': 'Hostname is: ESPAÑA',
                }
            }, 1)
        host = one.host.info(0)
        self.assertIn(host.TEMPLATE['NOTES'], [u"Hostname is: ESPAÑA"])

    def test_modify_template(self):
        host = one.host.info(0)
        host.TEMPLATE["NOTES"]="Hostname is: España"
        one.host.update(0,host.TEMPLATE,1)
        host2 = one.host.info(0)
        self.assertIn(host2.TEMPLATE['NOTES'], [u"Hostname is: España"])


    def test_vm_info(self):
        vm = one.vm.info(0)
        labels = vm.USER_TEMPLATE.get('LABELS', "")
        culsterId = vm.TEMPLATE['DISK']['CLUSTER_ID']
        self.assertEqual(vm.ID,0)
