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
    * node.category contains the category of the node, one of the alpha, beta, gamma, delta, lambda.
    * edge.identitysource contains the identity source, i.e. an item from the set S.
    * edge.validfrom contains the starting time stamp in the UNIX format.
    * edge.validto contains the starting time stamp in the UNIX format.
    * edge.inaccuracy contains the inaccuracy of the edge.
    """
    g = nx.read_gml(gml_file)
    return g

def check_path(p, constraints):
    """ Applies all constraints on the path.

    Returns True iff all constraints return True.
    """
    for c in constraints:
        if not c.check_path(p):
            return False
    return True

# Helping functions for linked
def create_linked(g, p, constraints):
    last = p[-1]
    paths = [p]
    for i, n in enumerate(nx.all_neighbors(g, last)):
        if n not in p:
            pn = p + (n,)
            if check_path(pn, constraints):
                paths += create_linked(g, pn, constraints)
    return paths

# Definition of linked
def linked(g, i0, constraints):
    """ Returns a list of linked identifiers.

    @param g The identity graph.
    @param i0 The input identifier.
    """
    try:
        v0 = g.node[i0]
    except KeyError as e:
        sys.stderr.write("Unknown identifier %s\n" % i0)
    accepted_paths = create_linked(g, (i0,), constraints)
    return set([p[-1] for p in accepted_paths])

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="Identity linking software")
    parser.add_argument("--graph_file", "-g", help="Input graph file with identities.")
    parser.add_argument("inputid", help="The input id (type: id).", default=None)
    parser.add_argument("--scope", "-s", type=int, choices = [1,2,3,4],
            help="The linking scope (1-4).", default=4)
    parser.add_argument("--time", "-t", type=TimeWrapper, help="Time for which to perform linkage (local TZ).")
    parser.add_argument("--max_inaccuracy", "-i", type=float, help="Maximal path inaccuracy.")
    return parser.parse_args()

def setup_constraints(args):
    scope_cs = {
            1: SpecificIdentifier,
            2: SpecificComputerOrInterface,
            3: SpecificUser,
            4: AllRelatedIndentifiers,
            }
    constraints = [scope_cs[args.scope](g)]

    if args.time != None:
        constraints.append(ActiveAtSpecificTime(g, args.time.get()))

    if args.max_inaccuracy != None:
        constraints.append(MaximalPathInaccuracy(g, args.max_inaccuracy))

    return constraints

# Main entry
if __name__ == "__main__":
    args = process_args()

    g = load_graph(args.graph_file)
    constraints = setup_constraints(args)

    if args.inputid:
        r = linked(g, args.inputid, constraints)
        l = list(r)
        l.sort()
        for i in l:
            print(i)
