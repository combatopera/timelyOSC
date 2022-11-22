# Copyright 2019 Andrzej Cichocki

# This file is part of timelyOSC.
#
# timelyOSC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# timelyOSC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with timelyOSC.  If not, see <http://www.gnu.org/licenses/>.

from timelyOSC import Bundle, Message, parse
from unittest import TestCase

class TestBundle(TestCase):

    def test_roundtrip(self):
        b = parse(Bundle(346.125, [
            Bundle(500, [Message('/zyx', [])]),
            Message('/woo', [100, 'yay']),
        ]).ser())
        self.assertEqual(346.125, b.timetag)
        e, f = b.elements
        self.assertEqual(500, e.timetag)
        g, = e.elements
        self.assertEqual('/zyx', g.addrpattern)
        self.assertEqual([], g.args)
        self.assertEqual('/woo', f.addrpattern)
        self.assertEqual([100, 'yay'], f.args)
