#!/usr/bin/python

from tvmazepy import tvmaze


SUPPORTED_LANGUAGES = [
    'ab', 'sq', 'ar', 'hy', 'az', 'bg', 'zh', 'cs', 'da', 'nl', 'en', 'et',
    'fi', 'fr', 'ka', 'de', 'ga', 'he', 'hi', 'hr', 'hu', 'is', 'it', 'ja',
    'ko', 'no', 'fa', 'pl', 'pt', 'ro', 'ru', 'sr', 'es', 'sv', 'tl', 'th',
    'tr', 'uk', 'ur', 'cy']


def Start():
    Log.Debug('Starting TVmaze agent...')


class TVmazeAgent(Agent.TV_Shows):
    name = "TVmaze"
    languages = SUPPORTED_LANGUAGES
    primary_provider = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        pass

    def update(self, metadata, media, lang, force):
        pass
