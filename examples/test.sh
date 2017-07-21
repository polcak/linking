#!/usr/bin/env bash

TMPFILE=`mktemp`

echo "PPP_RADIUS: -s 1 RadiusLogin: JohnDoe"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 10.11.12.1
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:55 -e 2017-01-01T12:55"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:55 -e 2017-01-01T12:55 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 10.11.12.1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:10 -e 2017-01-01T12:55 -t 1"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:10 -e 2017-01-01T12:55 -t 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:10 -e 2017-01-01T12:55 -t 2"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:10 -e 2017-01-01T12:55 -t 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 10.11.12.1
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:10 -e 2017-01-01T12:10 -t 2"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:10 -e 2017-01-01T12:10 -t 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:30 -e 2017-01-01T12:30 -t 2"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:30 -e 2017-01-01T12:30 -t 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS:  -s 1 RadiusLogin: JohnDoe -b 2017-01-01T12:50 -e 2017-01-01T12:50 -t 2"
../linking.py -g ppp_radius.gml -s 1 "RadiusLogin: JohnDoe" -b 2017-01-01T12:50 -e 2017-01-01T12:50 -t 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 10.11.12.1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS: IPv4: 10.0.0.1 -s 1"
../linking.py -g ppp_radius.gml "IPv4: 10.0.0.1" -s 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
COMPARE

echo "PPP_RADIUS: IPv4: 10.0.0.1 -s 2"
../linking.py -g ppp_radius.gml "IPv4: 10.0.0.1" -s 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
COMPARE

echo "PPP_RADIUS: RadiusLogin: JohnDoe -s 3"
../linking.py -g ppp_radius.gml "RadiusLogin: JohnDoe" -s 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 10.11.12.1
IPv6: 2001:db8::1
MAC: aa:bb:cc:00:11:22
MAC: aa:bb:cc:55:66:77
COMPARE

echo "PPP_RADIUS: IPv4: 10.11.12.1 -s 5"
../linking.py -g ppp_radius.gml "IPv4: 10.11.12.1" -s 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
PPPLogin: JohnDoe
RadiusLogin: JohnDoe
COMPARE


echo "IRC: IRC nickname: Bob -s 3"
../linking.py -g irc.gml "IRC nickname: Bob" -s 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
TCP: 10.0.0.1:1234 <-> 172.16.1.7:7000
COMPARE


echo "IRC: IRC channel: foo -s 4"
../linking.py -g irc.gml "IRC channel: foo" -s 4 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC nickname: Alice
IRC nickname: Bob
COMPARE


echo "IRC: IPv4: 192.168.1.1 -s 5"
../linking.py -g irc.gml "IPv4: 192.168.1.1" -s 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC nickname: Alice
COMPARE


echo "IRC: IPv4: 192.168.1.1 -s 6"
../linking.py -g irc.gml "IPv4: 192.168.1.1" -s 6 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: foo
COMPARE


echo "IRC2: IPv4: 10.0.0.1 -s 1"
../linking.py -g irc2.gml "IPv4: 10.0.0.1" -s 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 10.0.0.1:1234 <-> 172.16.1.7:7000
COMPARE


echo "IRC2: IPv4: 10.0.0.1 -s 2"
../linking.py -g irc2.gml "IPv4: 10.0.0.1" -s 2 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 10.0.0.1:1234 <-> 172.16.1.7:7000
COMPARE


echo "IRC2: IRC nickname: Alice -s 3"
../linking.py -g irc2.gml "IRC nickname: Alice" -s 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
IPv4: 192.168.1.1
TCP: 10.0.0.1:1234 <-> 172.16.1.7:7000
TCP: 192.168.1.1:1122 <-> 172.16.1.7:7000
COMPARE


echo "IRC2: IRC channel: foo -s 4"
../linking.py -g irc2.gml "IRC channel: foo" -s 4 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC nickname: Alice
COMPARE


echo "IRC2: IPv4: 10.0.0.1 -s 5"
../linking.py -g irc2.gml "IPv4: 10.0.0.1" -s 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC nickname: Alice
COMPARE


echo "IRC2: IPv4: 10.0.0.1 -s 6"
../linking.py -g irc2.gml "IPv4: 10.0.0.1" -s 6 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: moo
COMPARE

echo "IRC2: IPv4: 10.0.0.1 -s 6 -b 5 -e 5"
../linking.py -g irc2.gml "IPv4: 10.0.0.1" -s 6 -b 5 -e 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: moo
COMPARE

echo "IRC2: IRC nickname: Alice -s 6 -b 1 -e 1"
../linking.py -g irc2.gml "IRC nickname: Alice" -s 6 -b 1 -e 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: foo
COMPARE

echo "IRC2: IRC nickname: Alice -s 6 -b 3 -e 3"
../linking.py -g irc2.gml "IRC nickname: Alice" -s 6 -b 3 -e 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
COMPARE

echo "IRC2: IRC nickname: Alice -s 6 -b 5 -e 5"
../linking.py -g irc2.gml "IRC nickname: Alice" -s 6 -b 5 -e 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: moo
COMPARE



