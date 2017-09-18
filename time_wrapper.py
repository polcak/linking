# time_wrapper.py: Converts various time representations to Unix timestamp.
# Copyright (C) 2017 Libor Polčák <ipolcak@fit.vutbr.cz>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from dateutil import parser

months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

class TimeWrapper():
    """ Converts various string representation of time to Unix timestamp. """

    def __init__(self, s):
        try:
            self.v = float(s)
        except ValueError:
            self.v = None
        if not self.v:
            t = None
            try:
                t = parser.parse(s)
            except:
                try:
                    t = parser.parse(s.replace(":", "T", 1))
                except:
                    pass
            if t == None:
                raise ValueError("%s is not a supported time format" % s)
            self.v = t.timestamp()

    def get(self):
        return self.v
