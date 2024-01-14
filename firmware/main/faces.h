#include <LiquidCrystal.h>
#include <Servo.h>

/*
  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
*/

void calm_face(LiquidCrystal lcd, Servo left, Servo right) {
  // Eyes
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("     .    .     ");
  lcd.setCursor(0, 1);
  lcd.print("       __      ");

  // Eyebrows
  left.write(90);
  right.write(90);
}

void anxious_face(LiquidCrystal lcd, Servo left, Servo right) {
  // Eyes
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   >        <   ");
  lcd.setCursor(0, 1);
  lcd.print("       MM      ");

  // Eyebrows
  left.write(120);
  right.write(60);
}

void happy_face(LiquidCrystal lcd, Servo left, Servo right) {
  // Eyes
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  ^          ^   ");
  lcd.setCursor(0, 1);
  lcd.print(" °    __    ° ");
 
  // Eyebrows
  left.write(110);
  right.write(70);
}

