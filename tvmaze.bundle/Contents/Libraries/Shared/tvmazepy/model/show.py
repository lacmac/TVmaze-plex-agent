from __future__ import absolute_import, unicode_literals

from .. import utils
from .season import Season
from .episode import Episode
from .person import Crew, Character


class Show(object):
    def __init__(self, data):
        self.score = data['score'] if 'score' in data else 100
        show = data['show'] if 'show' in data else data
        self.id = show['id']
        self.name = show['name']
        self.url = show['url']
        self.type = show['type']
        self.lang = show['language']
        self.genres = show['genres']
        self.status = show['status']
        self.num_episodes = show['runtime']
        self.seasons = {}
        self._episode_list = []
        self.specials = {}
        self.cast = []
        self.crew = []
        self._handle_embedded(data['_embedded']) if '_embedded' in data else None
        self.premiere_date = show['premiered']  # datetime?
        self.official_site = show['officialSite']
        self.schedule = show['schedule']
        self.rating = show['rating']
        self.weight = show['weight']
        self.network = show['network']
        self.streaming_service = show['webChannel']
        self.external_ids = show['externals']
        self.images = show['image']
        self.summary = utils.strip_tags(show['summary'])
        self.links = show['_links']

    def _handle_embedded(self, embedded):
        special_num = 1
        if 'seasons' in embedded:
            seasons = [Season(season) for season in embedded['seasons']]
            for season in seasons:
                self.seasons[season.number] = season

        if 'seasons' in embedded and 'episodes' in embedded:
            episodes = [Episode(episode) for episode in embedded['episodes']]
            for episode in episodes:
                if not episode.special:
                    self.seasons[episode.season].episodes[episode.number] = episode
                else:
                    episode.season = 0
                    episode.number = special_num
                    special_num += 1
                    self.specials[episode.id] = episode

        if 'seasons' not in embedded and 'episodes' in embedded:
            episodes = [Episode(episode) for episode in embedded['episodes']]
            for episode in episodes:
                if not episode.special:
                    self._episode_list.append(episode)
                else:
                    episode.season = 0
                    episode.number = special_num
                    special_num += 1
                    self.specials[episode.id] = episode

        self.cast = [Character(c['character'], c['person']) for c in embedded['cast']] if 'cast' in embedded else []
        self.crew = [Crew(c) for c in embedded['crew']] if 'crew' in embedded else []

    def __str__(self):
        return str(self.id) + ': ' + self.name


class Alias:
    def __init__(self, data):
        self.name = data['name']
        if data['country'] is not None:
            self.country = data['country']
        else:
            self.country = {}
            self.country['name'] = 'Original Country'
            self.country['code'] = 'OG'
            self.country['timezome'] = 'Original Country Timezone'

    def __str__(self):
        return self.country['name'] + ': ' + self.name
