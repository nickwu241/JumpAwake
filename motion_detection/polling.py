import datetime
import requests
import calibrate_frame2
import sys
import time
import webbrowser

endpoint = "7fbfdf67.ngrok.io"

def main(args):
    name = args[0]
    webbrowser.open("http://{0}/#/{1}/wakeup".format(endpoint, name))

    response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))

    # while not response.text:
    #     response = requests.get("http://{0}/{1}/alarm".format(endpoint, name))
    #     time.sleep(5)

    calibrate_frame2.main(endpoint, name)


if __name__ == '__main__':
    main(sys.argv[1:])
