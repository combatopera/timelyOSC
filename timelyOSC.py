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

from io import BytesIO
from struct import Struct

bundlemagic = b'#bundle\0'
charset = 'ascii'
int32 = Struct('>i')
float32 = Struct('>f')
float64 = Struct('>d')
timetag = Struct('>II')
seconds1970 = 25567 * 24 * 60 * 60
fractionlimit = 1 << 32

def parse(v):
    return (Bundle.read if v.startswith(bundlemagic) else Message.read)(v)

class Reader:

    def __init__(self, v):
        self.c = 0
        self.v = v

    def __bool__(self):
        return self.c < len(self.v)

    def consume(self, n):
        self.c += n
        return self.v[self.c - n:self.c]

    def align(self):
        self.c += (-self.c) % 4

    def int32(self):
        return int32.unpack(self.consume(4))[0]

    def float32(self):
        return float32.unpack(self.consume(4))[0]

    def float64(self):
        return float64.unpack(self.consume(8))[0]

    def blob(self):
        blob = self.consume(self.int32())
        self.align()
        return blob

    def string(self):
        text = self.consume(self.v.index(b'\0', self.c) - self.c).decode(charset)
        self.c += 1 # Consume at least one null.
        self.align()
        return text

    def timetag(self):
        seconds1900, fraction = timetag.unpack(self.consume(8))
        return seconds1900 - seconds1970 + fraction / fractionlimit

    def element(self):
        return parse(self.consume(self.int32()))

class Writer:

    def __init__(self, f):
        self._f = f

    def s(self, text):
        v = text.encode(charset) + b'\0'
        v += b'\0' * ((-len(v)) % 4)
        self._f.write(v)

    def i(self, n):
        self._f.write(int32.pack(n))

    def f(self, n):
        self._f.write(float32.pack(n))

class Bundle:

    @classmethod
    def read(cls, v):
        r = Reader(v)
        r.string()
        timetag = r.timetag()
        elements = []
        while r:
            elements.append(r.element())
        return cls(timetag, elements)

    def __init__(self, timetag, elements):
        self.timetag = timetag
        self.elements = elements

    def __repr__(self):
        return f"{type(self).__name__}({self.timetag!r}, {self.elements!r})"

    def ser(self):
        f = BytesIO()
        w = Writer(f)
        w.s('#bundle')
        f.write(timetag.pack(seconds1970 + int(self.timetag // 1), round(self.timetag % 1 * fractionlimit)))
        for e in (e.ser() for e in self.elements):
            w.i(len(e))
            f.write(e)
        return f.getvalue()

class Message:

    types = dict(
        i = Reader.int32,
        f = Reader.float32,
        d = Reader.float64,
        b = Reader.blob,
        s = Reader.string,
    )
    tags = {
        int: 'i',
        float: 'f',
        str: 's',
    }

    @classmethod
    def read(cls, v):
        r = Reader(v)
        return cls(r.string(), [cls.types[tt](r) for tt in r.string()[1:]])

    def __init__(self, addrpattern, args):
        self.addrpattern = addrpattern
        self.args = args

    def __repr__(self):
        return f"{type(self).__name__}({self.addrpattern!r}, {self.args!r})"

    def ser(self):
        f = BytesIO()
        w = Writer(f)
        w.s(self.addrpattern)
        tags = [self.tags[type(arg)] for arg in self.args]
        w.s(f",{''.join(tags)}")
        for tt, arg in zip(tags, self.args):
            getattr(w, tt)(arg)
        return f.getvalue()
