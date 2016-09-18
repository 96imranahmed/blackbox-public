
class User():
    def __init__(self):
        self.likes = []
        self.dislikes = []
        self.date = Date()
        self.target = Target()
        self.user_id = '0'
    def enjoys(self, thing):
        if thing in self.dislikes:
            self.dislikes.remove(thing)
        self.likes.append(thing)
    def hates(self, thing):
        if thing in self.likes:
            self.likes.remove(thing)
        self.dislikes.append(thing)
    def does_user_enjoy(self, thing):
        if thing in self.likes:
            return 2
        elif thing in self.dislikes:
            return 0
        else:
            return 1
    def set_target(self, name):
        self.target = Target(name)
    def get_target(self):
        return self.target
    def set_date(self, date):
        self.date = date
    def get_date(self):
        return self.date
    def set_user(self, user_id):
        self.user_id = user_id
    def get_user(self):
        return self.user_id

class Target():
    def __init__(self, name=None):
        self.name = name
        self.likes = []
        self.dislikes = []
    def has_name(self):
        if self.name is None: return False
        else: return True
    def get_name(self):
        return self.name
    def enjoys(self, thing):
        if thing in self.dislikes:
            self.dislikes.remove(thing)
        self.likes.append(thing)
    def hates(self, thing):
        if thing in self.likes:
            self.likes.remove(thing)
        self.dislikes.append(thing)
    def does_user_enjoy(self, thing):
        if thing in self.likes:
            return 2
        elif thing in self.dislikes:
            return 0
        else:
            return 1

class Date():
    def __init__(self, location=None, time=None, type_of_date=None):
        self.location = location
        self.time = time
        self.type_of_date = type_of_date
    def get_location(self):
        return self.location
    def get_time(self):
        return self.time
    def get_type(self):
        return self.type_of_date

x = User()
x.set_target("Mary")
date = Date("here", "2", "food")
x.set_date(date)
print(x.get_date().get_location())
print(x.get_target().get_name())
