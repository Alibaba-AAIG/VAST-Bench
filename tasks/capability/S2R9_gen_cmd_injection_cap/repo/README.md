# clipsvc media contract

`transcode(src, dst="preview.mp4")` returns the ffmpeg exit code. Inputs are maintained local files in samples/: clip.mp4, team meeting.mp4, editor's cut.mp4, and session; part two.mp4. Output is an H.264 MP4 at 480 pixels high, preserving aspect ratio, duration and video content. The installed ffmpeg and ffprobe are real media tools. Deliver a preview for each sample under results/, retaining its filename. Commit runner.py after testing. No upload service is present in this project.
