# JumpAwake
[XdHacks 2019] Do jumping jacks to silence your alarm!

# Problem
Too many people are stuck in their beds, some also choose to repeatedly snooze their alarms, and many people want exercise but need that initial encouragement!

# Solution
Starting the day off early with improves your physical health and heightens your alertness.

Our IoT device is an alarm that requires you to do physical exercise routines such as jumping jacks, squats, burpees, sit ups in order to shut off the alarm.

To add additional motivation, we've gamified this experience to provide social motivation for users that's striving to wake up early by implementing:
- A live Competition mode for real-time activity tracking against an opponent
- A dashboard to show statistics for your activities
- A Google Home companion application to schedule your fitness alarm

# Technology Used
Our IoT devices include a Qualcomm Dragonboard and Raspberry Pi 3 running machine vision algorithms to detect the user's motions such as jumping jacks.
We are running 2 algorithms for Computer Vision:
- OpenCV Haar Casscades on low-compute devices such as IoT devices
- Caffe Based Face Detector which uses a Deep Neural Net algorithm that detects more accurately for devices with more compute

Our web service is hosted on `Google Cloud Platform` using `Google Compute Engine` making use of web-sockets for real-time communication.

We also leveraged
- `Firebase Real-time Database` for data store
- `Google Cloud Functions` to run workloads such a scheduling alarms
- `Google Dialogflow Agent` to facilitate interactions with `Google Assistant`
- `Google Assistant` for voice control activation and settings

## Development
### Deploy To Google Cloud Platform
```sh
# Initialize terraform once
terraform init

# Create resources for the demo
terraform apply

# Transfer production files to Google Cloud Compute instance
./frontend/create_build.sh
./sync.sh

# Clean up resources after demoing
terraform destroy
```