echo "Inaccuracy: 5"
../linking.py -g inaccuracy.gml "IPv6: 2001:db8::1" -i 5 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
Clock skew: 23.7 +- 0.5 ppm
Clock skew: 23.9 +- 0.8 ppm
IPv6: 2001:db8::2
COMPARE


echo "Inaccuracy: 10"
../linking.py -g inaccuracy.gml "IPv6: 2001:db8::1" -i 10 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
Clock skew: 23.7 +- 0.5 ppm
Clock skew: 23.9 +- 0.8 ppm
IPv6: 2001:db8::2
IPv6: 2001:db8::3
COMPARE


echo "Inaccuracy: 11"
../linking.py -g inaccuracy.gml "IPv6: 2001:db8::1" -i 11 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
Clock skew: 23.7 +- 0.5 ppm
Clock skew: 23.9 +- 0.8 ppm
Clock skew: 25.3 +- 1.0 ppm
IPv6: 2001:db8::2
IPv6: 2001:db8::3
COMPARE


echo "NAT: broken"
../linking.py -g nat_broken.gml "SIP account: Alice" -s 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 1.2.3.4
TCP: 1.2.3.4:11223 <-> 11.12.13.14:80
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.1:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:11223 <-> 11.12.13.14:80
UDP: 1.2.3.4:5678 <-> 5.6.7.8:2233
UDP: 10.0.0.1:5678 <-> 5.6.7.8:2233
COMPARE


echo "NAT: fixed"
../linking.py -g nat_fixed.gml "SIP account: Alice" -s 3 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.1
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.1:1234 <-> 147.229.1.1:5060
UDP: 1.2.3.4:5678 <-> 5.6.7.8:2233
UDP: 10.0.0.1:5678 <-> 5.6.7.8:2233
COMPARE


echo "NAT: IPv4: 1.2.3.4 (translator)"
../linking.py -g nat_fixed.gml "IPv4: 1.2.3.4" -s 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 1.2.3.4:11223 <-> 11.12.13.14:80
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.1:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:11223 <-> 11.12.13.14:80
UDP: 1.2.3.4:5678 <-> 5.6.7.8:2233
UDP: 10.0.0.1:5678 <-> 5.6.7.8:2233
COMPARE

echo "CGN -s 1 10.0.0.2"
../linking.py -g cgn.gml -s 1 "IPv4: 10.0.0.2" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 1.2.3.5:5678 <-> 195.113.1.1:80
TCP: 10.0.0.2:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:5678 <-> 195.113.1.1:80
TCP: 100.64.0.1:1234 <-> 147.229.1.1:5060
TCP: 100.64.0.1:5678 <-> 195.113.1.1:80
COMPARE

echo "CGN -s 2 10.0.0.2"
../linking.py -g cgn.gml -s 2 "IPv4: 10.0.0.2" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 1.2.3.5:5678 <-> 195.113.1.1:80
TCP: 10.0.0.2:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:5678 <-> 195.113.1.1:80
TCP: 100.64.0.1:1234 <-> 147.229.1.1:5060
TCP: 100.64.0.1:5678 <-> 195.113.1.1:80
COMPARE

echo "CGN -s 5 10.0.0.2"
../linking.py -g cgn.gml -s 5 "IPv4: 10.0.0.2" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
SIP account: Alice
COMPARE

echo "CGN -s 1 Alice"
../linking.py -g cgn.gml -s 1 "SIP account: Alice" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:1234 <-> 147.229.1.1:5060
TCP: 100.64.0.1:1234 <-> 147.229.1.1:5060
COMPARE

echo "CGN -s 3 Alice"
../linking.py -g cgn.gml -s 3 "SIP account: Alice" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 10.0.0.2
TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060
TCP: 1.2.3.5:5678 <-> 195.113.1.1:80
TCP: 10.0.0.2:1234 <-> 147.229.1.1:5060
TCP: 10.0.0.2:5678 <-> 195.113.1.1:80
TCP: 100.64.0.1:1234 <-> 147.229.1.1:5060
TCP: 100.64.0.1:5678 <-> 195.113.1.1:80
COMPARE

echo "CGN -s 3 Bob"
../linking.py -g cgn.gml -s 3 "SIP account: Bob" > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IPv4: 100.64.0.2
TCP: 1.2.3.4:2222 <-> 147.229.1.1:5060
TCP: 100.64.0.2:2222 <-> 147.229.1.1:5060
COMPARE

echo "L7 names aliases active - resources"
../linking.py -g l7ids.gml -s 6 "IRC nickname: Alice" -i 1 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: foo
receiver e-mail: alice@example.com
COMPARE

echo "L7 names aliases deactivated - resources"
../linking.py -g l7ids.gml -s 6 "IRC nickname: Alice" -i 0 > "$TMPFILE"

diff "$TMPFILE" - <<- COMPARE
IRC channel: foo
COMPARE


rm "$TMPFILE"
