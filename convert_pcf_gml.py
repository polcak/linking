#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as etree
from collections import namedtuple
SkewInfo = namedtuple("SkewInfo", ["IP", "absfrom", "absto", "skew"])

K = (1/3300)
Q = 2 - 3600*K

def process_xml(root):
    ips = set()
    skews = set()
    connections = []
    for computer in root:
        ip = computer.find("ip").text
        skewsx = computer.find("skews")
        if not skewsx:
            continue
        ips.add(ip)
        for se in skewsx:
            sd = se.attrib
            value = float(sd["value"]) * 1000
            absfrom = float(sd["absfrom"])
            absto = float(sd["absto"])
            if -1 < value < 1:
                continue # ignore computers that are probably running NTP
            uncertainty = 1/(K*(absto-absfrom)+Q)
            skew = (value, uncertainty)
            skews.add(skew)
            connections.append(SkewInfo(ip, absfrom, absto, skew))
    return ips, skews, connections

def create_gml(root, outfile, comment=""):
    ips, skews, connections = process_xml(root)
    with open(outfile, "w") as f:
        f.writelines([
            "graph [\n",
            '    comment "%s"\n' % comment,
            "    directed 0\n",
            "    multigraph 1\n",
        ])
        for ip in ips:
            f.writelines([
                "    node [\n",
                "        id %d\n" % hash(ip),
                '        label "IP %s"\n' % ip,
                '        category "beta"\n',
                "    ]\n",
            ])
        for skew in skews:
            f.writelines([
                "    node [\n",
                "        id %d\n" % hash(skew),
                '        label "Skew %f +- %f"\n' % skew,
                '        category "gamma"\n',
                "    ]\n",
            ])
        for c in connections:
            ip, absfrom, absto, skew = c
            value, uncertainty = skew
            minskew = value - uncertainty
            maxskew = value + uncertainty
            for s in skews:
                sval, suncert = s
                smin = sval - suncert
                smax = sval + suncert
                istart = max(minskew, smin)
                iend = min(maxskew, smax)
                if istart <= iend:
                    inaccuracy = (0.5 + uncertainty) / ((min(maxskew, iend) - max(minskew, istart)) / (maxskew-minskew))
                    f.writelines([
                        "    edge [\n",
                        "        source %d\n" % hash(ip),
                        "        target %d\n" % hash(s),
                        '        identitysource "PCF"\n',
                        '        validfrom %d\n' % absfrom,
                        '        validto %d\n' % absto,
                        '        inaccuracy %f\n' % inaccuracy,
                        "    ]\n",
                    ])

        f.write("]\n")

def parse_xml(filename):
    tree = etree.parse(filename)
    return tree

# Argument handling
def process_args():
    parser = argparse.ArgumentParser(description="This program converts PCF active.xml into an GML graph compatible with the input of linking.py")
    parser.add_argument("active", help="Input active.xml.")
    parser.add_argument("graph_file", help="Output graph file with identities.")
    return parser.parse_args()


# Main entry
if __name__ == "__main__":
    args = process_args()

    xml = parse_xml(args.active)
    create_gml(xml.getroot(), args.graph_file, "Graph genereated from PCF file %s" % args.active)
