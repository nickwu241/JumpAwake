const functions = require('firebase-functions');
const {
    dialogflow
} = require('actions-on-google');

const app = dialogflow({
    debug: true
});

app.intent('Set Alarm Intent', (conv, data) => {
    if (!data['time']) {
        conv.ask('Okay. At what time?')
        return
    }
    conv.close(`Your alarm is set for ${data['time']}`)
})

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);