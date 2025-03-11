from enum import Enum


class CertificateAuthority(Enum):
    """Certificate authorities enumeration"""

    ACTALIS = [
        [
            "Actalis EU Qualified Certificates CA G1  ",
            "f3 73 b3 87 06 5a 28 84 8a f2 f3 4a ce 19 2b dd c7 8e 9c ac",
        ],
        [
            "Actalis Qualified Certificates CA G1  ",
            "76 59 4a 51 3e 85 18 2b ef e8 7f 23 4e a5 76 4d d9 d2 a8 ad",
        ],
        [
            "Actalis Server Authentication Root CA  ",
            "36 08 4e ec 1e d7 3b b4 c9 d6 8e fd 13 a8 17 22 e8 27 7d 5f",
        ],
        [
            "CA Qualificata BNL erogata da Actalis  ",
            "27 05 f5 a7 7d 32 66 26 d9 bc 28 0f 91 7d d4 2a b2 14 55 c5",
        ],
    ]

    ADD_TRUST = [
        [
            "AddTrust External CA Root ",
            "02 fa f3 e2 91 43 54 68 60 78 57 69 4d f5 e4 5b 68 85 18 68",
        ]
    ]

    CERTUM = [
        [
            "Certum Certification Authority (Root)",
            "62 52 dc 40 f7 11 43 a2 2f de 9e f7 34 8e 06 42 51 b1 81 18",
        ],
        [
            "Certum Trusted Network CA  ",
            "07 e0 32 e0 20 b7 2c 3f 19 2f 06 28 a2 59 3a 19 a7 0f 06 9e",
        ],
    ]

    COMODO = [
        [
            "Comodo RSA Certification Authority  ",
            "af e5 d2 44 a8 d1 19 42 30 ff 47 9f e2 f8 97 bb cd 7a 8c b4",
        ]
    ]

    DIGICERT = [
        [
            " DigiCert Global Root CA  ",
            "a8 98 5d 3a 65 e5 e5 c4 b2 d7 d6 6d 40 c6 dd 2f b1 9c 54 36",
        ],
        [
            "DigiCert Global Root G2  ",
            "df 3c 24 f9 bf d6 66 76 1b 26 80 73 fe 06 d1 cc 8d 4f 82 a4",
        ],
        ["DigiCert Global Root G3", "7e 04 de 89 6a 3e 66 6d 00 e6 87 d3 3f fa d9 3b e8 3d 34 9e"],
        [
            "DigiCert High Assurance EV Root CA",
            "5f b7 ee 06 33 e2 59 db ad 0c 4c 9a e6 d3 8f 1a 61 c7 dc 25",
        ],
        ["DigiCert Trusted Root G4", "dd fb 16 cd 49 31 c9 73 a2 03 7d 3f c8 3a 4d 7d 77 5d 05 e4"],
    ]

    ENTRUST = [
        [
            "Entrust Root Certification Authority",
            "b3 1e b1 b7 40 e3 6c 84 02 da dc 37 d4 4d f5 d4 67 49 52 f9",
        ],
        [
            "Entrust Root Certification Authority - G2  ",
            "8c f4 27 fd 79 0c 3a d1 66 06 8d e8 1e 57 ef bb 93 22 72 d4",
        ],
        [
            "Entrust Root Certification Authority - G3  ",
            "ae 85 69 d9 4f 4a b1 c4 64 ad 9b 7c fd 78 40 b0 e3 9d af 66",
        ],
    ]

    GEOTRUST = [
        ["GeoTrust Global CA", "de 28 f4 a4 ff e5 b9 2f a3 c5 03 d1 a3 49 a7 f9 96 2a 82 12"],
        [
            "GeoTrust Primary Certification Authority  ",
            "32 3c 11 8e 1b f7 b8 b6 52 54 e2 e2 10 0d d6 02 90 37 f0 96",
        ],
        [
            "GeoTrust Primary Certification Authority - G2  ",
            "8d 17 84 d5 37 f3 03 7d ec 70 fe 57 8b 51 9a 99 e6 10 d7 b0",
        ],
        ["GeoTrust Universal CA ", "e6 21 f3 35 43 79 05 9a 4b 68 30 9d 8a 2f 74 22 15 87 ec 79"],
        [
            "GeoTrust Universal CA 2  ",
            "37 9a 19 7b 41 85 45 35 0c a6 03 69 f3 3c 2e af 47 4f 20 79",
        ],
    ]

    GLOBALSIGN = [
        ["GlobalSign Root CA", "b1 bc 96 8b d4 f4 9d 62 2a a8 9a 81 f2 15 01 52 a4 1d 82 9c"],
        ["GlobalSign Root CA - R2", "75 e0 ab b6 13 85 12 27 1c 04 f8 5f dd de 38 e4 b7 24 2e fe"],
        ["GlobalSign Root CA - R3", "d6 9b 56 11 48 f0 1c 77 c5 45 78 c1 09 26 df 5b 85 69 76 ad"],
    ]

    GODADDY = [
        [
            "GoDaddy Class 2 Certification Authority Root Certificate ",
            "27 96 ba e6 3f 18 01 e2 77 26 1b a0 d7 77 70 02 8f 20 ee e4",
        ],
        [
            "GoDaddy Class 2 Certification Authority Root Certificate – G2  ",
            "47 be ab c9 22 ea e8 0e 78 78 34 62 a7 9f 45 c2 54 fd e6 8b",
        ],
    ]

    QUOVADIS = [
        [
            "QuoVadis Limited Root CA 2 G3",
            "09 3C 61 F3 8B 8B DC 7D 55 DF 75 38 02 05 00 E1 25 F5 C8 36",
        ]
    ]

    SECURETRUST = [
        ["SecureTrust CA", "87 82 c6 c3 04 35 3b cf d2 96 92 d2 59 3e 7d 44 d9 34 ff 11"]
    ]

    USERTRUST_SECTIGO = [
        [
            "USERTrust RSA Certification Authority",
            "2b 8f 1b 57 33 0d bb a2 d0 7a 6c 51 f7 0e e9 0d da b9 ad 8e",
        ]
    ]

    VERISIGN = [
        [
            "Class 1 Public Primary Certification Authority  ",
            "90 ae a2 69 85 ff 14 80 4c 43 49 52 ec e9 60 84 77 af 55 6f",
        ],
        [
            "Class 1 Public Primary Certification Authority - G2  ",
            "27 3e e1 24 57 fd c4 f9 0c 55 e8 2b 56 16 7f 62 f5 32 e5 47",
        ],
        [
            "Class 2 Public Primary Certification Authority ",
            "67 82 aa e0 ed ee e2 1a 58 39 d3 c0 cd 14 68 0a 4f 60 14 2a",
        ],
        [
            "Class 2 Public Primary Certification Authority - G2",
            "b3 ea c4 47 76 c9 c8 1c ea f2 9d 95 b6 cc a0 08 1b 67 ec 9d",
        ],
        [
            "Class 3 Public Primary Certification Authority",
            "a1 db 63 93 91 6f 17 e4 18 55 09 40 04 15 c7 02 40 b0 ae 6b",
        ],
        [
            "Class 4 Public Primary Certification Authority - G2",
            "0b 77 be bb cb 7a a2 47 05 de cc 0f bd 6a 02 fc 7a bd 9b 52",
        ],
        [
            "VeriSign Class 1 Public Primary Certification Authority - G3 ",
            "20 42 85 dc f7 eb 76 41 95 57 8e 13 6b d4 b7 d1 e9 8e 46 a5",
        ],
        [
            "VeriSign Class 2 Public Primary Certification Authority - G3  ",
            "61 ef 43 d7 7f ca d4 61 51 bc 98 e0 c3 59 12 af 9f eb 63 11",
        ],
        [
            "VeriSign Class 3 Public Primary Certification Authority - G4 ",
            "22 d5 d8 df 8f 02 31 d1 8d f7 9d b7 cf 8a 2d 64 c9 3f 6c 3a",
        ],
        [
            "VeriSign Class 3 Public Primary Certification Authority - G5  ",
            "4e b6 d5 78 49 9b 1c cf 5f 58 1e ad 56 be 3d 9b 67 44 a5 e5",
        ],
        [
            "VeriSign Class 4 Public Primary Certification Authority - G3  ",
            "c8 ec 8c 87 92 69 cb 4b ab 39 e9 8d 7e 57 67 f3 14 95 73 9d",
        ],
        [
            "VeriSign Universal Root Certification Authority",
            "36 79 ca 35 66 87 72 30 4d 30 a5 fb 87 3b 0f a7 7b b7 0d 54",
        ],
    ]
