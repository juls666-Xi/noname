import time
import random

class DisposableVape:
    def __init__(self, battery_capacity_mah=280, liquid_ml=2.0, max_puffs=300):
        self.battery_capacity = battery_capacity_mah   # mAh
        self.battery = battery_capacity_mah            # current charge
        self.liquid = liquid_ml                        # mL remaining
        self.max_puffs = max_puffs
        self.puffs_taken = 0
        self.led_color = "green"
        self.is_active = True

    def _update_led(self):
        """Change LED color based on battery level."""
        percent = (self.battery / self.battery_capacity) * 100
        if percent > 50:
            self.led_color = "green"
        elif 20 < percent <= 50:
            self.led_color = "blue"
        elif 5 < percent <= 20:
            self.led_color = "yellow"
        else:
            self.led_color = "red"

    def puff(self):
        """Simulate taking a puff."""
        if not self.is_active:
            print("❌ Vape is dead. Replace it.")
            return False

        # Check resources
        if self.battery <= 0:
            print("🔋 Battery depleted. Vape is dead.")
            self.is_active = False
            return False

        if self.liquid <= 0:
            print("💧 No e-liquid left. Vape is dead.")
            self.is_active = False
            return False

        if self.puffs_taken >= self.max_puffs:
            print("⛔ Maximum puff count reached. Vape is dead.")
            self.is_active = False
            return False

        # Consume resources (randomised for realism)
        battery_used = random.uniform(0.8, 1.2)   # mAh per puff
        liquid_used = random.uniform(0.005, 0.015) # mL per puff

        self.battery = max(0, self.battery - battery_used)
        self.liquid = max(0, self.liquid - liquid_used)
        self.puffs_taken += 1

        self._update_led()
        print(f"💨 Puff #{self.puffs_taken} | LED: {self.led_color.upper()} | "
              f"Battery: {self.battery:.1f} mAh | Liquid: {self.liquid:.2f} mL")
        return True

    def status(self):
        """Display current status."""
        print("\n--- Vape Status ---")
        print(f"Puffs taken: {self.puffs_taken}/{self.max_puffs}")
        print(f"Battery: {self.battery:.1f} mAh ({self.battery/self.battery_capacity*100:.0f}%)")
        print(f"Liquid: {self.liquid:.2f} mL")
        print(f"LED: {self.led_color.upper()}")
        print(f"Active: {self.is_active}")
        print("--------------------\n")

# --- Interactive CLI ---
def main():
    vape = DisposableVape()
    print("🖥️  Disposable Vape Simulator")
    print("Commands: puff | status | reset | quit")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "puff":
            vape.puff()
        elif cmd == "status":
            vape.status()
        elif cmd == "reset":
            vape = DisposableVape()
            print("🔄 Vape reset to factory state.")
        elif cmd == "quit":
            break
        else:
            print("Unknown command. Try: puff, status, reset, quit")

if __name__ == "__main__":
    main()