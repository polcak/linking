# linking

Copyright (C) 2017 Libor Polčák <ipolcak@fit.vutbr.cz>

This is a README file for linking -- a tool for linking identities.

Usage
-----

<pre>
usage: linking.py [-h] [--graph_file GRAPH_FILE] [--scope {1,2,3,4,5,6}]
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
                        The linking scope (1-6):
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
  --begintime BEGINTIME, -b BEGINTIME
                        Begin time for which to perform linkage (local TZ).
  --endtime ENDTIME, -e ENDTIME
                        End time for which to perform linkage (local TZ).
  --timescope {1,2}, -t {1,2}
                        Time scope (1-2):
                        1~ All edges on the path have to be valid during
                           the whole period.
                        2~ All edges on the path have to be valid at
                           least once during the period [-b, -e] and
                           the period during the previous identifier
                           is valid on the path. 
  --max_inaccuracy MAX_INACCURACY, -i MAX_INACCURACY
                        Maximal path inaccuracy.
  --components, -c      Compute the number of components in the graph.
  --add_self, -a        Add the input node to the output set
</pre>

<pre>
usage: log2gml.py [-h] [--dhcp DHCP_LOG,YEAR,LEASE_PERIOD]
                  [--graph_file GRAPH_FILE] [--clf CLF_LOG,SERVER_FQDN]
                  output_graph_file

Log to GML graph convertor

positional arguments:
  output_graph_file     The Output graph file with identities.

optional arguments:
  -h, --help            show this help message and exit
  --dhcp DHCP_LOG,YEAR,LEASE_PERIOD, -d DHCP_LOG,YEAR,LEASE_PERIOD
                        ISC DHCP log file(s) and parameters:
                        file_name,year,lease_period(seconds).
  --graph_file GRAPH_FILE, -g GRAPH_FILE
                        Input graph file(s) in the GML format used by
                        linked.py.
  --clf CLF_LOG,SERVER_FQDN, -c CLF_LOG,SERVER_FQDN
                        Common/combined log format log file(s) used by HTTP(s)
                        servers, e.g. Apache, and the server FQDN.
</pre>

Note that log2gml.py supports multiple instances of --dhcp, --graph_file,
and --clf.

Conversion of log files to GML
------------------------------

The utility log2gml.py can convert log files to GML files compatible with
linking.py. So far ISC DHCP daemon and HTTP common/combined log format are
supported. Additionally, log2gml can merge multiple GML files into a single
GML file.

Feel free to develop additional convertors for different log file formats.

DHCP conversion example:

<pre>
./log2gml.py -d examples/log/dhcpd-anon.log,2017,7200 network.gml
</pre>

CLF conversion example based on files from Security Repo by Mike Sconzo
that is licensed under a Creative Commons Attribution 4.0 International
License:

<pre>
wget http://www.secrepo.com/self.logs/access.log.2017-01-01.gz
gunzip access.log.2017-01-01.gz
wget http://www.secrepo.com/self.logs/access.log.2017-01-02.gz
gunzip access.log.2017-01-02.gz
./log2gml.py -c access.log.2017-01-01,www.secrepo.com -c access.log.2017-01-02,www.secrepo.com secrepo.gml
</pre>

Merging:

<pre>
./log2gml.py -g network.gml -g secrepo.gml combined.gml
</pre>

Of course, you do not nedd to create the temporary GML files if you do not need them:

<pre>
./log2gml.py -d examples/log/dhcpd-anon.log,2017,7200 -c access.log.2017-01-01,www.secrepo.com -c access.log.2017-01-02,www.secrepo.com combined.gml
</pre>

Subsequently, you can use linking.py, for example, as follows:

<pre>
./linking.py -g combined.gml "URL: www.secrepo.com/self.logs/access.log.2015-02-13.gz"
IPv4: 163.172.64.187
IPv4: 163.172.66.68
IPv4: 46.229.168.69
URL: www.secrepo.com/self.logs/access.log.2015-02-23.gz
URL: www.secrepo.com/self.logs/access.log.2015-03-29.gz
URL: www.secrepo.com/self.logs/access.log.2015-04-21.gz
URL: www.secrepo.com/self.logs/access.log.2015-09-03.gz
URL: www.secrepo.com/self.logs/access.log.2015-09-06.gz
URL: www.secrepo.com/self.logs/access.log.2015-09-21.gz
URL: www.secrepo.com/self.logs/access.log.2015-09-24.gz
URL: www.secrepo.com/self.logs/access.log.2015-12-02.gz
URL: www.secrepo.com/self.logs/access.log.2015-12-08.gz
URL: www.secrepo.com/self.logs/access.log.2016-02-20.gz
URL: www.secrepo.com/self.logs/access.log.2016-03-22.gz
URL: www.secrepo.com/self.logs/access.log.2016-04-03.gz
URL: www.secrepo.com/self.logs/access.log.2016-04-10.gz
URL: www.secrepo.com/self.logs/access.log.2016-04-23.gz
URL: www.secrepo.com/self.logs/access.log.2016-05-10.gz
URL: www.secrepo.com/self.logs/access.log.2016-06-15.gz
URL: www.secrepo.com/self.logs/access.log.2016-07-05.gz
URL: www.secrepo.com/self.logs/access.log.2016-08-22.gz
URL: www.secrepo.com/self.logs/access.log.2016-09-11.gz
URL: www.secrepo.com/self.logs/access.log.2016-09-14.gz
URL: www.secrepo.com/self.logs/error.log.2015-01-25.gz
URL: www.secrepo.com/self.logs/error.log.2015-01-31.gz
URL: www.secrepo.com/self.logs/error.log.2015-03-28.gz
URL: www.secrepo.com/self.logs/error.log.2015-03-29.gz
URL: www.secrepo.com/self.logs/error.log.2015-05-17.gz
URL: www.secrepo.com/self.logs/error.log.2015-05-23.gz
URL: www.secrepo.com/self.logs/error.log.2015-06-05.gz
URL: www.secrepo.com/self.logs/error.log.2015-08-21.gz
URL: www.secrepo.com/self.logs/error.log.2015-08-31.gz
URL: www.secrepo.com/self.logs/error.log.2015-09-24.gz
URL: www.secrepo.com/self.logs/error.log.2015-11-04.gz
URL: www.secrepo.com/self.logs/error.log.2016-02-04.gz
URL: www.secrepo.com/self.logs/error.log.2016-03-29.gz
URL: www.secrepo.com/self.logs/error.log.2016-05-05.gz
URL: www.secrepo.com/self.logs/error.log.2016-05-13.gz
URL: www.secrepo.com/self.logs/error.log.2016-06-16.gz
URL: www.secrepo.com/self.logs/error.log.2016-08-02.gz
URL: www.secrepo.com/self.logs/error.log.2016-08-31.gz
URL: www.secrepo.com/self.logs/error.log.2016-11-05.gz
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
