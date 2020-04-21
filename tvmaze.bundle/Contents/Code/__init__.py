#!/usr/bin/python

import timeit
from datetime import datetime

from tvmazepy import tvmaze


SUPPORTED_LANGUAGES = [
    'ab', 'sq', 'ar', 'hy', 'az', 'bg', 'zh', 'cs', 'da', 'nl', 'en', 'et',
    'fi', 'fr', 'ka', 'de', 'ga', 'he', 'hi', 'hr', 'hu', 'is', 'it', 'ja',
    'ko', 'no', 'fa', 'pl', 'pt', 'ro', 'ru', 'sr', 'es', 'sv', 'tl', 'th',
    'tr', 'uk', 'ur', 'cy'
]


def Start():
    Log.Debug('Starting TVmaze agent...')


def time_taken(start, end):
    return '{:0.3f}'.format(end-start)


class TVmazeAgent(Agent.TV_Shows):
    name = "TVmaze"
    languages = SUPPORTED_LANGUAGES
    primary_provider = True

    def search(self, results, media, lang, manual):
        start = timeit.default_timer()
        Log.Info('Searching for matches with TVmaze agent for {}'.format(media.show))
        # Retrieve list of shows that match the given name.
        shows = tvmaze.search_show(media.show)

        Log.Info('Found {} shows that match "{}"'.format(len(shows), media.show))
        scores = [show.score for show in shows]
        for show in shows:
            # Retrieve language of the show
            locale = Locale.Language.Match(show.language) if show.language is not None else lang

            # Scale the scores so the best match has a score of 100.
            scaled_score = int(99 * (show.score - min(scores)) / (max(scores) - min(scores)) + 1) if len(shows) > 1 else 100

            # Add the show to the return list
            show_year = show.premiere_date.year if show.premiere_date else None
            results.Append(MetadataSearchResult(
                id=str(show.id),
                name=show.name,
                year=show_year,
                score=scaled_score,
                lang=locale,
            ))
            Log.Info('Added result MetadataSearchResult(id="{}", name="{}", score="{}", year="{}", lang="{}")'.format(
                show.id,
                show.name,
                scaled_score,
                show_year,
                locale,
            ))
        end = timeit.default_timer()
        Log.Info('Search completed with {} matches in {} seconds'.format(len(shows), time_taken(start, end)))

    def update(self, metadata, media, lang, force):
        start = timeit.default_timer()
        Log.Info('Updating metadata for {}'.format(metadata.id))
        show = tvmaze.get_show(metadata.id, populated=True)
        if show is None:
            return

        # Update main show details
        metadata.title = show.name
        metadata.summary = show.summary
        metadata.originally_available_at = show.premiere_date
        metadata.duration = show.num_episodes
        metadata.rating = show.rating.get('average')
        metadata.content_rating = None
        metadata.genres = show.genres
        if show.network is not None:
            metadata.studio = show.network.get('name')
        elif show.streaming_service is not None:
            metadata.studio = show.streaming_service.get('name')
        else:
            metadata.studio = None
        metadata.countries = []
        Log.Info('Updated main show details')

        # Update show poster
        if show.images is not None and show.images.get('original') is not None:
            show_poster_url = show.images.get('original')
            if show_poster_url not in metadata.posters:
                metadata.posters[show_poster_url] = Proxy.Media(HTTP.Request(show_poster_url).content)
        Log.Info('Updated show poster')

        # Update show cast
        metadata.roles.clear()
        for character in show.cast:
            role_metadata = metadata.roles.new()
            role_metadata.role = character.name
            role_metadata.name = character.person.name
            # Prefer character photo over talent photo
            if character.images is not None and character.images.get('original') is not None:
                role_metadata.photo = character.images.get('original')
            elif character.person.images is not None and character.person.images.get('original') is not None:
                role_metadata.photo = character.person.images.get('original')
        Log.Info('Updated cast')

        # Episode 1 index for calculating the absolute index of each episode
        episode_base_index = show.seasons[1].episodes[1].id

        # Update season and its episode details
        for season in show.seasons.values():
            season_metadata = metadata.seasons[season.number]

            # Update main season details
            season_metadata.summary = season.summary

            # Update season poster
            if season.images is not None and season.images.get('original') is not None:
                season_poster_url = season.images.get('original')
                if season_poster_url not in season_metadata.posters:
                    season_metadata.posters[season_poster_url] = Proxy.Media(HTTP.Request(season_poster_url).content)
            # Fallback to show poster
            elif show.images is not None:
                Log.Info('Fallback to show poster for season {}'.format(season.number))
                if show_poster_url not in season_metadata.posters:
                    season_metadata.posters[show_poster_url] = Proxy.Media(HTTP.Request(show_poster_url).content)
            Log.Info('Updated poster for season {}'.format(season.number))

            # Update episode details
            for episode in season.episodes.values():
                episode_metadata = metadata.seasons[episode.season].episodes[episode.number]

                # Update main episode details
                episode_metadata.title = episode.name
                episode_metadata.summary = episode.summary
                episode_metadata.originally_available_at = episode.airdate
                episode_metadata.rating = None
                episode_metadata.duration = episode.duration
                episode_metadata.absolute_index = episode.id - episode_base_index
                Log.Info('Updated info for S{}E{} {}'.format(episode.season, episode.number, episode.name))

                # Update episode thumbnail
                if episode.images is not None and episode.images.get('medium') is not None:
                    episode_thumbnail_url = episode.images.get('medium')
                    if episode_thumbnail_url not in episode_metadata.thumbs:
                        episode_metadata.thumbs[episode_thumbnail_url] = Proxy.Media(HTTP.Request(episode_thumbnail_url).content)
                Log.Info('Updated thumbnail for S{}E{} {}'.format(episode.season, episode.number, episode.name))
            Log.Info('Updated info for season {}'.format(season.number))
        end = timeit.default_timer()
        Log.Info('Metadata update completed in {} seconds'.format(time_taken(start, end)))
