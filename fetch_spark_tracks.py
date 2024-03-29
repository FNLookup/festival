import json
import requests
from datetime import datetime
import time

def transform_data(input_data, output_file):
    transformed_data = {"tracks": [], "lastModified": 0}

    for track_id, track_data in input_data.items():
        if track_id == "lastModified":
            unix_timestamp = datetime.strptime(track_data, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            transformed_data["lastModified"] = unix_timestamp

        if not isinstance(track_data, dict):
            continue

        transformed_track = {}

        transformed_track['lastModified'] = datetime.strptime(track_data["lastModified"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        transformed_track['active'] = datetime.strptime(track_data["_activeDate"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        transformed_track['language'] = track_data["_locale"]

        track_info = track_data['track']

        transformed_track['id'] = track_id
        transformed_track['title'] = track_info['tt']
        transformed_track['artist'] = track_info['an']
        transformed_track['album'] = track_info.get('ab', "")
        transformed_track['genres'] = track_info.get('ge', [])
        transformed_track['year'] = track_info['ry']
        transformed_track['duration'] = track_info['dn']
        transformed_track['instrument_defaults'] = {
            'vocals': track_info.get('siv', ""),
            'bass': track_info.get('sib', ""),
            'drums': track_info.get('sid', ""),
            'guitar': track_info.get('sig', "")
        }
        transformed_track['gameplay_tags'] = track_info.get('gt', [])
        transformed_track['join_code'] = track_info.get('jc', "")
        transformed_track['item_id'] = track_info.get('ti', "")
        transformed_track['difficulties'] = {
            'plastic_bass': track_info['in'].get('pb', 0),
            'plastic_drums': track_info['in'].get('pd', 0),
            'plastic_guitar': track_info['in'].get('pg', 0),
            'vocals': track_info['in'].get('vl', 0),
            'guitar': track_info['in'].get('gr', 0),
            'drums': track_info['in'].get('ds', 0),
            'bass': track_info['in'].get('ba', 0)
        }
        transformed_track['scale'] = track_info['mm']
        transformed_track['album_image'] = track_info['au']
        transformed_track['bpm'] = track_info['mt']
        transformed_track['key'] = track_info['mk']
        transformed_track['event_id'] = track_info['su']
        transformed_track['isrc'] = track_info.get('isrc', "") #Festival got isrc in....cool
        transformed_track['rating'] = track_info.get('ar', "") #I think this is rating

        track_qi = json.loads(track_info["qi"])

        transformed_track['preview_start'] = track_qi['preview']["starttime"]

        transformed_track['resources'] = [
            {
                'url': track_info['mu'],
                'type': 'FortniteGame_midi'
            },
            {
                'url': track_info.get('ti', ""),
                'type': 'FortniteGame_lipsyncdata'
            },
            {
                'url': track_qi['sid'],
                'type': 'SongStreamingID'
            },
            {
                'url': track_qi['pid'],
                'type': 'PreviewStreamingID'
            }
        ]

        transformed_data["tracks"].append(transformed_track)

    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

if __name__ == "__main__":
    api_url = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
    print("Receiving data from", api_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        print("Data received. Transforming...")
        input_data = response.json()
        output_file = "transformed_data.json"
        transform_data(input_data, output_file)
        print("Data transformation complete. Transformed data saved to", output_file)
        with open("timestamp.json", "w") as file:
            file.write('{"timestamp": ' + str(time.time()) + '}')
            print("Timestamp saved")
    else:
        print("Failed to fetch data from the API. Status code:", response.status_code)
