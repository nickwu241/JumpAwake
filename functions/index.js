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

const user = 'gordon'
const endpointBaseUrl = 'http://7fbfdf67.ngrok.io'

const endpoint = `${endpointBaseUrl}/${user}/alarm`

app.intent('Set Alarm Intent', (conv, data) => {
    if (!data['time']) {
        conv.ask('Okay. At what time?')
        return
    }
    const alarm = new Date(data['time'])
    const alarmISO = alarm.toISOString()

    console.log(`POST ${endpoint}: ${alarmISO}`)
    return axios.post(endpoint, alarmISO, {
            headers: {
                'Content-Type': 'text/plain'
            }
        })
        .then(res => {
            console.log(res)
            conv.close(`Your alarm is set.`)
            return res
        })
        .catch(err => {
            console.error(err)
            conv.close(`Your alarm is set.`)
        })
})

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);