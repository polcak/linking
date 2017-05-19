graph [
    comment "This is an example graph based on B.4 in the Ph.D. thesis"
    directed 0
    multigraph 1
    node [
        id 1
        label "IPv4: 10.0.0.2"
        category "beta"
    ]
    node [
        id 2
        label "TCP: 10.0.0.2:11223 <-> 11.12.13.14:80"
        category "alpha"
    ]
    node [
        id 3
        label "TCP: 1.2.3.4:11223 <-> 11.12.13.14:80"
        category "alpha"
    ]
    node [
        id 4
        label "IPv4: 10.0.0.1"
        category "beta"
    ]
    node [
        id 5
        label "TCP: 10.0.0.1:1234 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    node [
        id 6
        label "TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    node [
        id 7
        label "IPv4: 1.2.3.4"
        category "beta"
    ]
    node [
        id 8
        label "UDP: 10.0.0.1:5678 <-> 5.6.7.8:2233"
        category "alpha"
    ]
    node [
        id 9
        label "UDP: 1.2.3.4:5678 <-> 5.6.7.8:2233"
        category "alpha"
    ]
    node [
        id 10
        label "SIP account: Alice"
        category "lambda"
    ]

    edge [
        source 1
        target 2
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 2
        target 3
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 3
        target 7
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 4
        target 5
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 4
        target 8
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 5
        target 6
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 8
        target 9
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 6
        target 7
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 7
        target 9
        identitysource "NAT tracking"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 6
        target 10
        identitysource "SIP traffic monitor"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 9
        target 10
        identitysource "SIP traffic monitor"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 4
        target 10
        identitysource "NAT rule 8.5.5 1."
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 5
        target 10
        identitysource "NAT rule 8.5.5 2. (c)"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 8
        target 10
        identitysource "NAT rule 8.5.5 2. (c)"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
]
