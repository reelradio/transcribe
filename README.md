# transcribe.py

A python script to create a .txt transcript from an .m4a audio file

## How it works

1. Uses ffmpeg to convert an .m4a file into a .flac file (single channel, 16000 Hz)

2. Uploads the .flac file to a Google Cloud Storage bucket (required by Speech-to-Text for audio files over 60 seconds)

3. Deletes the .flac file from the local machine

4. Transcribes the uploaded .flac file, saving the transcript as a .txt file, while also building a mysql INSERT statement and appending it to the vsearch.sql file.

5. Deletes the .flac file from the Google Cloud Storage bucket

6. Simply log into the database and run the updated vsearch.sql file to add additional transcripts into the database.

## Set up your Google Cloud project

1. Sign in to Google Cloud Console

https://console.cloud.google.com/

2. Go to the project selector page and create a project

https://console.cloud.google.com/projectselector2/home

3. Enable the Speech-to-Text API

https://cloud.google.com/speech-to-text

4. Create a service account for your project

https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create

note: the account needs to have at least Storage Admin access in order to upload to the bucket on Google Cloud.

5. Create a JSON key for your service account

Select your service account, navigate to the KEYS tab, and select ADD KEY (Create new key)

This will download a JSON file to your machine, you'll need to know where this is later.

6. Create a Google Cloud Storage bucket

note: do not use a nested bucket.

https://console.cloud.google.com/storage/browser

## How to use

1. Pull the transcribe repository to the same machine as your audio files.

2. Edit transcribe.py and set BUCKET_NAME to the name of your Google Cloud Storage bucket.

3. Using a linux command line, set your authentication environment variable:

`export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"`

setting KEY_PATH with the path to your JSON key file, for example:

`export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"`

4. Call transcribe from the command line with the audio file as an argument:

`python3 transcribe.py path/to/file_name.m4a`

5. There may be a few installs required:

```
sudo apt install python3-pip
pip install --upgrade google
pip install --upgrade google-cloud-storage
pip install google-cloud-speech
sudo apt install ffmpeg
```

## Transcribe in batches

If you wish to loop over multiple .m4a audio files for processing, a shell script vloop.sh was created to facilitate using pattern matching  to transcribe batches with a single command.

Edit vloop.sh to declare the following:

1. Set the starting pattern

`starting_pattern="abc"` (this will match all files starting with the string “abc”)

2. Set the KEY_PATH with the path to your JSON file, just as before

`cred_path="/home/user/Downloads/service-account-file.json"`

3. Set the FILE_PATH with the path to your audio files to process

`FILES="audio/m4a"`

Call vloop from the command line:

`./vloop.sh`

vloop.sh does 2 passes, first transcribing all the scoped exhibits matching your specified starting pattern, then matching the remaining exhibits. Duplicates are avoided by checking the txt folder for an existing transcript, scoped or unscoped.

## Troubleshooting

Google Cloud's Speech-to-Text API can be tricky to get set up correctly.

1. If the process fails during audio conversion, make sure the original audio files are in .m4a format. Conversion from other formats is not currently supported.

2. If the process fails during upload to your Google Cloud Storage bucket, make sure your service account was granted at least Storage Admin access.

3. If the process fails during transcription, make sure the file path to your JSON key is correctly set and that Google Cloud's Speech-to-Text API is activated. Wait a few minutes before trying again.

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

