"""Functions to get and parse meetup events from the web"""

import os
import logging
import datetime

from requests_html import HTMLSession


logger = logging.getLogger(__name__)


def get_events():
    """Get events from meetup website, parse them and return a list of dicts"""

    group = os.environ['MEETUP_GROUP']
    url = f'https://www.meetup.com/{group}/events/'
    resp = HTMLSession().get(url, timeout=10)
    if not resp.ok:
        raise ConnectionError(
            f"Received http {resp.status_code} when connecting to {url}"
        )
    events = resp.html.find('.flex.flex--column.flex--spaceBetween')

    events = [parse_event(event) for event in events]
    return events


def parse_event(event_html):
    """Parse each event card and returns a dict"""

    event = {}

    # date
    aux = event_html.xpath('.//time/@datetime')[0][:-3]
    aux = int(aux)
    event['date'] = datetime.datetime.fromtimestamp(aux)

    # title
    event['title'] = event_html.xpath('.//a/text()')[0]

    # description
    aux = event_html.xpath(
        './/p[contains(@class, "text--small")]/text()'
    )
    aux = [text for text in aux if len(text) > 1]
    event['description'] = '\n'.join(aux)

    # url
    event['url'] = event_html.url + \
        event_html.xpath('.//a/@href')[0].split('/')[-2] + '/'

    # address
    event['location'] = event_html.xpath('.//address//text()')[0]

    logger.debug(f'Event:\n{event}')

    return event
