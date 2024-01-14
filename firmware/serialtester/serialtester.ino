#include <LiquidCrystal.h>
#include <string.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int x;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  // Setup lcd
  lcd.begin(16, 2);
  // Setup contrast
  analogWrite(6,150);
  lcd.print("Ready");
}
void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  lcd.print(String(x));
}