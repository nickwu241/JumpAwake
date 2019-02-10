import datetime
import requests
import calibrate_frame3
import subprocess
import sys
import time
import webbrowser

endpoint = "wakeupthe.net:5000"

def main(args):
    name = args[0]
    # webbrowser.open("http://{0}/#/{1}/wakeup".format(endpoint, name))

    response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
    print(response.text)
    while True:
        if response.text == "False":
            time.sleep(5)
            response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
            print(response.text)
            continue
        print("ALARM GOING OFF!!")

        subprocess.Popen(['curl', '-X', 'POST', "http://{0}/{1}/jump/end".format(endpoint, name)])
        calibrate_frame3.main(endpoint, name, 10)
        requests.post("http://{0}/{1}/alarm".format(endpoint, name), data="2019-02-11T01:00:00.000Z")
        response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
        subprocess.Popen(['curl', '-X', 'POST', "http://{0}/{1}/jump/finish".format(endpoint, name)])


if __name__ == '__main__':
    main(sys.argv[1:])
