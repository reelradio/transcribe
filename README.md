# transcribe.py

A python script to create a .txt transcript from an .m4a audio file

## How it works

1. Uses ffmpeg to convert an .m4a file into a .flac file (single channel, 16000 Hz)

2. Uploads the .flac file to a Goole Cloud Storage bucket (required by Speech-to-Text for audio files over 60 seconds)

3. Deletes the .flac file from the local machine

4. Transcribes the .flac file and saves it as a .txt file, also builds a mysql INSERT statement

5. Deletes the .flac file from the Google Cloud Storage bucket

## Setup

Set up your Google Cloud project:

1. Sign in to Cloud Console

https://console.cloud.google.com/

2. Go to the project selector page and create a project

https://console.cloud.google.com/projectselector2/home

3. Enable the Speech-to-Text API

https://cloud.google.com/speech-to-text

4. Create a service account for your project

https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create

note: the account needs to have at least Storage Admin access in order to upload to the bucket onGoogle Cloud

5. Create a JSON key for your service account

Select your service account, navigate to the KEYS tab, and select ADD KEY (Create new key)

6. Create a Cloud Storage bucket

https://console.cloud.google.com/storage/browser

## How to use

The only variable in the script that should need to be changed between users is the bucket_name declared on line 30.

In a linux environment, set your authentication environment variable:

`export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"`

Set the KEY_PATH to your JSON key file, for example:

`export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"`

Call transcribe from the command line with the audio file as an argument:

`python3 transcribe.py file_name.m4a`

There may be a few installs required:
```
sudo apt install python3-pip
pip install --upgrade google
pip install --upgrade google-cloud-storage
pip install google-cloud-speech
sudo apt install ffmpeg
```

## vloop.sh option

A shell script to loop through files using pattern matching to transcribe batches with a single command.

Edit vloop.sh to declare the following:

1. Set your starting string

`starting_pattern="abc"`

2. Set the KEY_PATH to your JSON file, same as before

`export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"`

Call vloop from the command line:

`./vloop.sh`

vloop.sh does 2 passes, first transcribing all the scoped exhibits mathcing your specified starting pattern, then matching the remaining exhibits that don't already have a scoped transcript completed.

### Additional Resources

ffmpeg:

https://ffmpeg.org/

Upload objects to a Google Cloud Storage bucket:

https://cloud.google.com/storage/docs/uploading-objects

Transcribe short audio files:

https://cloud.google.com/speech-to-text/docs/sync-recognize

Transcribe long audio files:

https://cloud.google.com/speech-to-text/docs/async-recognize#speech_transcribe_async_gcs-python

Delete objects from a Google Cloud Storage bucket:

https://cloud.google.com/storage/docs/deleting-objects

