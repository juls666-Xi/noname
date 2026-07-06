#!/bin/bash

# Default password (change it or set via environment)
PASSWORD="${TIMER_PASSWORD:-secret}"

# Check if duration is given
if [ -z "$1" ]; then
    echo "Usage: $0 <seconds> [password]"
    exit 1
fi

# Optional password override from argument
if [ -n "$2" ]; then
    PASSWORD="$2"
fi

DURATION="$1"

# Trap Ctrl+C (SIGINT)
trap 'ask_password' INT

ask_password() {
    echo
    echo -n "Enter password to stop the timer: "
    read -s user_pass
    echo
    if [ "$user_pass" = "$PASSWORD" ]; then
        echo "Password correct. Stopping timer."
        exit 0
    else
        echo "Wrong password. Timer continues."
        # Resume countdown
    fi
}

echo "Timer started for $DURATION seconds. Press Ctrl+C to stop (password required)."

# Countdown loop
for ((i=DURATION; i>0; i--)); do
    printf "\rTime remaining: %02d:%02d" $((i/60)) $((i%60))
    sleep 1
done

echo -e "\nTimer finished!"