import random
import sys

class GuessNumberGame:
    def __init__(self):
        self.total_score = 0
        self.rounds_played = 0
        self.difficulties = {
            'easy': {'range': (1, 50), 'attempts': 10},
            'medium': {'range': (1, 100), 'attempts': 7},
            'hard': {'range': (1, 200), 'attempts': 5}
        }

    def choose_difficulty(self):
        """Prompt user to select difficulty and return settings."""
        while True:
            print("\nChoose difficulty:")
            print("  (E)asy – numbers 1-50, 10 attempts")
            print("  (M)edium – numbers 1-100, 7 attempts")
            print("  (H)ard – numbers 1-200, 5 attempts")
            choice = input("Enter E, M, or H: ").strip().lower()
            
            if choice == 'e':
                return 'easy'
            elif choice == 'm':
                return 'medium'
            elif choice == 'h':
                return 'hard'
            else:
                print("Invalid choice. Please try again.")

    def play_round(self):
        """Run one round of the guessing game."""
        diff = self.choose_difficulty()
        settings = self.difficulties[diff]
        low, high = settings['range']
        max_attempts = settings['attempts']
        secret = random.randint(low, high)
        attempts_left = max_attempts

        print(f"\nI'm thinking of a number between {low} and {high}.")
        print(f"You have {max_attempts} attempts. Good luck!")

        while attempts_left > 0:
            print(f"\nAttempts remaining: {attempts_left}")
            try:
                guess = int(input("Your guess: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if guess < low or guess > high:
                print(f"Your guess must be between {low} and {high}.")
                continue

            attempts_left -= 1

            if guess == secret:
                # Calculate points: base 10 + bonus for remaining attempts
                points = 10 + attempts_left * 2
                self.total_score += points
                self.rounds_played += 1
                print(f"🎉 Correct! The number was {secret}.")
                print(f"You earned {points} points! (Total: {self.total_score})")
                return
            elif guess < secret:
                print("Too low!")
            else:
                print("Too high!")

        # Out of attempts
        print(f"\n😞 Out of attempts! The number was {secret}.")
        print(f"Better luck next time. Total score: {self.total_score}")

    def play_again(self):
        """Ask if user wants another round."""
        while True:
            again = input("\nPlay another round? (y/n): ").strip().lower()
            if again == 'y':
                return True
            elif again == 'n':
                return False
            else:
                print("Please enter 'y' or 'n'.")

    def run(self):
        """Main game loop."""
        print("=" * 40)
        print("   Welcome to Guess the Number!")
        print("=" * 40)
        print("Try to guess the secret number in as few attempts as possible.")
        print("Earn points for each correct guess – more points for fewer attempts!")
        
        while True:
            self.play_round()
            if not self.play_again():
                break

        print("\nThanks for playing!")
        print(f"Rounds played: {self.rounds_played}")
        print(f"Final score: {self.total_score}")
        print("Goodbye!")

if __name__ == "__main__":
    game = GuessNumberGame()
    game.run()