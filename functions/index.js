const functions = require('firebase-functions');
const {
    dialogflow
} = require('actions-on-google');
const axios = require('axios');

if (!Date.prototype.toISOString) {
    (function () {

        function pad(number) {
            if (number < 10) {
                return '0' + number;
            }
            return number;
        }

        Date.prototype.toISOString = function () {
            return this.getUTCFullYear() +
                '-' + pad(this.getUTCMonth() + 1) +
                '-' + pad(this.getUTCDate()) +
                'T' + pad(this.getUTCHours()) +
                ':' + pad(this.getUTCMinutes()) +
                ':' + pad(this.getUTCSeconds()) +
                '.' + (this.getUTCMilliseconds() / 1000).toFixed(3).slice(2, 5) +
                'Z';
        };

    }());
}

const app = dialogflow({
    debug: true
});

const user1 = 'gordon'
const user2 = 'marshall'
const endpointBaseUrl = 'http://wakeupthe.net:5000'

const endpoint1 = `${endpointBaseUrl}/${user1}/alarm`
const endpoint2 = `${endpointBaseUrl}/${user2}/alarm`

app.intent('Set Alarm Intent', (conv, data) => {
    if (!data['time']) {
        conv.ask('Okay. At what time?')
        return
    }
    const alarm = new Date(data['time'])
    const alarmISO = alarm.toISOString()

    console.log(`POST ${endpoint1}: ${alarmISO}`)
    var p1 = axios.post(endpoint1, alarmISO, {
            headers: {
                'Content-Type': 'text/plain'
            }
        })
        .then(res => {
            console.log(res)
            return res
        })

    console.log(`POST ${endpoint2}: ${alarmISO}`)
    var p2 = axios.post(endpoint2, alarmISO, {
            headers: {
                'Content-Type': 'text/plain'
            }
        })
        .then(res => {
            console.log(res)
            return res
        })

    return Promise.all([p1, p2])
        .then(r => conv.close(`Your alarm is set.`))
        .catch(err => {
            console.error(err)
        });
})

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);