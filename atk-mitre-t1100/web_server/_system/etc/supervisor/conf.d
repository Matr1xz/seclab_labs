[supervisord]
nodaemon=true

[program:watch_file]
command=/bin/sh /home/student/watch_file.sh
autostart=true
autorestart=true
