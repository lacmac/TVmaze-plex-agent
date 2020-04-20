#!/usr/bin/python

from tvmazepy import tvmaze


SUPPORTED_LANGUAGES = [
    'ab', 'sq', 'ar', 'hy', 'az', 'bg', 'zh', 'cs', 'da', 'nl', 'en', 'et',
    'fi', 'fr', 'ka', 'de', 'ga', 'he', 'hi', 'hr', 'hu', 'is', 'it', 'ja',
    'ko', 'no', 'fa', 'pl', 'pt', 'ro', 'ru', 'sr', 'es', 'sv', 'tl', 'th',
    'tr', 'uk', 'ur', 'cy'
]


def Start():
    Log.Debug('Starting TVmaze agent...')


class TVmazeAgent(Agent.TV_Shows):
    name = "TVmaze"
    languages = SUPPORTED_LANGUAGES
    primary_provider = True

    def search(self, results, media, lang, manual):
        Log.Info('Searching for matches with TVmaze agent: ' + media.show)
        # Retrieve list of shows that match the given name.
        shows = tvmaze.search_show(media.show)

        Log.Info('Found {} shows that match {}'.format(len(shows), media.show))
        scores = [show.score for show in shows]
        for show in shows:
            # Retrieve language of the show
            locale = Locale.Language.Match(show.language) if show.language is None else lang

            # Scale the scores so the best match has a score of 100.
            scale = (show.score - min(scores)) / (max(scores) - min(scores))
            scaled_score = int(99 * scale + 1) if len(shows) > 1 else 100

            # Add the show to the return list
            results.Append(MetadataSearchResult(
                id=str(show.id),
                name=show.name,
                year=int(show.premiere_date[:4]) if show.premiere_date is not None else None,
                score=scaled_score,
                lang=locale,
            ))
            Log.Debug('Added result MetadataSearchResult(id="{}", name="{}", score="{}", year="{}", lang="{}")'.format(
                str(show.id),
                show.name,
                str(scaled_score),
                show.premiere_date[:4] if show.premiere_date is not None else '',
                locale,
            ))

    def update(self, metadata, media, lang, force):
        pass
