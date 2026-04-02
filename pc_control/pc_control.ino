#define CLK  2
#define DT   3
#define SW   4
#define BTN1 5
#define BTN2 6
#define BTN3 7
#define BTN4 8
#define POT  A0

volatile bool turned = false;
volatile bool direction = true;
bool lastSW   = HIGH;
bool lastBtn1 = HIGH, lastBtn2 = HIGH, lastBtn3 = HIGH, lastBtn4 = HIGH;
int lastBrightness = -1;
unsigned long lastPotRead = 0;

void encoderISR() {
  direction = (digitalRead(DT) == HIGH);
  turned = true;
}

void setup() {
  Serial.begin(9600);
  pinMode(CLK,  INPUT_PULLUP);
  pinMode(DT,   INPUT_PULLUP);
  pinMode(SW,   INPUT_PULLUP);
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);
  pinMode(BTN3, INPUT_PULLUP);
  pinMode(BTN4, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(CLK), encoderISR, FALLING);
  Serial.println("Ready!");
}

void loop() {
  // Encoder rotation
  if (turned) {
    turned = false;
    Serial.println(direction ? "CW" : "CCW");
  }

  // Encoder button (mute)
  bool sw = digitalRead(SW);
  if (sw == LOW && lastSW == HIGH) { Serial.println("BTN"); delay(50); }
  lastSW = sw;

  // Potentiometer — read only every 200ms with deadband of 5
  if (millis() - lastPotRead > 200) {
    lastPotRead = millis();

    // Average 5 readings to reduce noise
    int raw = 0;
    for (int i = 0; i < 5; i++) {
      raw += analogRead(POT);
      delay(2);
    }
    raw /= 5;

    int brightness = map(raw, 0, 1023, 0, 100);
    if (abs(brightness - lastBrightness) > 5) {  // deadband increased to 5
      Serial.print("BRIGHT:");
      Serial.println(brightness);
      lastBrightness = brightness;
    }
  }

  // Push buttons
  bool b1 = digitalRead(BTN1);
  bool b2 = digitalRead(BTN2);
  bool b3 = digitalRead(BTN3);
  bool b4 = digitalRead(BTN4);

  if (b1 == LOW && lastBtn1 == HIGH) { Serial.println("PLAY");  delay(50); }
  if (b2 == LOW && lastBtn2 == HIGH) { Serial.println("NEXT");  delay(50); }
  if (b3 == LOW && lastBtn3 == HIGH) { Serial.println("PREV");  delay(50); }
  if (b4 == LOW && lastBtn4 == HIGH) { Serial.println("BRAVE"); delay(50); }

  lastBtn1 = b1; lastBtn2 = b2; lastBtn3 = b3; lastBtn4 = b4;

  delay(1);
}