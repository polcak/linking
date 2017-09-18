# linking

Copyright (C) 2017 Libor Polčák <ipolcak@fit.vutbr.cz>

This is a README file for linking -- a tool for linking identities.

Usage
-----

<pre>
linking.py [-h] [--graph_file GRAPH_FILE] [--scope {1,2,3,4,5,6}]
                  [--begintime BEGINTIME] [--endtime ENDTIME]
                  [--timescope {1,2}] [--max_inaccuracy MAX_INACCURACY]
                  [--components] [--add_self]
                  inputid

Identity linking software

positional arguments:
  inputid               The input id (type: id).

optional arguments:
  -h, --help            show this help message and exit
  --graph_file GRAPH_FILE, -g GRAPH_FILE
                        Input graph file with identities.
  --scope {1,2,3,4,5,6}, -s {1,2,3,4,5,6}
                        The linking scope (1-6): 1~ Constraints revealing
                        components of partial identity aka Other corresponding
                        identifiers 2~ Constraints revealing partial
                        identities of specific computer aka Identifiers of a
                        specific computer 3~ Constraints revealing partial
                        identities of computers where specific user
                        authenticated or logged in 4~ Constraints revealing
                        identifiers of all users accessing specific resource
                        5~ Constraints revealing all user accounts logged in
                        or authenticated from computer or set of computers 6~
                        Constraints revealing all accessed resources
  --begintime BEGINTIME, -b BEGINTIME
                        Begin time for which to perform linkage (local TZ).
  --endtime ENDTIME, -e ENDTIME
                        End time for which to perform linkage (local TZ).
  --timescope {1,2}, -t {1,2}
                        Time scope (1-2): 1~ All edges on the path have to be
                        valid during the whole period. 2~ All edges on the
                        path have to be valid at least once during the period
                        [-b, -e] and the period during the previous identifier
                        is valid on the path.
  --max_inaccuracy MAX_INACCURACY, -i MAX_INACCURACY
                        Maximal path inaccuracy.
  --components, -c      Compute the number of components in the graph.
  --add_self, -a        Add the input node to the output set
</pre>



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



Query examples
--------------

For some query examples, have a look to the examples/test.sh file.


Required libraries
------------------

 * NetworkX - https://networkx.github.io/
 * dateutil - http://labix.org/python-dateutil


Project history
---------------

TBD
