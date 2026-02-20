from datetime import datetime

import requests

import superscript


def get_today_data(use_new_cal: bool=True) -> dict:
    cal = 'gregorian' if use_new_cal else 'julian'
    today = datetime.today()
    api_url = f'https://orthocal.info/api/{cal}/{today.year}/{today.month}/{today.day}/'
    response = requests.get(api_url)

    if response.ok:
        return response.json()
    else:
        raise RuntimeError(f'API returned {response.status_code}')


def get_post_contents(data: dict) -> dict:
    # dict entries: day, feasts, commemorations, readings
    post_contents = {}

    ## day header
    pretty_date = datetime.today().strftime(f'%b. {datetime.today().day}, %Y')
    day_title = '; '.join(title for title in data['titles'])
    post_contents['day'] = f'# {pretty_date} - {day_title}'

    # feasts
    if data['feasts']:
        feasts_header = '## Feasts'
        feasts = '\n'.join(feast for feast in data['feasts'])
        post_contents['feasts'] = f'{feasts_header}\n{feasts}'
    else:
        post_contents['feasts'] = None

    # commemorations
    if data['saints']:
        commemoration_header = '## Commemorations'
        saints = '\n'.join(story['title'] for story in data['stories'])
        post_contents['commemorations'] = f'{commemoration_header}\n{saints}'
    else:
        post_contents['commemorations'] = None

    # readings
    post_contents['readings'] = derive_readings(data['readings'])

    return post_contents


def derive_readings(data: dict) -> dict:
    readings = {}
    summary_header = '## Today\'s Readings'
    summary_list = '\n'.join(entry['display'] for entry in data)
    readings['summary'] = f'{summary_header}\n{summary_list}'
    passages = []
    readings['passages'] = passages

    for entry in data:
        current_chapter = 0
        heading = entry['display']
        passage = {}
        verses = []
        passages.append(passage)
        passage['heading'] = f'## {heading}\n'
        passage['verses'] = verses

        for verse in entry['passage']:
            current_verse = '\n>\t' if verse['paragraph_start'] else ''
            is_new_chapter = verse['chapter'] != current_chapter
            current_chapter = verse['chapter'] if is_new_chapter else current_chapter
            verse_sup = get_verse_number(current_chapter, verse['verse'], include_chapter=is_new_chapter)
            current_verse += f'{verse_sup}{verse["content"]}'
            verses.append(current_verse)


    return readings


def get_verse_number(chapter: int, verse: int, include_chapter: bool=False) -> str:
    chapter_sup = f'{superscript.convert_num_to_super(chapter)}\u207B' if include_chapter else ''
    verse_sup = superscript.convert_num_to_super(verse)

    return f'{chapter_sup}{verse_sup}'



if __name__ == '__main__':
    new_cal = get_today_data()
    old_cal = get_today_data(use_new_cal=False)
    print(get_post_contents(old_cal))
    print('***********************************************************************************')
    print(get_post_contents(new_cal))
