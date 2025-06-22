docker build -t video-pipeline .
docker run -v /local/path/to/video:/app/input.mp4 -v /local/output:/app/output video-pipeline --video_path /app/input.mp4 --output_dir /app/output