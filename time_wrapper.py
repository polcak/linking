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

    reprs = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            ]

    def __init__(self, s):
        try:
            self.v = float(s)
        except ValueError:
            self.v = None
        if not self.v:
            for r in self.reprs:
                try:
                    self.v = time.mktime(time.strptime(s, r))
                except ValueError:
                    continue
                break
            else:
                raise ValueError("%s is not a supported time format" % s)

    def get(self):
        return self.v
