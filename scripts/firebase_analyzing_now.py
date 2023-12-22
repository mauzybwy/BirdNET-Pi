import sys
import requests
import gzip
import datetime
from tzlocal import get_localzone
import re

FB_URL = "http://192.168.1.156:5001/bubblebird-5940d/us-central1"


def main():
    print("-------- ANALYZING NOW FIREBASE ----------")

    _, mp3_fpath, png_fpath = sys.argv

    success = upload_mp3(mp3_fpath)
    if not success:
        print("COULD NOT UPLOAD MP3")
        return

    success = upload_spectrogram(png_fpath)
    if not success:
        print("COULD NOT UPLOAD SPECTROGRAM")
        return


def upload_mp3(mp3_fpath):
    try:
        print("UPLOAD MP3")
        soundscape_url = "{}/soundscapes?analyzing_now=true".format(FB_URL)

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
            return True

    except BaseException as err:
        print("Error on soundscape POST", err)


def upload_spectrogram(png_fpath):
    try:
        print("UPLOAD SPECTROGRAM")
        spectrogram_url = "{}/spectrograms?analyzing_now=true".format(FB_URL)

        with open(png_fpath, 'rb') as f:
            png_data = f.read()
            gzip_png_data = gzip.compress(png_data)
            response = requests.post(
                url=spectrogram_url,
                data=gzip_png_data,
                headers={
                    'Content-Type': 'application/octet-stream',
                    'Content-Encoding': 'gzip'
                })

            print("Soundscape POST Response Status - ", response.status_code)
            return True

    except BaseException as err:
        print("Error on soundscape POST", err)


if __name__ == "__main__":
    main()
