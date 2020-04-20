from __future__ import unicode_literals


class Person(object):
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.name = data['name']
        self.country = data['country']
        self.birthday = data['birthday']
        self.deathday = data['deathday']
        self.gender = data['gender']
        self.image = data['image']
        self.links = data['_links']

    def __str__(self):
        return self.name


class Character(object):
    def __init__(self, data, person):
        self.id = data['id']
        self.url = data['url']
        self.name = data['name']
        self.image = data['image']
        self.links = data['_links']
        # self.self = data['self']
        # self.voice = data['voice']
        self.person = Person(person)

    def __str__(self):
        return self.name + ': ' + self.person


class Crew(Person):
    def __init__(self, data):
        super(Crew, self).__init__(data['person'])
        self.job = data['type']

    def __str__(self):
        return self.job + ': ' + str(super())
