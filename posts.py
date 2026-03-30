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
        current_message += passage['heading']
        for verse in passage['verses']:
            if len(current_message) + len(verse) > 2000:
                messages.append(current_message)
                current_message = '> '

            current_message += verse

        if len(current_message) > 0:
            messages.append(current_message)
            current_message = ''

    return messages
