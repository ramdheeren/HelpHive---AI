from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, phone, password, first_name, last_name, is_volunteer, skills, radius, days, location):
        self.email = email
        self.phone = phone
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_volunteer = is_volunteer
        
        self.skills = skills
        self.radius = radius
        self.days = days
        self.location = location