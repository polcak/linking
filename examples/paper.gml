graph [
    comment "This is an example graph inspired by a graph in the paper"
    directed 0
    multigraph 1
    node [
        id 1
        label "RadiusLogin: JohnDoe"
        category "delta"
    ]
    node [
        id 2
        label "MAC: aa:bb:cc:00:11:22"
        category "gamma"
    ]
    node [
        id 3
        label "IPv4: 10.0.0.1"
        category "beta"
    ]
    edge [
        source 1
        target 2
        identitysource "RADIUS log"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 2
        target 3
        identitysource "RADIUS log"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]
    edge [
        source 1
        target 3
        identitysource "RADIUS log"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 0
    ]



    node [
        id 4
        label "IPv6: 2001:db8::/64"
        category "beta"
    ]
    edge [
        source 2
        target 4
        identitysource "DHCPv6 log"
        validfrom 1483268460
        validto 1483270260
        inaccuracy 0
    ]
]
