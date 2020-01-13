import os
import subprocess
from subprocess import Popen
import yaml

FNULL = open(os.devnull, 'w')


def read_config(path_to_config_yaml):
    with open(path_to_config_yaml, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def verify_youtubedl_installed():
    return_code = subprocess.run(
        ["which", "youtube-dl"], stdout=FNULL).returncode
    if return_code != 0:
        raise Exception("youtube-dl not found")


def createDirectories(config):
    for podcast in config['podcasts']:
        dir = '/downloads/' + podcast['channelName']
        try:
            print("Try creating directory: " + dir)
            os.mkdir(dir)
        except FileExistsError:
            print(f"Directory {dir} already exists")
        finally:
            writeConfigYaml(podcast)


def writeConfigYaml(podcast):
    fileName = os.path.join(
        '/downloads', podcast['channelName'], 'metadata.yaml')
    try:
        with open(fileName, 'w') as outfile:
            print(f"Writing metadata.yaml to dir: {podcast['channelName']}")
            yaml.dump(podcast, outfile, default_flow_style=False)
    except FileExistsError:
        print(f"{fileName} already exists")


def downloadPodcasts(config, cmd):
    allProcesses = []
    verbose = os.environ['VERBOSE']
    if verbose == False:
        out = FNULL
    else:
        out = None

    for podcast in config['podcasts']:
        downloadChannelCommand = cmd + ["--download-archive",
                                        f"/downloads/{podcast['channelName']}/archive.txt", "-o", f"/downloads/{podcast['channelName']}/%(title)s__%(uploader)s__%(upload_date)s.%(ext)s", podcast['playlistToDownloadURL']]
        print(f"Excecuting: {downloadChannelCommand}")
        parallelExecution = os.environ['PARALLEL']
        if parallelExecution:
            p = subprocess.Popen(downloadChannelCommand, stdout=out)
            allProcesses.append(p)
            try:
                for process in allProcesses:
                    process.wait()
            except Exception as e:
                print("Unexpected Exception: " + e.message)
        else:
            subprocess.run(downloadChannelCommand)


config = read_config('/config.yaml')
lengthFilter = config['minLength']

cmd = ["youtube-dl", "-x", "-i", "--dateafter", "now-12months", "--audio-format", "mp3",
       "--embed-thumbnail", "--add-metadata", "--match-filter", f"duration>{lengthFilter}"]

verify_youtubedl_installed()
createDirectories(config)
downloadPodcasts(config, cmd)
