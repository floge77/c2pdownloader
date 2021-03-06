FROM alpine

RUN apk update && apk add --no-cache ffmpeg curl python3 py3-pip
RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
RUN chmod a+rx /usr/local/bin/youtube-dl

VOLUME [ "/downloads" ]

WORKDIR /c2pdownloader

ADD downloader.py Pipfile Pipfile.lock ./

ENV VERBOSE=false
ENV PARALLEL=false

RUN pip3 install --no-cache-dir pipenv &&  pipenv install --python /usr/bin/python3
ENTRYPOINT ["pipenv", "run", "python3", "downloader.py"]
