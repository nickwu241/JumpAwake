import datetime
import requests
import calibrate_frame3
import subprocess
import sys
import time
import webbrowser

endpoint = "35.233.243.58:5000"

def main(args):
    name = args[0]
    # webbrowser.open("http://{0}/#/{1}/wakeup".format(endpoint, name))

    response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
    print(response.text)
    while response.text == "False":
        response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
        print(response.text)
        time.sleep(5)
    print("ALARM GOING OFF!!")

    calibrate_frame3.main(endpoint, name, 10)
    subprocess.Popen(['curl', '-X', 'POST', "http://{0}/{1}/jump/end".format(endpoint, name)])


if __name__ == '__main__':
    main(sys.argv[1:])
