# Copyright 2021 Google Inc. All Rights Reserved:
#   upload_blob()
#   transcribe()
#   delete_blob()
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

# Modified for use by:
# Victor Galbraith
# 14 February 2022

"""Google Cloud Speech-to-Text application using the gRPC for async
batch processing.
"""

import argparse
import glob
import os
import sys
import time

from google.cloud import speech
from google.cloud import storage
from pathlib import Path

bucket_name = "BUCKET_NAME" # Replace BUCKET_NAME with your bucket name
flac_folder = "flac"
txt_folder = "txt"

# [START convert .m4a to .flac]
def convert_m4a_to_flac(m4a_file):
    os.system("ffmpeg -i " + m4a_file + " -ar 16000 -ac 1 -loglevel quiet flac/" + Path(m4a_file).stem + ".flac")
    print(time.ctime() + " - Conversion complete.")
# [END convert .m4a to .flac]


# [START storage_upload_file]
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(time.ctime() + " - Upload complete.")
# [END storage_upload_file]


# [START delete_flac]
def delete_flac(flac_file):
    os.remove(flac_file)

    print(time.ctime() + " - Deletion complete.")
# [END delete_flac]


# [START speech_transcribe_async_gcs]
def transcribe(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=5000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        f1.write(u"{}".format(result.alternatives[0].transcript))
        f2.write(u"{}".format(result.alternatives[0].transcript))
        #print("Confidence: {}".format(result.alternatives[0].confidence))

    f1.close()
    print(time.ctime() + " - Transcription complete.")
# [END speech_transcribe_async_gcs]


# [START delete_blob]
def delete_blob(bucket_name, blob_name):
    """deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print(time.ctime() + " - Deletion complete.\n")
# [END delete_blob]


if __name__ == "__main__":
    # grab stem from filename open new file named {filename}.txt
    audio_name = sys.argv[1]
    audio_stem = Path(audio_name).stem
    audio_converted = audio_stem + ".flac"
    audio_text = audio_stem + ".txt"

    #checks if the transcription already exists
    path_sc = Path(txt_folder + "/" + audio_text)
    if path_sc.is_file():
        print("transcription exists\n")
        sys.exit()

    #checks if a scoped transcription already exists
    path_sc = Path(txt_folder + "/" + audio_stem + "-sc.txt")
    if path_sc.is_file():
        print("scoped transcription exists\n")
        sys.exit()

    # Convert audio
    print(time.ctime() + " - Converting " + audio_stem + ".m4a to " + audio_converted + " ...")
    convert_m4a_to_flac(audio_name)

    # Upload converted audio file
    print(time.ctime() + " - Uploading " + audio_converted + " to Google Cloud Storage ...")
    upload_blob(bucket_name, flac_folder + "/" + audio_converted, audio_converted)

    # Delete .flac file from local machine
    print(time.ctime() + " - Deleting flac/" + audio_converted + " ...")
    delete_flac(flac_folder + "/" + audio_converted)

    # Transcribe audio file and build mysql INSERT statement
    print(time.ctime() + " - Transcribing " + audio_converted + " to " + audio_text + " ...")
    f1 = open(txt_folder + "/" + audio_text, "a")
    f2 = open("vsearch.sql", "a")
    f2.write("INSERT INTO vsearch VALUES ('" + audio_stem + "', \"")
    transcribe("gs://" + bucket_name + "/" + audio_converted)
    f2.write("\");\n")
    f2.close()

    # Delete .flac file from bucket
    print(time.ctime() + " - Deleting gs://" + bucket_name + "/" + audio_converted + " ...")
    delete_blob(bucket_name, audio_converted)

