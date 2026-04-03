import logging


log = logging.getLogger(__name__)


def create_messages(content: dict) -> list:
    messages = []
    log.debug(f'content: {content}')

    # initial day post
    header = content.get('day', '')
    feasts = content.get('feasts') if content.get('feasts') else ''
    commemorations = content.get('commemorations', '')
    readings_summary = content.get('readings', {}).get('summary', '')
    messages.append(f'{header}\n{feasts}\n{commemorations}\n{readings_summary}')

    # readings {summary: string, passages: [{heading: string, verses: [string]}]
    passages = content['readings']['passages']
    current_message = ''

    for passage in passages:
        fragments = fragment(passage['heading'], passage['verses'])
        messages.extend(fragments)

    return messages


def fragment(heading: str, verses: list) -> list:
    fragments = []
    full_reading = ' '.join(verses)
    tokens = full_reading.split(' ')
    current = heading

    for token in tokens:
        if len(current) + len(token) + 1 > 2000:
            fragments.append(current)
            current = f'> {token}'
        else:
            current += f' {token}'

    fragments.append(current)

    return fragments
