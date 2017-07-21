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

class EdgeScopeConstraintFunction(ConstraintFunction):
    """ This is a base class for scope constraint functions depending on edges."""
    def __init__(self, g):
        ConstraintFunction.__init__(self, g)

    def _allow_edge(self, src, dst):
        """ Edge conformance, abstract mehod. """
        raise NotImplementedError("Abstract method")

    def _allow_first_edge(self, src, dst):
        """ Edge conformance, abstract mehod. """
        raise NotImplementedError("Abstract method")

    def check_path(self, p):
        """ Redefines base class method. """
        if len(p) <= 1:
            return (False, False)
        src1, dst1 = p[0:2]
        if self._allow_first_edge(src1, dst1):
            for n1, n2 in zip(range(1, len(p)), range(2, len(p))):
                src = p[n1]
                dst = p[n2]
                if not self._allow_edge(src, dst):
                    return (False, False)
            return (True, True)
        else:
            return (False, False)

class PartialIdentityComponents(EdgeScopeConstraintFunction):
    """ A constraint function for Components of a partial identity. """
    def __init__(self, g):
        self.__rules = {
            "alpha": ["alpha"],
            "beta": ["alpha"],
            "gamma": ["beta"],
            "delta": ["beta", "gamma"],
            "lambda": ["alpha"],
            "rho": [],
        }
        EdgeScopeConstraintFunction.__init__(self, g)

    def _allow_edge(self, src, dst):
        return self._g.node[dst]["category"] in self.__rules[self._g.node[src]["category"]]

    def _allow_first_edge(self, src, dst):
        return self._allow_edge(src, dst)

class SpecificComputerOrInterface(EdgeScopeConstraintFunction):
    """ A constraint function for Identifiers used by a specific computer. """
    def __init__(self, g):
        self.__rules = {
            "alpha": ["alpha"],
            "beta": ["alpha", "gamma"],
            "gamma": ["beta"],
            "delta": [],
            "lambda": [],
            "rho": [],
        }
        EdgeScopeConstraintFunction.__init__(self, g)

    def _allow_edge(self, src, dst):
        return self._g.node[dst]["category"] in self.__rules[self._g.node[src]["category"]]

    def _allow_first_edge(self, src, dst):
        return self._allow_edge(src, dst)

class SpecificComputerOrInterfaceLoggedUser(EdgeScopeConstraintFunction):
    """ A constraint function for Identifiers of all computers where a specific user was authenticated or logged in. """
    def __init__(self, g):
        self.__rules_first = {
            "alpha": [],
            "beta": [],
            "gamma": [],
            "delta": ["beta", "gamma"],
            "lambda": ["beta"],
            "rho": [],
        }
        self.__specific_computer_or_interface = SpecificComputerOrInterface(g)
        EdgeScopeConstraintFunction.__init__(self, g)

    def _allow_edge(self, src, dst):
        return self.__specific_computer_or_interface.check_path([src, dst])[0]

    def _allow_first_edge(self, src, dst):
        return self._g.node[dst]["category"] in self.__rules_first[self._g.node[src]["category"]]

class UsersAccessingResource(EdgeScopeConstraintFunction):
    """ A constraint function for Identifiers of all users accessing a specific resource. """
    def __init__(self, g):
        self.__rules_first = {
            "alpha": [],
            "beta": [],
            "gamma": [],
            "delta": [],
            "lambda": [],
            "rho": ["lambda"],
        }
        EdgeScopeConstraintFunction.__init__(self, g)

    def _allow_edge(self, src, dst):
        return False

    def _allow_first_edge(self, src, dst):
        return self._g.node[dst]["category"] in self.__rules_first[self._g.node[src]["category"]]

