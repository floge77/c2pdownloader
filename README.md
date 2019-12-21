# Cloud2Podcast Downloader

Downloads youtube channels based on your configuration using youtube-dl.

## How to use

1. Clone this repository.

2. Create a config.yaml and provide the necessary infos as:

   - Minimal length of the videos
   - Name of the channel
   - URL of the channel
   - URL of the channel's image
   - URL of the playlist to download

See an example here:

```yaml
minLength: 1800

podcasts:
  - channelName: "Q-Dance"
    channelURL: "https://www.youtube.com/user/Qdancedotnl"
    channelImageURL: "https://yt3.ggpht.com/a-/AN66SAzyW12uAQRayPY4MS_Fo_Wlj6PFjyNfx3X7CQ=s288-mo-c-c0xffffffff-rj-k-no"
    playlistToDownloadURL: "https://www.youtube.com/user/Qdancedotnl/videos"
  - channelName: "B2S"
    channelURL: "https://www.youtube.com/user/officialb2s"
    channelImageURL: "https://yt3.ggpht.com/a-/AN66SAzOHiotaZ20EWS6f9SHfzDPHQeAR_gyn-ng9w=s288-mo-c-c0xffffffff-rj-k-no"
    playlistToDownloadURL: "https://www.youtube.com/user/officialb2s/videos"
```

3. Build the docker image with `docker build -t c2pdownloader .`

4. Run the docker container with the config.yaml and downloads directory mounted:

```bash
docker run -it --rm --name c2pdownloader -v $(pwd)/config.yaml:/config.yaml -v /Users/floge77/Downloads:/downloads c2pdownloader
```

The downloads will run in parallel which is why the output of youtube-dl would be a mess. Therefore c2pdownloader will print the output to /dev/null. If you wish to see the output or need to debug c2pdownloader just add "`-e VERBOSE=True`" to the docker run command.
