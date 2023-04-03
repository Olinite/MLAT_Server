# -*- mode: python; indent-tabs-mode: nil -*-

# Part of mlat-server: a Mode S multilateration server
# Copyright (C) 2015  Oliver Jowett <oliver@mutability.co.uk>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Decoder for 12-bit squawk (identity) fields contained in some Mode S messages.
"""

__all__ = ('decode_id13',)


def _make_upper_table():
    ut = []
    for i in range(64):
        v = 0
        id13 = i << 7
        if id13 & 0x1000:
            v |= 0x0010  # C1
        if id13 & 0x0800:
            v |= 0x1000  # A1
        if id13 & 0x0400:
            v |= 0x0020  # C2
        if id13 & 0x0200:
            v |= 0x2000  # A2
        if id13 & 0x0100:
            v |= 0x0040  # C4
        if id13 & 0x0080:
            v |= 0x4000  # A4
        ut.append(v)
    return ut


def _make_lower_table():
    lt = []
    for id13 in range(64):
        v = 0
        # 0040 unused (M/X)
        if id13 & 0x0020:
            v |= 0x0100  # B1
        if id13 & 0x0010:
            v |= 0x0001  # D1/Q
        if id13 & 0x0008:
            v |= 0x0200  # B2
        if id13 & 0x0004:
            v |= 0x0002  # D2
        if id13 & 0x0002:
            v |= 0x0400  # B4
        if id13 & 0x0001:
            v |= 0x0004  # D4
        lt.append(v)

    return lt


def decode_id13(id13):
    """Decode a 13-bit Mode A squawk.

    The expected ordering is that from Annex 10 vol 4 3.1.2.6.7.1:

      C1, A1, C2, A2, C4, A4, ZERO, B1, D1, B2, D2, B4, D4

    Returns the squawk as a 4-character string."""

    return '{0:04x}'.format(_lt[id13 & 63] | _ut[id13 >> 7])


if __name__ == '__main__':
    _lt = _make_lower_table()
    _ut = _make_upper_table()

    print('# -*- mode: python; indent-tabs-mode: nil -*-')
    print('# generated by modes.squawk: python3 -m modes.squawk')
    print()
    print('lt = (')
    for i in range(0, len(_lt), 8):
        print('    ' + ', '.join(['0x{0:04x}'.format(v) for v in _lt[i:i+8]]) + ',')
    print(')')
    print()
    print('ut = (')
    for i in range(0, len(_ut), 8):
        print('    ' + ', '.join(['0x{0:04x}'.format(v) for v in _ut[i:i+8]]) + ',')
    print(')')

else:
    try:
        from .squawk_lookup import ut as _ut, lt as _lt
    except ImportError:
        _lt = _make_lower_table()
        _ut = _make_upper_table()
