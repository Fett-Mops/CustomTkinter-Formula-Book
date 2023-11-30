dic = {
    "formula": {
        "Leistung": {
            "search_terms": [
                "Spannung",
                "Strom",
                "Wiederstand",
                "Elektrotechnick"
            ],
            "formula": [
                "U=I*R",
                [
                    "U",
                    "I",
                    "R"
                ]
            ],
            "values": [
                [
                    0,
                    3,
                    2
                ],
                [
                    1,
                    0,
                    0
                ]
            ],
            "information": "insert information",
            "category": "Elecktrotechinck"
        },
        "Uri": {
            "search_terms": [
                "Spannung",
                "Strom",
                "Wiederstand",
                "Elektrotechnick"
            ],
            "formula": [
                "U=I*R",
                "U,I,R"
            ],
            "values": [
                [
                    0,
                    1,
                    2
                ],
                [
                    0,
                    0,
                    0
                ]
            ],
            "information": "insert information",
            "category": "Elecktrotechinck"
        },
        "a": {
            "search_terms": [],
            "formula": [
                "",
                []
            ],
            "values": [
                [
                    37,
                    38,
                    39
                ],
                []
            ],
            "information": "insert info",
            "category": ""
        },
        "fdfsg": {
            "search_terms": [],
            "formula": [
                "",
                []
            ],
            "values": [
                [
                    49,
                    50,
                    51
                ],
                []
            ],
            "information": "insert info",
            "category": ""
        },
        "unnamed formula 1 2 3": {
            "search_terms": [],
            "formula": [
                "",
                []
            ],
            "values": [
                [
                    31,
                    32,
                    33
                ],
                []
            ],
            "information": "insert info",
            "category": ""
        }
    }
}


#print(dic['formula'])


sortednames=sorted(dic['formula'].keys(), key=lambda x:x.lower())
a ={}

for i in sortednames:
    d = []
    d = dic['formula'][i]
    a[i] = d
w={'formula':a}
print(w)

