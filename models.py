import firebase_admin
from firebase_admin import credentials, db

from dateutil.parser import *
from datetime import datetime, timedelta

cred = credentials.Certificate('firebase-sa-secret.json')
default_app = firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://jump-awake.firebaseio.com'
})

DB = db.reference('/users')
TIME_SERIES = db.reference('/time_series')

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

        jump_data = self.data
        TIME_SERIES.push().set({
            'user': self.id,
            'timestamp': datetime.now().isoformat(),
            'current_jumps': jump_data['jumps'],
            'lifetime_jumps': jump_data['lifetime_jumps']
        })

        return new_jumps

    def end_jump_session(self):
        self.__lifetime_jumps_node.set(self.lifetime_jumps + self.jumps)
        self.__jumps_node.set(0)

    def set_alarm(self, timestamp):
        print('[SET ALARM]' + self.id)
        return DB.child('{}/{}'.format(self.id, ALARM_KEY)).set(timestamp)

    @property
    def seconds_until_alarm(self):
        alarm = self.__get_datetime(self.data['alarm'])
        now = datetime.utcnow()
        dt = alarm - now
        # Give 30 second delay for camera to warm up
        return (dt - timedelta(seconds=30)).total_seconds()

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


    def __get_datetime(self, iso_string):
        try:
            return datetime.strptime(self.data['alarm'], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            return datetime.strptime(self.data['alarm'], '%Y-%m-%dT%H:%M:%S.000Z')

def fmt_time_series(ts):
    if not ts:
        return [{'x':[], 'y': [], 'type': 'scatter'}]
    x = [point['timestamp'] for point in ts]
    y = [point['current_jumps'] for point in ts]
    two_mins_before = (parse(x[-1]) - timedelta(seconds=90)).isoformat()
    layout = {
        'title': 'Latest Activity',
        'xaxis': {
            'range': [two_mins_before, x[-1]]
        }
    }
    return [{'x': x, 'y': y, 'type': 'scatter', 'mode': 'markers'}], layout


def get_time_series(filter_user_name=''):
    if filter_user_name:
        return fmt_time_series([v for v in TIME_SERIES.get().values() if v['user'] == filter_user_name])
    return fmt_time_series(TIME_SERIES.get().values())