from __future__ import absolute_import, print_function
from datetime import datetime

import requests
from dateutil import parser

from . import endpoints
from .model.show import Show, Alias
from .model.episode import Episode
from .model.season import Season
from .model.person import Character, Person, Crew
from .model.embed import Embed


class TVmaze(object):
    def _query_api(self, url, params=None):
        res = requests.get(url, params)
        print(res.url)
        if res.status_code != requests.codes.OK:
            print('Page request was unsuccessful: ' + res.status_code, res.reason)
            return None
        return res.json()

    def search_show(self, show_name):
        res = self._query_api(endpoints.search_show_name, {'q': show_name})
        return [Show(show) for show in res] if res is not None else []

    def search_show_best_match(self, show_name, embed=None):
        embed = Embed(embed)
        res = self._query_api(endpoints.search_show_best_match, {'q': show_name, embed.key: embed.value})
        return Show(res) if res is not None else None

    def get_show_external(self, imdb_id=None, tvdb_id=None, tvrage_id=None):
        if len(list(filter(None, [imdb_id, tvdb_id, tvrage_id]))) == 0:
            return None
        if imdb_id is not None:
            return self._get_show_external_id('imdb', imdb_id)
        if tvdb_id is not None:
            return self._get_show_external_id('thetvdb', tvdb_id)
        if tvrage_id is not None:
            return self._get_show_external_id('tvrage', tvrage_id)

    def _get_show_external_id(self, external_name, external_id):
        res = self._query_api(endpoints.search_external_show_id, {external_name: external_id})
        return Show(res) if res is not None else None

    def get_show(self, tvmaze_id, populated=False, embed=None):
        embed = Embed(embed) if not populated else Embed(['seasons', 'cast', 'crew'])
        res = self._query_api(endpoints.show_information.format(str(tvmaze_id)), {embed.key: embed.value})
        if populated:
            episodes = [episode for episode in self._get_show_episode_list_raw(tvmaze_id, specials=True)]
            res['_embedded']['episodes'] = episodes
        return Show(res) if res is not None else None

    def get_show_episode_list(self, tvmaze_id, specials=False):
        specials = 1 if specials else None
        res = self._get_show_episode_list_raw(tvmaze_id, specials)
        return [Episode(episode) for episode in res] if res is not None else []

    def _get_show_episode_list_raw(self, tvmaze_id, specials):
        return self._query_api(endpoints.show_episode_list.format(str(tvmaze_id)), {'specials': specials})

    def get_show_specials(self, tvmaze_id):
        res = self._query_api(endpoints.show_episode_list.format(str(tvmaze_id)), {'specials': 1})
        specials = [Episode(episode) for episode in res if episode['number'] is None] if res is not None else []
        special_num = 1
        for special in specials:
            special.season = 0
            special.number = special_num
            special_num += 1
        return specials

    def get_show_episode(self, tvmaze_id, season, episode):
        res = self._query_api(endpoints.show_episode.format(str(tvmaze_id)), {'season': season, 'number': episode})
        return Episode(res) if res is not None else None

    def get_show_episodes_by_date(self, tvmaze_id, date_input):
        if type(date_input) is str:
            try:
                date = parser.parse(date_input)
            except parser._parser.ParserError:
                return []
        elif type(date_input) is datetime:
            date = date_input
        else:
            return []
        res = self._query_api(endpoints.show_episodes_on_date.format(str(tvmaze_id)), {'date': date.isoformat()[:10]})
        return [Episode(episode) for episode in res] if res is not None else []

    def get_show_season_list(self, tvmaze_id):
        res = self._query_api(endpoints.show_season_list.format(str(tvmaze_id)))
        return [Season(season) for season in res] if res is not None else []

    def get_season_episode_list(self, tvmaze_season_id):
        res = self._query_api(endpoints.season_episode_list.format(str(tvmaze_season_id)))
        # episode['number'] is None when it is classed as a special, for now don't include specials
        return [Episode(episode) for episode in res if episode['number'] is not None] if res is not None else []

    def get_show_aliases(self, tvmaze_id):
        res = self._query_api(endpoints.show_alias_list.format(str(tvmaze_id)))
        return [Alias(alias) for alias in res] if res is not None else []

    def get_episode_information(self, tvmaze_episode_id, embed=None):
        embed = Embed(embed)
        res = self._query_api(endpoints.episode_information.format(str(tvmaze_episode_id)), {embed.key: embed.value})
        return Episode(res) if res is not None else None

    def get_show_cast(self, tvmaze_id):
        res = self._query_api(endpoints.show_cast.format(str(tvmaze_id)))
        return [Character(cast['character'], cast['person']) for cast in res]

    def get_show_crew(self, tvmaze_id):
        res = self._query_api(endpoints.show_crew.format(str(tvmaze_id)))
        return [Crew(crew_member) for crew_member in res]
