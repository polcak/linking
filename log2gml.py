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
import itertools
import networkx as nx
import re
import sys
import time
import time_wrapper

isc_dhcp_line_regex = re.compile(R"([A-Za-z]+) ([0-9]+) ([0-9]{2}:[0-9]{2}:[0-9]{2}) [a-zA-Z0-9]+ dhcpd: DHCP(ACK|RELEASE) (?:on|of) (\d+\.\d+\.\d+\.\d+) (?:from|to) ([a-fA-F0-9:]+)")

clf_line_regex = re.compile(R'([^ \t]+) [^ \t]+ ([^ \t]+) \[([^]]+)\] "[A-Z]+ ([^ \t]+) HTTP/[0-9]\.[0-9]" ([0-9]+)')

def add_node_ip(g, addr):
    """ Add the IP address addr to the graph g."""
    ip = "IPv4: %s" % addr
    g.add_node(ip, category = "beta")
    return ip

def add_node_mac(g, addr):
    """ Add the MAC address addr to the graph g."""
    mac = "MAC: %s" % addr
    g.add_node(mac, category = "gamma")
    return mac

def add_node_http_user(g, username):
    """ Adds the HTTP user username to the graph g."""
    user = "HTTP user: %s" % username
    g.add_node(user, category = "lambda")
    return user

def add_node_url(g, url):
    """ Adds the URL url to the graph g."""
    url_node = "URL: %s" % url
    g.add_node(url_node, category = "rho")
    return url_node

def add_edge(g, source, destination, identitysource, validfrom, validto, inaccuracy):
    """ Adds an edge (source, destination) to the graph g.

    Prolongs the validity of an existing edge if available.
    """
    try:
        edges = g.edge[source][destination]
    except Exception as e:
        edges = {}
    for e in edges.values():
        if e["identitysource"] == identitysource and \
                e["inaccuracy"] == inaccuracy:
            if e["validto"] > validfrom > e["validfrom"]:
                e["validto"] = validto
                return # The edge is prolonged
            if validfrom < e["validfrom"] < validto:
                e["validfrom"] = validfrom
                e["validto"] = validto
                return # The edge starts earlier and validto is updated
    # This is a new edge
    g.add_edge(source, destination, identitysource = identitysource,
            validfrom = validfrom, validto = validto,
            inaccuracy = inaccuracy)

def add_edges(g, nodes, identitysource, validfrom, validto, inaccuracy):
    """ Adds an edge between all nodes to the graph g.

    Prolongs the validity of an existing edge if available.
    """
    for source, destination in itertools.combinations(nodes, 2):
        add_edge(g, source, destination, identitysource, validfrom, validto,
                inaccuracy)

def stop_edge(g, source, destination, identitysource, time, inaccuracy):
    """ Stops ongoing edge at time t.

    For now, it is sufficient to call add_edge.
    """
    add_edge(g, source, destination, identitysource, time, time, inaccuracy)

def make_isc_dhcp_time(match, year):
    """ Create Unix timestamp for the ISC DHCP message.

    @match - The match object for isc_dhcp_line_regex.
    @year - The year of the log file.
    """
    month = time_wrapper.months[match.group(1)]
    day = int(match.group(2))
    this_month = int(time.strftime("%m"))
    this_day = int(time.strftime("%d"))
    t = time.mktime(time.strptime("%d.%d.%d %s" %
            (day, month, year, match.group(3)), "%d.%m.%Y %H:%M:%S"))
    return t

def parse_isc_dhcp_log(g, log_file, year, lease_period):
    """ ISC DHCP log parser. """
    with open(log_file, "r") as f:
        for line in f:
            match = isc_dhcp_line_regex.search(line)
            if match:
                try:
                    msg = match.group(4)
                    if msg == "ACK":
                        t = make_isc_dhcp_time(match, year)
                        ip = add_node_ip(g, match.group(5))
                        mac = add_node_mac(g, match.group(6))
                        add_edge(g, ip, mac, identitysource = log_file,
                                validfrom = t, validto = t+lease_period, inaccuracy = 0)
                    elif msg == "RELEASE":
                        t = make_isc_dhcp_time(match, year)
                        ip = add_node_ip(g, match.group(5))
                        mac = add_node_mac(g, match.group(6))
                        stop_edge(g, ip, mac, identitysource = log_file,
                                time = t, inaccuracy = 0)
                except Exception as e:
                    sys.stderr.write("Cannot parse line %s: %s" % (str(e), line)) # Note that newline is already in the line

def parse_clf_log(g, log_file_name, fqdn):
    """ Parses Common/combined log format used by HTTP(s) servers. """
    with open(log_file_name, "r") as f:
        for line in f:
            match = clf_line_regex.search(line)
            if match:
                nodes = []
                nodes.append(add_node_ip(g, match.group(1)))
                user = match.group(2)
                if user != "-":
                    nodes.append(add_node_http_user(g, user))
                t = time_wrapper.TimeWrapper(match.group(3)).get()
                nodes.append(add_node_url(g, fqdn + match.group(4)))
                add_edges(g, nodes, identitysource = log_file_name,
                        validfrom = t, validto = t, inaccuracy = 0)

def merge_multigraphs(g1, g2):
    """ Merge MultiGraph g2 into MultiGraph g1.

    Inspired by nx.compose with several modifications:

    * g1 is updated instead of creation of a new graph.
    * Multiple edges are preserved, see https://github.com/networkx/networkx/pull/2101 and linked
    issues.
    """
    for n, attribs in g2.node.items():
        g1.add_node(n, **attribs)
    for src, dst, _, attribs_new in g2.edges_iter(keys=True, data=True):
        already_known = False
        if dst in g1[src]:
            for attribs_checked in g1[src][dst].values():
                if attribs_checked == attribs_new:
                    already_known = True
                    break
        if not already_known:
            g1.add_edge(src, dst, **attribs_new)

def merge_gml_file(g, file_name):
    """ Merge the current graph and the graph in the given GML file."""
    g2 = nx.read_gml(file_name)
    merge_multigraphs(g, g2)

def parse_isc_dhcp_arg(s):
    """ Parses the ISC DHCP arguments and returns a tuple """
    f, year, lease_period = s.split(",")
    year = int(year)
    lease_period = int(lease_period)
    return (f, year, lease_period)

def parse_clf_arg(s):
    """ Parses the common/combined log format arguments and returns a tuple """
    f, fqdn = s.split(",")
    return (f, fqdn)

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="Log to GML graph convertor")
    parser.add_argument("output_graph_file", help="The Output graph file with identities.", default=None)
    parser.add_argument("--dhcp", "-d", action='append', default=[],
            help = "ISC DHCP log file(s) and parameters: file_name,year,lease_period(seconds).",
            type = parse_isc_dhcp_arg, metavar = "DHCP_LOG,YEAR,LEASE_PERIOD")
    parser.add_argument("--graph_file", "-g", action='append', default=[],
            help="Input graph file(s) in the GML format used by linked.py.")
    parser.add_argument("--clf", "-c", action='append', default=[],
            help="Common/combined log format log file(s) used by HTTP(s) servers, e.g. Apache, and the server FQDN.",
            type = parse_clf_arg, metavar = "CLF_LOG,SERVER_FQDN")
    return parser.parse_args()

# Main entry
if __name__ == "__main__":
    args = process_args()

    g = nx.MultiGraph()

    for f in args.graph_file:
        merge_gml_file(g, f)

    for d in args.dhcp:
        parse_isc_dhcp_log(g, *d)

    for f, fqdn in args.clf:
        parse_clf_log(g, f, fqdn)

    nx.write_gml(g, args.output_graph_file)
