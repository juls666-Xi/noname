// Detonator control firmware for Arduino Uno/Nano
// Pin 13: LED status indicator
// Pin 12: Armed/Disarmed switch input (HIGH = armed)
// Pin 9: Relay/igniter output (HIGH = fire)
// Pin 2: Trigger button input (pull-down, fire when pressed and armed)

const int LED_PIN = 13;
const int ARM_PIN = 12;
const int FIRE_PIN = 9;
const int TRIGGER_PIN = 2;

bool armed = false;
bool fired = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(ARM_PIN, INPUT_PULLUP);   // internal pull-up, LOW when switch to ground
  pinMode(FIRE_PIN, OUTPUT);
  pinMode(TRIGGER_PIN, INPUT_PULLDOWN); // external pull-down, HIGH when button pressed
  
  digitalWrite(FIRE_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(9600);
}

void loop() {
  // Read arm switch (LOW = armed because of pull-up and switch to ground)
  bool current_arm = (digitalRead(ARM_PIN) == LOW);
  
  if (current_arm && !armed && !fired) {
    armed = true;
    digitalWrite(LED_PIN, HIGH);
    Serial.println("ARMED");
  } else if (!current_arm && armed) {
    armed = false;
    digitalWrite(LED_PIN, LOW);
    Serial.println("DISARMED");
  }
  
  // Trigger when armed and trigger button pressed and not already fired
  bool trigger = digitalRead(TRIGGER_PIN);
  if (armed && trigger && !fired) {
    fired = true;
    digitalWrite(FIRE_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);  // blink? Keep high to indicate fired
    Serial.println("FIRED");
    delay(5000);                  // keep output high for 5 seconds
    digitalWrite(FIRE_PIN, LOW);  // safe after delay
    armed = false;
  }
  
  delay(50);
}