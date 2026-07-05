import random
import sys

# Word pairs (civilian, spy)
WORD_PAIRS = [
    ("beach", "pool"),
    ("restaurant", "café"),
    ("airport", "train station"),
    ("library", "bookstore"),
    ("park", "garden"),
    ("kitchen", "bathroom"),
    ("car", "bicycle"),
    ("dog", "cat"),
    ("pizza", "pasta"),
    ("summer", "winter"),
]

# Player names
PLAYERS = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

# Clue templates – each bot generates a clue by filling in their word
CLUE_TEMPLATES = [
    "I think of {} when I relax.",
    "{} is my favourite place.",
    "You can find me at {}.",
    "I love the smell of {}.",
    "{} reminds me of holidays.",
    "I often go to {}.",
    "{} makes me happy.",
    "I associate {} with fun.",
    "The best thing about {} is the atmosphere.",
    "I could spend hours at {}.",
]

def show_instructions():
    print("\n" + "=" * 50)
    print("🔍  WHO'S THE SPY? — A deduction game")
    print("=" * 50)
    print("""
How it works:
  • 5 players are secretly given a word.
  • All except one get the SAME civilian word.
  • The odd one out (the SPY) gets a different, similar word.
  • Each player gives a one‑sentence clue about their word.
  • Your task: read the clues carefully and GUESS who the spy is.

You only get ONE guess – so pay attention!

The players are: """ + ", ".join(PLAYERS) + """

Type the full name of the player you think is the spy.
Good luck!
""")
    input("Press Enter to start the game...")
    print("\n" + "─" * 50 + "\n")

def pick_word_pair():
    return random.choice(WORD_PAIRS)

def assign_roles(players, civilian_word, spy_word):
    spy_index = random.randrange(len(players))
    roles = {}
    for i, name in enumerate(players):
        roles[name] = spy_word if i == spy_index else civilian_word
    return roles, spy_index

def generate_clue(word):
    template = random.choice(CLUE_TEMPLATES)
    return template.format(word)

def main():
    show_instructions()

    # Setup
    civilian_word, spy_word = pick_word_pair()
    roles, spy_index = assign_roles(PLAYERS, civilian_word, spy_word)
    spy_name = PLAYERS[spy_index]

    # Bot clues (shuffled order)
    order = PLAYERS.copy()
    random.shuffle(order)

    print("📝 Each bot gives a clue about their word. Read carefully!\n")
    for name in order:
        clue = generate_clue(roles[name])
        print(f"  {name}: \"{clue}\"")

    print("\n" + "─" * 40)

    # Player guesses
    while True:
        guess = input("\n👉 Who is the spy? (Type a name): ").strip().title()
        if guess in PLAYERS:
            break
        print(f"❌ Invalid name. Choose from: {', '.join(PLAYERS)}")

    # Reveal
    print("\n" + "─" * 40)
    if guess == spy_name:
        print(f"✅ Correct! {spy_name} was the spy (word: {spy_word}).")
    else:
        print(f"❌ Wrong! The spy was {spy_name} (word: {spy_word}).")
    print(f"   Civilian word was: {civilian_word}")

    print("\nThanks for playing!\n")

if __name__ == "__main__":
    main()