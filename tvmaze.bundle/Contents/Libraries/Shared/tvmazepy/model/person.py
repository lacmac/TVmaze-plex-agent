class Person:
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


class Character:
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
        return f'{self.name}: {str(self.person)}'


class Crew(Person):
    def __init__(self, data):
        super().__init__(data['person'])
        self.job = data['type']

    def __str__(self):
        return f'{self.job}: {super().__str__()}'
