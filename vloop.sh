#!/bin/bash
starting_pattern="a"
cred_path="KEY_PATH"

FILES="../../m4a"
pattern="${FILES}/${starting_pattern}.*.m4a"

export GOOGLE_APPLICATION_CREDENTIALS="${cred_path}";

for f in $FILES/*;
do
   if [[ "$f" =~ $pattern ]]
   then
      echo "python3 transcribe.py $f";
      python3 transcribe.py $f;
   fi
done

