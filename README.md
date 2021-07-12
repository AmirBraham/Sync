# Sync
Syncing Youtube and Spotify playlists

bugs and improvements:
- sometimes script need to be executed twice to detect changes
- deletion sometimes fails
- upload to heroku and execute every hour
- better youtube title cleanup for easier spotify search
- batch search and add songs to playlists

# provide the following files to run it on your machine
postgres.json :
```
 { 
     "POSTGRES_URI" :"your_postgres_uri"
    }
```

spotify_client_secret.json : 
```


{
    "SPOTIPY_CLIENT_ID": "",
    "SPOTIPY_CLIENT_SECRET": "",
    "SPOTIPY_REDIRECT_URI": ""
}
```

client_secret.json : 
```

{
    "installed": {
        "client_id": "",
        "project_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_secret": "",
        "redirect_uris": [
            "",
            ""
        ]
    }
}
```

## playlists you want to sync should have  "#sync" in their description