import sys
import requests
import gzip
import datetime
from tzlocal import get_localzone
import re

FB_URL = "https://us-central1-bubblebird-5940d.cloudfunctions.net"

def main():
    print("-------- WELCOME TO FIREBASE ----------")

    _, date, start, end, common, scientific, confidence, mp3_fpath, png_fpath \
        = sys.argv
    current_iso8601 = calc_datetime_from_fname(mp3_fpath)

    data = {
        'timestamp': current_iso8601,
        'soundscapeStartTime': start,
        'soundscapeEndTime': end,
        'scientificName': scientific,
        'commonName': common,
        'confidence': confidence,
    }

    soundscape_id = upload_soundscape(mp3_fpath, current_iso8601)
    if not soundscape_id:
        print("COULD NOT UPLOAD SOUNDSCAPE")
        return

    success = upload_spectrogram(png_fpath, soundscape_id)
    if not success:
        print("COULD NOT UPLOAD SPECTROGRAM")
        return

    data['id'] = soundscape_id
    success = upload_metadata(data)
    if not success:
        print("COULD NOT UPLOAD METADATA")


def calc_datetime_from_fname(fname):
    mat = re.match(
        r".*(\d{4}-\d{1,2}-\d{1,2})-birdnet-(\d{1,2}:\d{1,2}:\d{1,2}).*",
        fname
    )

    if not mat:
        raise

    date_time_str = "{} {}".format(mat.group(1), mat.group(2))
    print(date_time_str)
    date_time_obj = datetime.datetime.strptime(
        date_time_str,
        '%Y-%m-%d %H:%M:%S'
    )
    print('Date-time:', date_time_obj)
    now = date_time_obj
    current_iso8601 = now.astimezone(get_localzone()).isoformat()

    return current_iso8601


def upload_soundscape(mp3_fpath, current_iso8601):
    try:
        print("UPLOAD SOUNDSCAPE")
        soundscape_url = "{}/soundscapes?timestamp={}".format(
            FB_URL,
            current_iso8601
        )

        with open(mp3_fpath, 'rb') as f:
            mp3_data = f.read()
            gzip_mp3_data = gzip.compress(mp3_data)
            response = requests.post(
                url=soundscape_url,
                data=gzip_mp3_data,
                headers={
                    'Content-Type': 'application/octet-stream',
                    'Content-Encoding': 'gzip'
                })

            print("Soundscape POST Response Status - ", response.status_code)
            sdata = response.json()
            soundscape_id = sdata['soundscape']['id']
            return soundscape_id

    except BaseException as err:
        print("Error on soundscape POST", err)


def upload_spectrogram(png_fpath, soundscape_id):
    try:
        print("UPLOAD SPECTROGRAM")
        soundscape_url = "{}/spectrograms?soundscapeId={}".format(
            FB_URL,
            soundscape_id
        )

        with open(png_fpath, 'rb') as f:
            png_data = f.read()
            gzip_png_data = gzip.compress(png_data)
            response = requests.post(
                url=soundscape_url,
                data=gzip_png_data,
                headers={
                    'Content-Type': 'application/octet-stream',
                    'Content-Encoding': 'gzip'
                })

            print("Soundscape POST Response Status - ", response.status_code)
            return True

    except BaseException as err:
        print("Error on soundscape POST", err)


def upload_metadata(metadata):
    try:
        print("UPLOAD DETECTION METADATA")
        print(metadata)
        detection_url = "{}/detections".format(FB_URL)
        response = requests.post(detection_url, json=metadata)
        print("Detection POST Response Status - ", response.status_code)
        return True

    except BaseException as err:
        print("Error on metadata POST", err)


if __name__ == "__main__":
    main()
