from __future__ import unicode_literals
import string
from datetime import datetime

from .. import utils
from .episode import Episode


class Season(object):
    def __init__(self, data, special=False):
        if not special:
            self.id = data.get('id')
            self.url = data.get('url')
            self.number = data.get('number')
            self.name = data.get('name')
            self.num_episodes = data.get('episodeOrder')
            self.episodes = {}
            self.premiere_date = datetime.strptime(data.get('premiereDate'), '%Y-%m-%d') if data.get('premiereDate') is not None else None
            self.end_date = data.get('endDate')
            self.network = data.get('network')
            self.streaming_service = data.get('webChannel')
            self.images = data.get('image')
            self.summary = utils.strip_tags(data.get('summary'))
            self.links = data.get('_links')

    def __str__(self):
        return string.capwords(' '.join(self.url.split('/')[-1].split('-')))
