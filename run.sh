#!/bin/bash
#!/usr/bin/env bash

# shellcheck disable=SC2006
# shellcheck disable=SC2002
# shellcheck disable=SC2126
# shellcheck disable=SC2197
# cpunum=`cat /proc/cpuinfo | grep processor | wc -l`
cpunum=`fgrep processor /proc/cpuinfo | sort -u | wc -l`
point=16736
echo 'current cpu number is: '"$cpunum"
echo ''
echo 'recommend algorithm start ...'
nohup gunicorn --worker-class=gevent --worker-connections=500 --workers="$cpunum" -b 0.0.0.0:"$point"  runserver:app &
echo 'recommend algorithm start finished ...'
echo 'the interface port is '"$point"
echo 'please test interface is nomal... '