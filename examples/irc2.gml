graph [
    comment "This is an example graph based on B.2 in the Ph.D. thesis (second example)"
    directed 0
    multigraph 1
    node [
        id 1
        label "IPv4: 192.168.1.1"
        category "beta"
    ]
    node [
        id 2
        label "TCP: 192.168.1.1:1122 <-> 172.16.1.7:7000"
        category "alpha"
    ]
    node [
        id 3
        label "IRC nickname: Alice"
        category "lambda"
    ]

    edge [
        source 1
        target 2
        identitysource "IRC parser"
        validfrom 0
        validto 2
        inaccuracy 0
    ]
    edge [
        source 1
        target 3
        identitysource "IRC parser"
        validfrom 0
        validto 2
        inaccuracy 0
    ]
    edge [
        source 2
        target 3
        identitysource "IRC parser"
        validfrom 0
        validto 2
        inaccuracy 0
    ]



    node [
        id 4
        label "IRC channel: foo"
        category "rho"
    ]

    edge [
        source 1
        target 4
        identitysource "IRC parser"
        validfrom 1
        validto 2
        inaccuracy 0
    ]
    edge [
        source 2
        target 4
        identitysource "IRC parser"
        validfrom 1
        validto 2
        inaccuracy 0
    ]
    edge [
        source 3
        target 4
        identitysource "IRC parser"
        validfrom 1
        validto 2
        inaccuracy 0
    ]



    node [
        id 5
        label "IPv4: 10.0.0.1"
        category "beta"
    ]
    node [
        id 6
        label "TCP: 10.0.0.1:1234 <-> 172.16.1.7:7000"
        category "alpha"
    ]

    edge [
        source 5
        target 6
        identitysource "IRC parser"
        validfrom 3
        validto 5
        inaccuracy 0
    ]
    edge [
        source 5
        target 3
        identitysource "IRC parser"
        validfrom 3
        validto 5
        inaccuracy 0
    ]
    edge [
        source 6
        target 3
        identitysource "IRC parser"
        validfrom 3
        validto 5
        inaccuracy 0
    ]



    node [
        id 7
        label "IRC channel: moo"
        category "rho"
    ]

    edge [
        source 5
        target 7
        identitysource "IRC parser"
        validfrom 4
        validto 5
        inaccuracy 0
    ]
    edge [
        source 6
        target 7
        identitysource "IRC parser"
        validfrom 4
        validto 5
        inaccuracy 0
    ]
    edge [
        source 3
        target 7
        identitysource "IRC parser"
        validfrom 4
        validto 5
        inaccuracy 0
    ]
]