class UsersLoggedIn(ConstraintFunction):
    """ A constraint function for All user accounts logged in from a computer or a set of computers. """
    def __init__(self, g):
        self.__rules_last = {
            "alpha": [],
            "beta": ["delta", "lambda"],
            "gamma": ["delta"],
            "delta": [],
            "lambda": [],
            "rho": ["lambda"],
        }
        self.__l2 = SpecificComputerOrInterface(g)
        self.__l3 = SpecificComputerOrInterfaceLoggedUser(g)
        EdgeScopeConstraintFunction.__init__(self, g)

    def check_path(self, p):
        """ @Overloads """
        if len(p) < 2:
            return (False, True)
        last_src = p[-2]
        last_dst = p[-1]
        if self._g.node[last_dst]["category"] not in \
            self.__rules_last[self._g.node[last_src]["category"]]:
            return (False, True)
        all_but_last = p[:-1]
        return (len(all_but_last) == 1 or self.__l2.check_path(all_but_last)[0] or
            self.__l3.check_path(all_but_last)[0], True)

class AccessedResources(ConstraintFunction):
    """ A constraint function for All accessed resources. """
    def __init__(self, g):
        self.__l2 = SpecificComputerOrInterface(g)
        self.__l3 = SpecificComputerOrInterfaceLoggedUser(g)
        EdgeScopeConstraintFunction.__init__(self, g)

    def __remove_beginning_alternate_names(self, p):
        """ Helper functions that removes multiple lambdas at the beginning """
        lambda_last = (self._g.node[p[0]]["category"] == "lambda")
        if not lambda_last:
            return p
        ret = []
        for x, y in zip(p, p[1:]):
            if lambda_last:
                if self._g.node[y]["category"] != "lambda":
                    ret.append(x)
                    ret.append(y)
                    lambda_last = False
            else:
                ret.append(y)
        if lambda_last:
            ret = [p[-1]]
        return ret

    def check_path(self, p):
        """ @Overloads """
        p = self.__remove_beginning_alternate_names(p)
        if len(p) < 2:
            return (False, True)
        last_src = p[-2]
        last_dst = p[-1]
        if self._g.node[last_src]["category"] not in ["beta", "lambda"] or \
                self._g.node[last_dst]["category"] != "rho":
            return (False, self.__l2.check_path(p) or self.__l3.check_path(p))
        all_but_last = p[:-1]
        return (len(all_but_last) == 1 or self.__l2.check_path(all_but_last)[0] or
            self.__l3.check_path(all_but_last)[0], True)



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
                return (False, False)
        return (True, True)

class ActiveContinuouslyDuring(EdgeConstraintFunction):
    """ All edges along the path have to be active during the whole duration. """
    def __init__(self, g, b_time, e_time):
        EdgeConstraintFunction.__init__(self, g)
        self.__b_time = b_time
        self.__e_time = e_time

    def _allow_edge(self, validfrom, validto, identitysource, inaccuracy):
        """ Defines base class abstract method. """
        return validfrom <= self.__b_time and validto >= self.__e_time

class ActiveDuringTime(ConstraintFunction):
    """ Identifiers have to be linkable for at least a moment during the given duration. """
    def __init__(self, g, b_time, e_time):
        ConstraintFunction.__init__(self, g)
        self.__b_time = b_time
        self.__e_time = e_time

    def _check_path(self, p, prevstart, prevend):
        src = p[0]
        dst = p[1]
        for i, e in self._g.edge[src][dst].items():
            r = self._check_edge_and_following(p[1:], prevstart, prevend, **e)
            if r:
                return True
        return False

    def _check_edge_and_following(self, p, prevstart, prevend, validfrom, validto, identitysource, inaccuracy):
        s = max(self.__b_time, prevstart, validfrom)
        e = min(self.__e_time, prevend, validto)
        if e < s:
            return False
        if len(p) < 2:
            return True
        return self._check_path(p, validfrom, validto)

    def check_path(self, p):
        """ Redefines base class method. """
        if len(p) < 2:
            return (False, True)
        r = self._check_path(p, self.__b_time, self.__e_time)
        return (r, r)

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
        res = self.__compute_min_inaccuracy(p) <= self._max_inaccuracy
        return (res, res)


