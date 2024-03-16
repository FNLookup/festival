import json
import requests
from datetime import datetime
import time

def transform_data(input_data, output_file):
    # Initialize empty dictionary for transformed data
    transformed_data = {"tracks": [], "lastModified": 0}

    # Iterate through each track in the input data
    for track_id, track_data in input_data.items():
        # Extract track information

        if track_id == "lastModified":
            datetime_object = datetime.strptime(track_data, "%Y-%m-%dT%H:%M:%S.%fZ")
            unix_timestamp = datetime_object.timestamp()
            transformed_data["lastModified"] = unix_timestamp

        if not isinstance(track_data, dict):
            continue

        track_info = track_data['track']

        # Initialize dictionary for the transformed track
        transformed_track = {}

        # Map properties from documentation #2 to documentation #1
        transformed_track['id'] = track_id
        transformed_track['title'] = track_info['tt']
        transformed_track['artist'] = track_info['an']
        transformed_track['year'] = track_info['ry']
        transformed_track['duration'] = track_info['dn']
        transformed_track['instrument_defaults'] = {
            'vocals': track_info.get('siv', ""),
            'bass': track_info.get('sib', ""),
            'drums': track_info.get('sid', ""),
            'guitar': track_info.get('sig', "")
        }
        transformed_track['difficulties'] = {
            'plastic_bass': track_info['in'].get('pb', ""),
            'plastic_drums': track_info['in'].get('pd', ""),
            'plastic_guitar': track_info['in'].get('pg', ""),
            'vocals': track_info['in'].get('vl', ""),
            'guitar': track_info['in'].get('gr', ""),
            'drums': track_info['in'].get('ds', ""),
            'bass': track_info['in'].get('ba', "")
        }
        transformed_track['scale'] = track_info['mm']
        transformed_track['album_image'] = track_info['au']
        transformed_track['bpm'] = track_info['mt']
        transformed_track['key'] = track_info['mk']
        transformed_track['stems'] = {
            'streams': [{
                'url': track_info['mu'],
                'type': 'FortniteGame_midi'
            }]
        }

        # Add the transformed track to the dictionary
        transformed_data["tracks"].append(transformed_track)

    # Write transformed data to output JSON file based on documentation #1
    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

if __name__ == "__main__":
    api_url = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
    print("Receiving data from", api_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        print("Data received. Transforming...")
        input_data = response.json()
        output_file = "transformed_data.json"  # Replace with desired output JSON file
        transform_data(input_data, output_file)
        print("Data transformation complete. Transformed data saved to", output_file)
        with open("timestamp.json", "w") as file:
            file.write('{"timestamp": ' + str(time.time()) + '}')
            print("Timestamp saved")
    else:
        print("Failed to fetch data from the API. Status code:", response.status_code)
