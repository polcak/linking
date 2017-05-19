graph [
    comment "This is an example graph based on CGN example in the Ph.D. thesis"
    directed 0
    multigraph 1
    node [
        id 1
        label "IPv4: 10.0.0.2"
        category "beta"
    ]
    node [
        id 2
        label "IPv4: 100.64.0.1"
        category "beta"
    ]
    node [
        id 3
        label "IPv4: 1.2.3.4"
        category "beta"
    ]

    node [
        id 4
        label "TCP: 10.0.0.2:1234 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    node [
        id 5
        label "TCP: 100.64.0.1:1234 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    node [
        id 6
        label "TCP: 1.2.3.4:1234 <-> 147.229.1.1:5060"
        category "alpha"
    ]

    node [
        id 10
        label "SIP account: Alice"
        category "lambda"
    ]

    edge [
        source 1
        target 4
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 2
        target 5
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 3
        target 6
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 4
        target 5
        identitysource "NAT"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 5
        target 6
        identitysource "CGN"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 1
        target 10
        identitysource "NAT rule 8.4.5 1."
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 4
        target 10
        identitysource "NAT rule 8.4.5 2. (c)"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 5
        target 10
        identitysource "NAT rule 8.4.5 2. (c)"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    edge [
        source 6
        target 10
        identitysource "NAT rule 8.4.5 2. (c)"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]

    node [
        id 7
        label "IPv4: 1.2.3.5"
        category "beta"
    ]
    node [
        id 11
        label "TCP: 10.0.0.2:5678 <-> 195.113.1.1:80"
        category "alpha"
    ]
    node [
        id 12
        label "TCP: 100.64.0.1:5678 <-> 195.113.1.1:80"
        category "alpha"
    ]
    node [
        id 13
        label "TCP: 1.2.3.4:5678 <-> 195.113.1.1:80"
        category "alpha"
    ]

    edge [
        source 1
        target 11
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268461
        validto 1483268491
        inaccuracy 0
    ]
    edge [
        source 2
        target 12
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268461
        validto 1483268491
        inaccuracy 0
    ]
    edge [
        source 7
        target 13
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268461
        validto 1483268491
        inaccuracy 0
    ]
    edge [
        source 11
        target 12
        identitysource "NAT"
        validfrom 1483268461
        validto 1483268491
        inaccuracy 0
    ]
    edge [
        source 12
        target 13
        identitysource "CGN"
        validfrom 1483268461
        validto 1483268491
        inaccuracy 0
    ]


    node [
        id 8
        label "IPv4: 100.64.0.2"
        category "beta"
    ]
    node [
        id 9
        label "SIP account: Bob"
        category "lambda"
    ]
     node [
        id 14
        label "TCP: 100.64.0.2:2222 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    node [
        id 15
        label "TCP: 1.2.3.4:2222 <-> 147.229.1.1:5060"
        category "alpha"
    ]
    edge [
        source 8
        target 14
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]
    edge [
        source 3
        target 15
        identitysource "Automatic edge between IP address and its flow"
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]
    edge [
        source 14
        target 15
        identitysource "CGN"
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]

    edge [
        source 8
        target 9
        identitysource "NAT rule 8.4.5 1."
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]
    edge [
        source 9
        target 14
        identitysource "NAT rule 8.4.5 2. (c)"
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]
    edge [
        source 9
        target 15
        identitysource "NAT rule 8.4.5 2. (c)"
        validfrom 1483268461
        validto 1483269573
        inaccuracy 0
    ]


]
