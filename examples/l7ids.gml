graph [
    comment "This is a graph that implements the lambda-lambda extension in the NPU paper"
		directed 0
		multigraph 1
    node [
        id 1
        label "IPv4: 10.0.0.1"
        category "beta"
    ]
    node [
        id 2
        label "e-mail: alice@example.com"
        category "lambda"
    ]
    node [
        id 3
        label "receiver e-mail: alice@example.com"
        category "rho"
    ]
    node [
        id 4
        label "IRC nickname: Alice"
        category "lambda"
    ]
    node [
        id 5
        label "IRC channel: foo"
        category "rho"
    ]

    edge [
        source 1
        target 2
        identitysource "SMTP log"
        validfrom 10
        validto 10
        inaccuracy 0
    ]

    edge [
        source 2
        target 3
        identitysource "SMTP log"
        validfrom 10
        validto 10
        inaccuracy 0
    ]

    edge [
        source 1
        target 4
        identitysource "Chat log"
        validfrom 1
        validto 1000
        inaccuracy 0
    ]

    edge [
        source 4
        target 5
        identitysource "Chat log"
        validfrom 2
        validto 1000
        inaccuracy 0
    ]

    edge [
        source 2
        target 4
        identitysource "Common knowledge"
        validfrom 0
        validto 1000000
        inaccuracy 1
    ]
]
