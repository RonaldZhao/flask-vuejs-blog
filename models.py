import json
import uuid
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

PROFILE_FILE = os.path.join(os.path.dirname(__file__), 'profile.json')


class User(UserMixin):
    def get_id(self):
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return str(uuid.uuid4())

    def __init__(self, username, password):
        self.username = username
        self.id = self.get_id()
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
                print(type(profiles))
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash, self.id]
            f.write(json.dumps(profiles))

    def get_password_hash(self):
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def verify_password(self, password):
        if self.get_password_hash() is None:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name, profile[0])
        except IOError:
            return None
        except ValueError:
            return None
        return None
