import os
import subprocess
import yaml


def read_config(path_to_config_yaml):
    with open(path_to_config_yaml, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def verify_youtubedl_installed():
    FNULL = open(os.devnull, 'w')
    return_code = subprocess.run(
        ["which", "youtube-dl"], stdout=FNULL).returncode
    if return_code != 0:
        raise Exception("youtube-dl not found")


def createDirectories():
    for podcast in podcasts:
        dir = '/downloads/' + podcast['channelName']
        try:
            print("Try creating directory: " + dir)
            os.mkdir(dir)
        except FileExistsError:
            print(f"Directory {dir} already exists")


def downloadPodcasts(cmd):
    for podcast in podcasts:
        downloadChannelCommand = cmd + ["--download-archive",
                                        f"/downloads/{podcast['channelName']}/archive.txt", "-o", f"/downloads/{podcast['channelName']}/%(title)s__%(uploader)s__%(upload_date)s.%(ext)s", podcast['playlistToDownloadURL']]
        print(f"Excecuting: {downloadChannelCommand}")
        subprocess.run(downloadChannelCommand)


config = read_config('/config.yaml')
lengthFilter = config['minLength']
podcasts = config['podcasts']

cmd = ["youtube-dl", "-x", "-i", "--dateafter", "now-12months", "--audio-format", "mp3",
       "--embed-thumbnail", "--add-metadata", "--match-filter", f"duration>{lengthFilter}"]

verify_youtubedl_installed()
createDirectories()
downloadPodcasts(cmd)
