![Galiboo](./assets/logo.png)

# Python SDK for Galiboo's A.I. Music API (beta)
https://galiboo.com

## API key
Be sure to get an API key from <a href="https://galiboo.com">https://galiboo.com</a> to use this library.

## Installation

```bash
pip install galiboo
```

## Usage
Here are some examples. 
You can also checkout our API docs at: <a href="https://apidocs.galiboo.com">https://apidocs.galiboo.com</a>

### Authentication
Always set your API key first, before calling any other API endpoints.

```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")
```


### AI-powered search for music
Find tracks that are relevant to any natural language query, auto-magically.
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's search for some relaxing music
query = "soft, piano tunes"
tracks = galiboo_client.track.smart_search(query)
```

### Get a track's music analysis data
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's get the moods, emotions, & other music analysis data
# that Galiboo's Music A.I. has extracted for Coldplay's "Viva la Vida"

viva_la_vida = galiboo_client.track.get("5a3fc326d836490c18703e3f")

print viva_la_vida['analysis']
print viva_la_vida['analysis']['smart_tags']
# etc...
```

### Find tracks by tags
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's find some nice music for doing focus work
query = {
    "energy" : 0.25,
    "smart_tags" : {
         "Emotion-Calming_/_Soothing" : 0.9
    }
    # etc. (see our API docs for more info)
}

tracks = galiboo_client.track.search_by_tags(query)
print tracks
```

### Find similar-sounding tracks
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's find similar tracks to Coldplay's Viva la Vida
similar_tracks = galiboo_client.track.search_by_similar("5a3fc326d836490c18703e3f")

print similar_tracks
```

### Analyze music from a URL
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's analyze the audio at this URL
audio_url = "https://storage.googleapis.com/gb_spotify20k/spotify_preview_audios/4iLqG9SeJSnt0cSPICSjxv.mp3"
analysis = galiboo_client.track.analyze(audio_url)

print analysis
```

### Analyze music from a YouTube video
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's analyze the audio at this URL
youtube_video = "https://www.youtube.com/watch?v=nfs8NYg7yQM"
analysis = galiboo_client.track.ai_analyze(youtube_video)

print analysis
```

### Schedule a music analysis job
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's schedule a job in Galiboo's cloud to analyze the audio at this URL
audio_url = "https://storage.googleapis.com/gb_spotify20k/spotify_preview_audios/4iLqG9SeJSnt0cSPICSjxv.mp3"
job = galiboo_client.track.analyze(audio_url)

print job
```

### View a music analysis job
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's get the status/results of an analysis job that we scheduled
job_id = "5b8c17c9011610000bc2de67"
job = galiboo_client.job.get(job_id)

print job
```

### View all music analysis jobs
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's get the status/results of all the analysis jobs that we scheduled
jobs = galiboo_client.job.all()
print jobs
```

### Search for tracks
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's search for Charlie Puth's Attention
track = "Attention"
tracks = galiboo_client.track.get(track=track)
```

### Search for artists
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

# Let's search for some relaxing music
artist = "Camila Cabello"
artists = galiboo_client.artist.get(artist)
```


### Get an artist's metadata
```python
from galiboo import Galiboo
galiboo_client = Galiboo("<your api key>")

coldplay = galiboo_client.artist.metadata("5a3fc2ffd836490c18703c7d")

print coldplay['tracks']
```

## Last words
Be sure to checkout our API docs at <a href="apidocs.galiboo.com">apidocs.galiboo.com</a> and visit our website (<a href="https://galiboo.com">galiboo.com</a>) for more information.

If you have any questions, feel free to email us at <a href="mailto:hello@galiboo.com">hello@galiboo.com</a>, and we'll get back to you ASAP! :)
