#!/usr/bin/env python3
# linking.py: Linking identities in a graph model
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

import argparse
import networkx as nx
import sys

from constraints import *
from time_wrapper import TimeWrapper

# Helping functions
def load_graph(gml_file):
    """ Loads identity graph from a file.

    @param gml_file The identity file.

    The idenity file graph is expected to be in the GML format, see
    http://www.fim.uni-passau.de/fileadmin/files/lehrstuhl/brandenburg/projekte/gml/gml-technical-report.pdf
    for details.

    This software has the following expectations:

    * graph.directed should be set to 0.
    * graph.multigraph should be set to 1.
    * node.label contains the unique identifier value.
    * node.category contains the category of the node, one of the alpha, beta, gamma, delta, lambda, rho;
      alpha means L4Flow, beta means IPAddr, gamma means IfcOrComp, delta means AAAUser, lambda
      means L7User, and rho means L7Resource.
    * edge.identitysource contains the identity source, i.e. an item from the set S.
    * edge.validfrom contains the starting time stamp in the UNIX format.
    * edge.validto contains the starting time stamp in the UNIX format.
    * edge.inaccuracy contains the inaccuracy of the edge.
    """
    g = nx.read_gml(gml_file)
    return g

def check_path(p, constraints):
    """ Applies all constraints on the path.

    Returns 2-tuple:
     * 1st item: True iff all constraints return True.
     * 2nd item: True iff all constraints return True.
    """
    res_valid = True
    res_cont = True
    for c in constraints:
        valid, cont = c.check_path(p)
        if not valid:
            res_valid = False
        if not cont:
            res_cont = False
    return (res_valid, res_cont)

# Helping functions for linked
def create_linked(g, p, constraints):
    last = p[-1]
    paths = []
    try:
        neighbors = nx.all_neighbors(g, last)
    except nx.exception.NetworkXError as e:
        sys.stderr.write("%s\n" % str(e))
        sys.exit(1)
    for i, n in enumerate(neighbors):
        if n not in p:
            pn = p + (n,)
            valid, cont = check_path(pn, constraints)
            if valid:
                paths += [pn]
            if cont:
                paths += create_linked(g, pn, constraints)
    return paths

# Definition of linked
def linked(g, i0, add_start, constraints):
    """ Returns a list of linked identifiers.

    @param g The identity graph.
    @param i0 The input identifier.
    @param add_start Adds start node to the output.
    @param constraints An iterable of constraint functions.
    """
    try:
        v0 = g.node[i0]
    except KeyError as e:
        sys.stderr.write("Unknown identifier %s\n" % i0)
        sys.exit(2)
    accepted_paths = create_linked(g, (i0,), constraints)
    if add_start:
        accepted_paths.append([i0])
    return set([p[-1] for p in accepted_paths])

scope_help = """The linking scope (1-8):
1~ Constraints revealing components of partial
   identity aka Other corresponding identifiers.
2~ Constraints revealing partial identities of
   specific computer aka Identifiers of
   a specific computer.
3~ Constraints revealing partial identities of
   computers where specific user authenticated
   or logged in.
4~ Constraints revealing identifiers of all
   users accessing specific resource.
5~ Constraints revealing all user accounts
   logged in or authenticated from computer or
   set of computers.
6~ Constraints revealing all accessed resources.
7~ Constraints revealing all login aliases.
8~ Constraints revealing all IP addresses
   accesing a specific resource.
"""

timescope_help = """Time scope (1-2):
1~ All edges on the path have to be valid during
   the whole period.
2~ All edges on the path have to be valid at
   least once during the period [-b, -e] and
   the period during the previous identifier
   is valid on the path. 
"""

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="Identity linking software",
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--graph_file", "-g", help="Input graph file with identities.")
    parser.add_argument("inputid", help="The input id (type: id).", default=None)
    parser.add_argument("--scope", "-s", type=int, choices = [1,2,3,4,5,6,7,8],
            help=scope_help, default=None,)
    parser.add_argument("--begintime", "-b", type=TimeWrapper, help="Begin time for which to perform linkage (local TZ).")
    parser.add_argument("--endtime", "-e", type=TimeWrapper, help="End time for which to perform linkage (local TZ).")
    parser.add_argument("--timescope", "-t", type=int, choices = [1,2],
            help=timescope_help, default=None)
    parser.add_argument("--max_inaccuracy", "-i", type=float, help="Maximal path inaccuracy.")
    parser.add_argument("--components", "-c", action="store_true", help="Compute the number of components in the graph.")
    parser.add_argument("--add_self", "-a", action="store_true", help="Add the input node to the output set")
    return parser.parse_args()

def setup_constraints(args):
    scope_cs = {
            1: PartialIdentityComponents,
            2: SpecificComputerOrInterface,
            3: SpecificComputerOrInterfaceLoggedUser,
            4: UsersAccessingResource,
            5: UsersLoggedIn,
            6: AccessedResources,
            7: Logins,
            8: IPAddrsAccessingResource,
            }
    time_scope_cs = {
            1: ActiveContinuouslyDuring,
            2: ActiveDuringTime,
            }

    constraints = []
    if args.scope:
        constraints.append(scope_cs[args.scope](g))

    if args.timescope != None:
        if args.begintime:
            if args.endtime:
                constraints.append(time_scope_cs[args.timescope](g, args.begintime.get(),
                    args.endtime.get()))
            else:
                constraints.append(time_scope_cs[args.timescope](g, args.begintime.get(),
                    args.begintime.get()))
        else:
            raise NotImplementedError("Time scope set but no begin time entered")
    elif args.begintime:
        if args.endtime:
            constraints.append(ActiveContinuouslyDuring(g, args.begintime.get(), args.endtime.get()))
        else:
            constraints.append(ActiveContinuouslyDuring(g, args.begintime.get(), args.begintime.get()))

    if args.max_inaccuracy != None:
        constraints.append(MaximalPathInaccuracy(g, args.max_inaccuracy))

    return constraints

# Main entry
if __name__ == "__main__":
    args = process_args()

    g = load_graph(args.graph_file)
    constraints = setup_constraints(args)

    if args.components:
        print("Number of components: %d" % nx.number_connected_components(g))

    if args.inputid:
        r = linked(g, args.inputid, args.add_self, constraints)
        l = list(r)
        l.sort()
        for i in l:
            print(i)
