from pyphenorm.afep.afep import extract_mml_from_json


def test_extract_from_json():
    json_item = {
        'matchedtext': 'novel coronavirus',
        'negated': False,
        'evlist': [
            {
                'score': 0,
                'matchedtext': 'novel coronavirus',
                'pos': 'JJ',
                'start': 10,
                'length': 17,
                'id': 'ev0',
                'conceptinfo': {
                    'conceptstring': 'Novel Coronavirus',
                    'sources': [
                        'MTH',
                        'LNC',
                        'MSH',
                        'NCI',
                        'SNOMEDCT_US'
                    ],
                    'cui': 'C5203676',
                    'preferredname': 'SARS-CoV-2',
                    'semantictypes': [
                        'virs'
                    ]
                }
            }
        ],
        'docid': 'Medscape_COVID-19.txt',
        'start': 10,
        'length': 17,
        'id': 'en0'
    }
    results = list(extract_mml_from_json([json_item]))
    assert len(results) == 1
    result = results[0]
    assert result['matchedtext'] == 'novel coronavirus'
    assert result['cui'] == 'C5203676'
    assert result['preferredname'] == 'SARS-CoV-2'
    assert result['conceptstring'] == 'Novel Coronavirus'
    assert result['virs'] == 1
    assert result['MTH'] == 1
    assert result['LNC'] == 1
    assert result['MSH'] == 1
    assert result['NCI'] == 1
    assert result['SNOMEDCT_US'] == 1
