import firebase_admin
from firebase_admin import credentials, db

from datetime import datetime

cred = credentials.Certificate('firebase-sa-secret.json')
default_app = firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://jump-awake.firebaseio.com'
})

DB = db.reference('/users')

JUMPS_KEY = 'jumps'
LIFETIME_JUMP_KEY = 'lifetime_jumps'
ALARM_KEY = 'alarm'

class User():
    def __init__(self, user_id):
        # Create user if doesn't exist
        if not DB.child(user_id).get():
            DB.child(user_id).set({
                JUMPS_KEY: 0,
                LIFETIME_JUMP_KEY: 0
            })
        self.id = user_id

    def increment_jump(self):
        new_jumps = self.jumps + 1
        self.__jumps_node.set(new_jumps)
        return new_jumps

    def end_jump_session(self):
        self.__lifetime_jumps_node.set(self.lifetime_jumps + self.jumps)
        self.__jumps_node.set(0)

    def set_alarm(self, timestamp):
        return DB.child('{}/{}'.format(self.id, ALARM_KEY)).set(timestamp)

    @property
    def seconds_until_alarm(self):
        alarm = datetime.strptime(self.data['alarm'], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.utcnow()
        dt = alarm - now
        return dt.total_seconds()

    @property
    def data(self):
        return DB.child(self.id).get()

    @property
    def jumps(self):
        return int(self.__jumps_node.get())

    @property
    def lifetime_jumps(self):
        return int(self.__lifetime_jumps_node.get())

    @property
    def __lifetime_jumps_node(self):
        return DB.child('{}/{}'.format(self.id, LIFETIME_JUMP_KEY))

    @property
    def __jumps_node(self):
        return DB.child('{}/{}'.format(self.id, JUMPS_KEY))
