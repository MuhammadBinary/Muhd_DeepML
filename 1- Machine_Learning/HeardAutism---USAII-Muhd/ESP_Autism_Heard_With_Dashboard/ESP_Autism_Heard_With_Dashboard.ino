#include <LedControl.h>

LedControl lc = LedControl(12, 11, 10, 1);

// -------------- ANIMATIONS - 2 frames each -------------------------

byte happy[2][8] = {
  {0x3C, 0x42, 0xA5, 0x81, 0xBD, 0x81, 0x42, 0x3C},
  {0x3C, 0x42, 0xA5, 0x81, 0xA5, 0x99, 0x42, 0x3C}
};

byte angry[2][8] = {
  {0x3C, 0x42, 0xA5, 0x81, 0xBD, 0x81, 0x42, 0x3C},
  {0x3C, 0x42, 0xA5, 0x81, 0x99, 0xA5, 0x42, 0x3C}
};

byte neutral[2][8] = {
  {0x3C, 0x42, 0x81, 0xA5, 0x81, 0xBD, 0x42, 0x3C},
  {0x3C, 0x42, 0x81, 0xA5, 0x81, 0xBD, 0x42, 0x3C}
};

// -------------------------- STATE ----------------------------
char currentEmotion = 'N';
int  frameIdx       = 0;
unsigned long lastFrame = 0;

int getSpeed() {
  if (currentEmotion == 'H') return 600;
  if (currentEmotion == 'A') return 600;
  return 800;
}

void showFrame(byte frame[8]) {
  for (int row = 0; row < 8; row++) {
    lc.setRow(0, row, frame[row]);
  }
}

void setup() {
  Serial.begin(9600);

  lc.shutdown(0, false);
  lc.setIntensity(0, 10);
  lc.clearDisplay(0);

  // Startup sweep
  for (int i = 0; i < 8; i++) {
    lc.setRow(0, i, 0xFF);
    delay(80);
  }
  delay(400);
  lc.clearDisplay(0);

  showFrame(neutral[0]);
}

void loop() {
  // Read serial
  char cmd = 0;
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'H' || c == 'A' || c == 'N') {
      cmd = c;
    }
  }

  if (cmd != 0 && cmd != currentEmotion) {
    currentEmotion = cmd;
    frameIdx = 0;  // reset animation on emotion change
  }

  // Advance animation frame
  unsigned long now = millis();
  if (now - lastFrame > getSpeed()) {
    lastFrame = now;
    frameIdx = (frameIdx + 1) % 2;

    if      (currentEmotion == 'H') showFrame(happy[frameIdx]);
    else if (currentEmotion == 'A') showFrame(angry[frameIdx]);
    else                            showFrame(neutral[frameIdx]);
  }
}
