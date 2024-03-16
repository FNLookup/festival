Json Dev Template

- tracks
  - track_identifier
    - title: Song
    - year: 2024
    - artist: FNLookup
    - scale: Major
    - instrument_defaults
      - vocals: keyboard
      - guitar: lead
      - drums: drums
      - bass: bass
    - difficulties
      - plastic_bass: 0
      - plastic_drums: 0
      - plastic_guitar: 0
      - vocals: 0
      - bass: 0
      - drums: 0
      - guitar: 0
    - duration: 0
    - album_image: url
    - bpm: 100
    - preview_start: 50
    - genre: music
    - key: Eb
    - stems:
      - streams: array
        [
          {
            url: location_ogg
            type: drums_track
          },
          {
            url: location_ogg
            type: background_track
          }
        ]
      - stream_source: string

# Explanations

`tracks`
array with every track's details

`track_identifier`
short string with the song in lower case containing the song details

`title`
song title

`year`
release year

`artist`
song artist

`scale`
music scale: major, minor

`instrument_defaults`
object containing the icons for each instrument, also represents the ingame instrument for that track

`instrument_defaults.vocals`
instrument used ingame for vocals track

`instrument_defaults.guitar`
instrument used ingame for guitar track

`instrument_defaults.drums`
instrument used ingame for drums track

`instrument_defaults.bass`
instrument used ingame for bass track

`difficulties`
object with the difficulty for every track

`difficulties.plastic_bass`
difficulty level for plastic bass

`difficulties.plastic_drums`
difficulty level for plastic drums

`difficulties.plastic_guitar`
difficulty level for plastic guitar

`difficulties.vocals`
difficulty level for vocals

`difficulties.bass`
difficulty level for bass

`difficulties.drums`
difficulty level for drums

`difficulties.guitar`
difficulty level for guitar

`duration`
duration in seconds

`album_image`
album art url

`bpm`
bpm for this track

`key`
music key for the track

`stems`
object containing streaming oggs for streams of songs

`stems.streams`
array with ogg tracks for the song

`stems.streams[all].url`
ogg audio file with the instrument stem

`stems.streams[all].type`
instrument for this stem

required: `stems.streams[all].type = combined`
all stems combined, full track for the preview and standalone track

`stems.stream_source`
source for obtaining these stems

optional: `stream_credits_url`
url to the credits of sourcers for the m4s segments for the stems of the track.
