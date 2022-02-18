# Copyright 2021 Google Inc. All Rights Reserved:
#   upload_blob()
#   transcribe()
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
from pydub import AudioSegment

bucket_name = "reelradio"

# [START convert .m4a to .flac]
def convert_m4a_to_flac(m4a_file):
    new_version = AudioSegment.from_file(m4a_file)
    new_version.export(Path(m4a_file).stem + ".flac", format="flac", parameters=["-ac", "1", "-ar", "16000"])
    print(time.ctime() + " - Conversion complete.\n")
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

    print(time.ctime() + " - Upload complete.\n")
# [END storage_upload_file]


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
        f.write(u"{}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    f.close()
    print(time.ctime() + " - Transcription complete.\n")
# [END speech_transcribe_async_gcs]


if __name__ == "__main__":
    # grab stem from filename open new file named {filename}.txt
    audio_name = sys.argv[1]
    audio_stem = Path(audio_name).stem
    audio_converted = audio_stem + ".flac"
    audio_text = audio_stem + ".txt"
    f = open(audio_text, "a")

    # Convert audio
    print(time.ctime() + " - Converting " + audio_stem + ".m4a to " + audio_converted + " ...")
    convert_m4a_to_flac(audio_name)

    # Upload converted audio file
    print(time.ctime() + " - Uploading " + audio_converted + " to Google Cloud Storage ...")
    upload_blob(bucket_name, audio_converted, audio_converted)

    # Transcribe audio file
    print(time.ctime() + " - Transcribing " + audio_converted + " to " + audio_text + " ...")
    transcribe("gs://" + bucket_name + "/" + audio_converted)
