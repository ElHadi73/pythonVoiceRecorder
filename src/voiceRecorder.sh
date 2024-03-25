#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path> $1 <filename>"
    exit 1
fi

if [ "${0%/}" != "$0" ]; then
    echo "Usage: $0 <path/>"
    echo "dont forget '/' for directory"
    exit 1
fi

# Extract the filename from the arguments
filename="$2"

#record registring destination
destinationPath=$1
#destinationPath="/home/oli/Music/recordings/"

#start recording program
python3 voiceRecorderDir/voiceRecorder.py

# Give read permissions to everyone
chmod 444 "record.wav"

# Check if the target directory exists, create if it doesn't
if [ ! -d "$destinationPath" ]; then
    mkdir -p "$destinationPath"
fi

# Copy the file to the specified directory
mv "record.wav" "$destinationPath$filename.wav"

echo "$filename has been created, permissions set, and copied to $destinationPath"
