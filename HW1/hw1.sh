#!/bin/bash

PIDFILE="monitor.pid"
LOGDIR="logs"
mkdir -p "$LOGDIR"

monitor() {
    start=$(date +"%Y-%m-%d_%H-%M-%S")
    current_date=$(date +"%Y-%m-%d")
    filename="${current_date}_${start}.csv"
    filepath="$LOGDIR/$filename"

    echo "Timestamp,DiskUsage,InodesUsage" > "$filepath"

    while true
    do

        current_time=$(date +"%Y-%m-%d %H:%M:%S")
        new_date=$(date +"%Y-%m-%d")

        if [ "$new_date" != "$current_date" ]; then
            current_date=$new_date
            start=$(date +"%Y-%m-%d_%H-%M-%S")
            filename="${current_date}_${start}.csv"
            filepath="$LOGDIR/$filename"

            echo "Timestamp,DiskUsage,InodesUsage" > "$filepath"
        fi

        disk_available=$(df -m | awk '$NF == "/" {print $4}')
        inode_available=$(df -i | awk '$NF == "/" {print $7}')

        echo "$current_time,$disk_available,$inode_available" >> "$filepath"

        sleep 60

    done
}

case "$1" in
    START)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "Мониторинг уже запущен"
        else 
            monitor &
            PID=$!
            echo "$PID" > "$PIDFILE"
            echo "Мониторинг запущен с PID $PID"
        fi
        ;;
    STOP)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            PID=$(cat "$PIDFILE")
            kill $PID
            rm "$PIDFILE"
            echo "Мониторинг остановлен"
        else
            echo "Мониторинг не запущен"
        fi
        ;;
    STATUS)
        if [ -f "$PIDFILE" ]  && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "Мониторинг запущен с PID $(cat $PIDFILE)"
        else
            echo "Мониторинг не запущен"
        fi
        ;;

esac
exit 0
