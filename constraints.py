# constraints.py: Constraints function for identity linking model
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

# Ordering on categories
ordering = {
        "alpha": {},
        "beta": {"alpha"},
        "gamma": {"alpha", "beta"},
        "delta": {"alpha", "beta", "gamma"},
        "lambda": {"alpha"},
        }

# Definition of constraint functions
class ConstraintFunction():
    """ A base class for constraint functions. """
    def __init__(self, g):
        """ Constructor.

        @param g The graphs to operate on.
        """
        self._g = g

    def check_path(self, p):
        """ Applies the constraint function on the path p.

        @param p The path on which this constraint function should be applied.

        This is an abstract function.
        """
        raise NotImplementedError("Abstract method called")

class ScopeConstraintFunction():
    """ A base class for scope constraint function. """
    def __init__(self, g):
        ConstraintFunction.__init__(self, g)

    def _check_path_source(self, psrc):
        """ Checks if this constraint function allows paths to start from psrc.
        
        Deafult implementation, returns always True.
        """
        return True

    def _allow_identifiers(self, src, dst):
        """ Check for the validity of nodes on a link on a path.

        @param src The current identifier on the path.
        @param dst The following identifier on the path.
        """
        return True

    def check_path(self, p):
        """ Redefines base class method. """
        if not self._check_path_source(p[0]):
            return False
        for n1, n2 in zip(range(len(p)), range(1, len(p))):
            src = p[n1]
            dst = p[n2]
            if not self._allow_identifiers(src, dst):
                return False
        return True

class SpecificIdentifier(ScopeConstraintFunction):
    """ A specific identifier constraint function. """
    def __init__(self, g):
        ScopeConstraintFunction.__init__(self, g)

    def _allow_identifiers(self, src, dst):
        return self._g.node[dst]["category"] in ordering[self._g.node[src]["category"]]

class SpecificComputerOrInterface(ScopeConstraintFunction):
    """ Specific computer(s) or interface(s) """
    def __init__(self, g):
        ScopeConstraintFunction.__init__(self, g)

    def _allow_identifiers(self, src, dst):
        return self._g.node[dst]["category"] in ordering["delta"]

class SpecificUser(ScopeConstraintFunction):
    """ Specific user """
    def __init__(self, g):
        ScopeConstraintFunction.__init__(self, g)

    def _check_path_source(self, psrc):
        self.__psrc_c = self._g.node[psrc]["category"]
        self.__allow_cs = set(list(ordering[self.__psrc_c]) + [self.__psrc_c])
        return self.__psrc_c in ["gamma", "delta"]

    def _allow_identifiers(self, src, dst):
        return self._g.node[dst]["category"] in self.__allow_cs


class AllRelatedIndentifiers(ConstraintFunction):
    """ All related identifiers, it accepts all paths. """
    def __init__(self, g):
        ConstraintFunction.__init__(self, g)

    def check_path(self, p):
        return True

class EdgeConstraintFunction(ConstraintFunction):
    """ This is a base class for constraint functions depending only on edges."""
    def __init__(self, g):
        ConstraintFunction.__init__(self, g)

    def _allow_edge(self, validfrom, validto, identitysource, inaccuracy):
        """ Edge conformance, abstract mehod. """
        raise NotImplementedError("Abstract method")

    def __check_link(self, src, dst):
        for i, e in self._g.edge[src][dst].items():
            # Test validity of edge, one is sufficient to be valid
            if self._allow_edge(**e):
                return True
        return False

    def check_path(self, p):
        """ Redefines base class method. """
        for n1, n2 in zip(range(len(p)), range(1, len(p))):
            src = p[n1]
            dst = p[n2]
            if not self.__check_link(src, dst):
                return False
        return True

class ActiveAtSpecificTime(EdgeConstraintFunction):
    """ All  """
    def __init__(self, g, ref_time):
        EdgeConstraintFunction.__init__(self, g)
        self.__ref_time = ref_time

    def _allow_edge(self, validfrom, validto, identitysource, inaccuracy):
        """ Defines base class abstract method. """
        return self.__ref_time >= validfrom and self.__ref_time <= validto

class MaximalPathInaccuracy(ConstraintFunction):
    """ Checks the path for a maximal total inaccuracy """
    def __init__(self, g, max_inaccuracy):
        ConstraintFunction.__init__(self, g)
        self._max_inaccuracy = max_inaccuracy

    def __get_edge_min_inaccuracy(self, multie):
        min_inaccuracy = None
        for e in multie.values():
            try:
                min_inaccuracy = min(min_inaccuracy, e["inaccuracy"])
            except TypeError: # No inaccuracy set, yet
                min_inaccuracy = e["inaccuracy"]
        return min_inaccuracy

    def __compute_min_inaccuracy(self, p):
        inaccuracy = 0
        for n1, n2 in zip(range(len(p)), range(1, len(p))):
            src = p[n1]
            dst = p[n2]
            inaccuracy += self.__get_edge_min_inaccuracy(self._g.edge[src][dst])
        return inaccuracy

    def check_path(self, p):
        """ Redefines base class method. """
        return self.__compute_min_inaccuracy(p) <= self._max_inaccuracy


