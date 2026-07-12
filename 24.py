import sys
import time
import random

def type_chorus(line, base_speed=0.07):
    """Types a line like a vocalist: fast for short words, slow for drama."""
    for char in line:
        # --- The "Lyrical" Timing Engine ---
        if char in ".?!":
            time.sleep(0.4)  # The dramatic pause at the end of a phrase
        elif char == ",":
            time.sleep(0.15) # A breath between clauses
        elif char == " ":
            time.sleep(0.04) # Quick breath between words
        
        # Speed up on vowels (feels more energetic), slow down on consonants
        if char.lower() in "aeiou" and char != " ":
            time.sleep(base_speed * 0.6)  # Vowels sing faster
        else:
            time.sleep(base_speed)
        
        # Write the character and force it to display immediately
        sys.stdout.write(char)
        sys.stdout.flush()
        
        # The "Blinking Cursor" illusion (dot after each letter)
        if char != " ":
            sys.stdout.write('\033[5m.\033[0m')  # Flashing dot
            sys.stdout.flush()
            time.sleep(0.02)
            # Backspace to remove the dot
            sys.stdout.write('\b \b')
            sys.stdout.flush()
    
    print()  # Newline after finishing the line
    time.sleep(0.5) # Pause between verses

# --- The Chorus (Rick Astley - Never Gonna Give You Up) ---
lyrics = [
    "Never gonna give you up,",
    "Never gonna let you down,",
    "Never gonna run around and desert you.",
    "Never gonna make you cry,",
    "Never gonna say goodbye,",
    "Never gonna tell a lie and hurt you."
]

print("\033[1;36m")  # Bold Cyan - like a neon sign
print("🎤 KARAOKE MODE ENGAGED 🎤")
print("\033[0m")     # Reset color
time.sleep(1)

for line in lyrics:
    type_chorus(line.upper(), base_speed=0.06)  # UPPERCASE feels like shouting!

print("\033[3;33m")  # Italic Yellow for the final fade-out
print("...and I just rick-rolled your terminal.")
print("\033[0m")