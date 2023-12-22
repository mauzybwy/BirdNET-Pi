#!/usr/bin/env bash
# Make sox spectrogram
source /etc/birdnet/birdnet.conf

PYTHON_VIRTUAL_ENV="$HOME/BirdNET-Pi/birdnet/bin/python3"
DIR="$HOME/BirdNET-Pi/scripts"

# Read the logging level from the configuration option
LOGGING_LEVEL="${LogLevel_SpectrogramViewerService}"
# If empty for some reason default to log level of error
[ -z $LOGGING_LEVEL ] && LOGGING_LEVEL='error'
# Additionally if we're at debug or info level then allow printing of script commands and variables
if [ "$LOGGING_LEVEL" == "info" ] || [ "$LOGGING_LEVEL" == "debug" ];then
  # Enable printing of commands/variables etc to terminal for debugging
  set -x
fi

# Time to sleep between generating spectrogram's, default set the recording length
# To try catch the spectrogram as soon as possible run at a smaller intervals
SLEEP_DELAY=$((RECORDING_LENGTH / 4))

# Continuously loop generating a spectrogram every 10 seconds
while true; do
  analyzing_now="$(cat $HOME/BirdNET-Pi/analyzing_now.txt)"

  if [ ! -z "${analyzing_now}" ] && [ -f "${analyzing_now}" ]; then
    echo "GENERATE ANALYZING_NOW SPECTROGRAM"
    spectrogram_png=${EXTRACTED}/spectrogram.png
    sox -V1 "${analyzing_now}" -n remix 1 rate 24k spectrogram -c "${analyzing_now//$HOME\//}" -o "${spectrogram_png}"

    # echo "CONVERT ANALYZING_NOW TO MP3"
    # analyzing_now_mp3=${EXTRACTED}/analyzing_now.mp3
    # sox -V1 "${analyzing_now}" "${analyzing_now_mp3}"

    # echo "SEND ANALYZING_NOW TO FIREBASE"
    # $PYTHON_VIRTUAL_ENV $DIR/firebase_analyzing_now.py ${analyzing_now_mp3} ${spectrogram_png}
  fi

  sleep $SLEEP_DELAY
done
