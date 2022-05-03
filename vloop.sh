#!/bin/bash
starting_pattern="PATTERN" # Replace PATTERN with your starting pattern
cred_path="KEY_PATH"       # Replace KEY_PATH with the path to your JSON credentials
FILES="FILE_PATH"          # Replace FILE_PATH with the path to your audio files

pattern1="${FILES}/${starting_pattern}.*-sc.m4a"
pattern2="${FILES}/${starting_pattern}.*.m4a"

export GOOGLE_APPLICATION_CREDENTIALS="${cred_path}";

#transcribes all scoped files
for f in $FILES/*;
do
   if [[ "$f" =~ $pattern1 ]]
   then
      echo "python3 transcribe.py $f";
      python3 transcribe.py $f;
   fi
done

#transcribes remaining unscoped files (checks for existing in transcribe.py)
for f in $FILES/*;
do
   if [[ "$f" =~ $pattern2 ]]
   then
      echo "python3 transcribe.py $f";
      python3 transcribe.py $f;
   fi
done

