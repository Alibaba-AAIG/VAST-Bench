ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg git && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
WORKDIR /testbed
RUN mkdir -p samples && ffmpeg -v error -f lavfi -i color=c=blue:s=320x240:r=5:d=1 -c:v libx264 -pix_fmt yuv420p samples/clip.mp4 && cp samples/clip.mp4 'samples/team meeting.mp4' && cp samples/clip.mp4 "samples/editor's cut.mp4" && cp samples/clip.mp4 'samples/session; part two.mp4'
RUN git init -q && git add . && git -c user.name='clipsvc CI' -c user.email=ci@example.invalid commit -qm 'Initial local preview renderer'
