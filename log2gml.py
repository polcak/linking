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
import re
import sys
import time

isc_dhcp_line_regex = re.compile(R"([A-Za-z]+) ([0-9]+) ([0-9]{2}:[0-9]{2}:[0-9]{2}) [a-zA-Z0-9]+ dhcpd: (DHCP[A-Z]+) (?:for|on) (\d+\.\d+\.\d+\.\d+) (?:from|to) ([a-fA-F0-9:]+)")
isc_dhcp_months = {
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

def parse_isc_dhcp_log(g, log_file, year, lease_period):
    """ ISC DHCP log parser. """
    with open(log_file, "r") as f:
        for line in f:
            match = isc_dhcp_line_regex.search(line)
            if match:
                try:
                    msg = match.group(4)
                    if msg == "DHCPACK":
                        month = isc_dhcp_months[match.group(1)]
                        day = int(match.group(2))
                        this_month = int(time.strftime("%m"))
                        this_day = int(time.strftime("%d"))
                        t = time.mktime(time.strptime("%d.%d.%d %s" %
                                (day, month, year, match.group(3)), "%d.%m.%Y %H:%M:%S"))
                        ip = "IPv4: %s" % match.group(5)
                        mac = "MAC: %s" % match.group(6)
                        g.add_node(ip, category = "beta")
                        g.add_node(mac, category = "gamma")
                        g.add_edge(ip, mac, identitysource = log_file,
                                validfrom = t, validto = t+lease_period, inaccuracy = 0)
                except Exception as e:
                    sys.stderr.write("Cannot parse line %s: %s" % (str(e), line)) # Note that newline is already in the line

def parse_isc_dhcp_arg(s):
    """ Parses the ISC DHCP arguments and returns a tuple """
    f, year, lease_period = s.split(",")
    year = int(year)
    lease_period = int(lease_period)
    return (f, year, lease_period)

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="Log to GML graph convertor")
    parser.add_argument("--graph_file", "-g", help="Output graph file with identities.")
    parser.add_argument("--dhcp", "-d", action='append', default=[],
            help = "ISC DHCP log file(s) and parameters: file_name,year,lease_period(seconds).",
            type = parse_isc_dhcp_arg, metavar = "DHCP_LOG,YEAR,LEASE_PERIOD")
    return parser.parse_args()

# Main entry
if __name__ == "__main__":
    args = process_args()

    g = nx.MultiGraph()

    for d in args.dhcp:
        parse_isc_dhcp_log(g, *d)

    nx.write_gml(g, args.graph_file)
