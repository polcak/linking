# inaccuracy.py: Inaccuracy computations for identity linking model
# Copyright (C) 2018 Libor Polčák <ipolcak@fit.vutbr.cz>
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

from id_attrs import id_attrs

class inaccuracy_list(object):
    """ This datastructure stores a list of identifiers and their minimal inaccuracy """

    def __init__(self, iterable):
        self.__content = {}
        self.__update(iterable)

    def __update(self, iterable):
        """ Updates current list with items in the iterable. """
        for item in iterable:
            if item.value in self.__content:
                self.__content[item.value] = min(self.__content[item.value], \
                        item.inaccuracy)
            else:
                self.__content[item.value] = item.inaccuracy

    def update(self, other):
        """ Updates current list with items in the other inaccuracy_list. """
        self.__update(other.get_all())

    def get_all(self):
        """ Returns all items. """
        return [id_attrs(k, v) for k, v in self.__content.items()]

    def __iter__(self):
        """ Returns an iterator. """
        return iter(self.get_all())

def compute_inaccuracy(g, p):
    """ Returns minimal path inaccuracy. """
    inaccuracy = 0
    for n1, n2 in zip(range(len(p)), range(1, len(p))):
        src = p[n1]
        dst = p[n2]
        inaccuracy += __get_edge_min_inaccuracy(g.edge[src][dst])
    return inaccuracy

def __get_edge_min_inaccuracy(multie):
    """ Returns minimal inaccuracy of the multiedge. """
    min_inaccuracy = None
    for e in multie.values():
        try:
            min_inaccuracy = min(min_inaccuracy, e["inaccuracy"])
        except TypeError: # No inaccuracy set, yet
            min_inaccuracy = e["inaccuracy"]
    return min_inaccuracy
