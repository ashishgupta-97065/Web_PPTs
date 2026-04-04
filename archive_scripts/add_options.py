import json
with open('template_deck.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
slides = data if isinstance(data, list) else data.get('slides', [])
options = {
    'themes': ['dark', 'light', 'teal'],
    'tagColors': ['default', 'teal', 'grn', 'amb', 'blu', 'red'],
    'stepColors': ['default', 'red', 'grn', 'amb'],
    'cardThemes': ['dark', 'light'],
    'gridTypes': ['grid3', 'grid4', 'grid2'],
    'templates': {
        'Hero': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'content': ['string (paragraphs)']
        },
        'Process': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'steps': [{
                'number': 'string/number',
                'color': 'enum (stepColors)',
                'heading': 'string',
                'text': ['string (paragraphs)'],
                'details': [{
                    'title': 'string',
                    'tags': ['string (badges/tags)'],
                    'text': 'string (description)'
                }]
            }]
        },
        'GridCards': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'grids': [{
                'type': 'enum (gridTypes)',
                'cards': [{
                    'theme': 'enum (cardThemes)',
                    'heading': 'string',
                    'text': ['string (paragraphs)']
                }]
            }]
        },
        'BeforeAfter': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'comparisons': [{
                'before': {
                    'heading': 'string',
                    'text': 'string'
                },
                'after': {
                    'heading': 'string',
                    'text': 'string'
                }
            }]
        },
        'Timeline': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'timeline': [{
                'heading': 'string',
                'duration': 'string',
                'text': 'string'
            }]
        },
        'TableLayout': {
            'theme': 'enum (themes)',
            'header': {
                'tag': 'string',
                'tagColor': 'enum (tagColors)',
                'title': 'string',
                'subtitle': 'string (optional)'
            },
            'table': {
                'headers': ['string'],
                'rows': [['string (columns)']]
            },
            'grid': [['string (large stat)', 'string (desc)']]
        }
    }
}
new_data = {'options': options, 'slides': slides}
with open('template_deck.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2)
print('JSON updated.')
