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


# Enums were only introduced in python 3.4 and then backported,
# this tests help stablishing if they are working in previous versions too.

from unittest import TestCase
from pyone import MARKETAPP_STATE

class ConstantTest(TestCase):
    def test_int_constants(self):
        self.assertEqual(MARKETAPP_STATE.READY,1)