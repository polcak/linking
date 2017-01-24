# linking

Copyright (C) 2017 Libor Polčák <ipolcak@fit.vutbr.cz>

This is a README file for linking -- a tool for linking identities.

Usage
-----

linking.py [-h] [--graph_file GRAPH_FILE] [--scope {1,2,3,4}]
                  [--time TIME] [--max_inaccuracy MAX_INACCURACY]
                  inputid

Identity linking software

positional arguments:
  inputid               The input id (type: id).

optional arguments:
  -h, --help            show this help message and exit
  --graph_file GRAPH_FILE, -g GRAPH_FILE
                        Input graph file with identities.
  --scope {1,2,3,4}, -s {1,2,3,4}
                        The linking scope (1-4).
  --time TIME, -t TIME  Time for which to perform linkage (local TZ).
  --max_inaccuracy MAX_INACCURACY, -i MAX_INACCURACY
                        Maximal path inaccuracy.



Getting GML data from PCF
-------------------------

Use convert_pcf_gml.py.

usage: convert_pcf_gml.py [-h] active graph_file

This program converts PCF active.xml into an GML graph compatible with the
input of linking.py

positional arguments:
  active      Input active.xml.
  graph_file  Output graph file with identities.

optional arguments:
  -h, --help  show this help message and exit


Project history
---------------

TBD
