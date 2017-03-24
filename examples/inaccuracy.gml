graph [
    comment "This is an example graph based on B.3 in the Ph.D. thesis"
    directed 0
    multigraph 1
    node [
        id 1
        label "Clock skew: 23.7 +- 0.5 ppm"
        category "gamma"
    ]
    node [
        id 2
        label "Clock skew: 23.9 +- 0.8 ppm"
        category "gamma"
    ]
    node [
        id 3
        label "Clock skew: 25.3 +- 1.0 ppm"
        category "gamma"
    ]
    node [
        id 4
        label "Clock skew: -10.7 +- 0.5 ppm"
        category "gamma"
    ]
    node [
        id 5
        label "IPv6: 2001:db8::1"
        category "beta"
    ]
    node [
        id 6
        label "IPv6: 2001:db8::2"
        category "beta"
    ]
    node [
        id 7
        label "IPv6: 2001:db8::3"
        category "beta"
    ]
    node [
        id 8
        label "IPv6: 2001:db8::4"
        category "beta"
    ]

    edge [
        source 1
        target 5
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1
    ]
    edge [
        source 1
        target 6
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1.6
    ]
    edge [
        source 2
        target 5
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1.6
    ]
    edge [
        source 2
        target 6
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1
    ]
    edge [
        source 2
        target 7
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 8
    ]
    edge [
        source 3
        target 6
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 8
    ]
    edge [
        source 3
        target 7
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1
    ]
    edge [
        source 4
        target 8
        identitysource "pcf"
        validfrom 1483268459
        validto 1483272059
        inaccuracy 1
    ]
]
