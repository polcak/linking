#!/usr/bin/env python3
# log2gml.py: Converts log files to GML graph
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

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="Log to GML graph convertor")
    parser.add_argument("--graph_file", "-g", help="Output graph file with identities.")
    parser.add_argument("--dhcp", "-d", action='append', default=[])
    return parser.parse_args()

# Main entry
if __name__ == "__main__":
    args = process_args()

    g = nx.MultiGraph()

    for d in args.dhcp:
        pass

    nx.write_gml(g, args.graph_file)
