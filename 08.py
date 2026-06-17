import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Supported audio formats
SUPPORTED_EXTS = {'.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac'}

def get_audio_files(directory):
    """Recursively finds all audio files in a directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if Path(filename).suffix.lower() in SUPPORTED_EXTS:
                files.append(os.path.join(root, filename))
    return sorted(files)

def play_file(filepath):
    subprocess.run(['termux-media-player', 'play', filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def pause_resume():
    try:
        info = subprocess.check_output(['termux-media-player', 'info'], text=True, stderr=subprocess.DEVNULL)
        data = json.loads(info)
        if data.get('paused'):
            subprocess.run(['termux-media-player', 'resume'], stdout=subprocess.DEVNULL)
            return "Playing"
        else:
            subprocess.run(['termux-media-player', 'pause'], stdout=subprocess.DEVNULL)
            return "Paused"
    except Exception:
        return "Unknown"

def stop_playback():
    subprocess.run(['termux-media-player', 'stop'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Default to the Android Music folder
    directory = os.path.expanduser('~/storage/music')
    if not os.path.exists(directory):
        directory = os.path.expanduser('~')

    playlist = get_audio_files(directory)
    current_index = 0
    status = "Stopped"
    try:
        while True:
            clear_screen()
            print("=" * 45)
            print("       🎵 Termux CLI MP3 Player 🎵")
            print("=" * 45)
            print(f"📂 Directory: {directory}")
            print(f"🎶 Tracks found: {len(playlist)}\n")

            if playlist:
                current_track = os.path.basename(playlist[current_index])
                # Truncate long file names for better UI
                if len(current_track) > 35:
                    current_track = current_track[:32] + "..."
                print(f"▶ Now Playing: {current_track}")
                print(f"⏯ Status: {status}\n")
            else:
                print("❌ No audio files found in this directory.\n")

            print("1. Play / Pause")
            print("2. Next Track")
            print("3. Previous Track")
            print("4. Stop Playback")
            print("5. Change Directory")
            print("6. Show Full Playlist")
            print("7. Exit")
            print("-" * 45)

            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                if playlist:
                    if status in ["Stopped", "Paused"]:
                        play_file(playlist[current_index])
                        status = "Playing"
                    else:
                        status = pause_resume()

            elif choice == '2':
                if playlist:
                    current_index = (current_index + 1) % len(playlist)
                    play_file(playlist[current_index])
                    status = "Playing"

            elif choice == '3':
                if playlist:
                    current_index = (current_index - 1) % len(playlist)
                    play_file(playlist[current_index])
                    status = "Playing"
            elif choice == '4':
                stop_playback()
                status = "Stopped"

            elif choice == '5':
                new_dir = input("Enter new directory path (e.g., ~/storage/downloads): ").strip()
                new_dir = os.path.expanduser(new_dir)
                if os.path.exists(new_dir):
                    directory = new_dir
                    playlist = get_audio_files(directory)
                    current_index = 0
                    status = "Stopped"
                else:
                    print("❌ Invalid directory!")
                    time.sleep(1.5)

            elif choice == '6':
                clear_screen()
                print("📜 Full Playlist:")
                for i, track in enumerate(playlist):
                    marker = ">> " if i == current_index else "   "
                    track_name = os.path.basename(track)
                    if len(track_name) > 40:
                        track_name = track_name[:37] + "..."
                    print(f"{marker}{i+1:02d}. {track_name}")
                input("\nPress Enter to return to main menu...")

            elif choice == '7':
                stop_playback()
                print("Exiting player. Goodbye! 👋")
                break

            else:
                print("❌ Invalid choice. Please try again.")
                time.sleep(1)

    except KeyboardInterrupt:
        stop_playback()
        print("\nPlayback stopped. Exiting... 👋")
        sys.exit(0)

if __name__ == "__main__":
    main()