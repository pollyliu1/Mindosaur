#include <string.h>
#include "buzzer.h"
#include "faces.h"

// Pins
int SERVO1_PIN = 8;
int SERVO2_PIN = 9;
int BUZZER_PIN = 10;

// Moods
int CALM = 0;
int ANXIOUS = 1;
int HAPPY = 2;
int last_mood = "";

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo left, right;

void setup() {
  // LCD setup
  lcd.begin(16, 2);
  // Set up contrast
  analogWrite(6,150);

  // Servo setup
  left.attach(SERVO1_PIN);
  right.attach(SERVO2_PIN);

  // Face
  calm_face(lcd, left, right);

  // Amogi Setup (sound)
  // int array_size = sizeof(amogi_note) / sizeof(amogi_note[0]);
  // for (int i = 0; i < array_size; i++) {
  //   tone(BUZZER_PIN, amogi_note[i], amogi_dur[i]);
  //   delay(amogi_dur[i]); // Add delay for note duration
  // }

  delay(10000); // 10 seconds
}

void loop() {
  // LCD


  // Servos


  // Buzzer
  // int received_mood = CALM; // CHANGE FOR PARSING
  // if (last_mood != received_mood) {
  //   int* mood_notes;
  //   int* mood_dur;
  //   int array_size;

  //   if (received_mood == CALM) {
  //     mood_notes = calm_note;
  //     mood_dur = calm_dur;
  //     array_size = sizeof(calm_note) / sizeof(calm_note[0]);
  //   } else if (received_mood == ANXIOUS) {
  //     mood_notes = anxious_note;
  //     mood_dur = anxious_dur;
  //     array_size = sizeof(anxious_note) / sizeof(anxious_note[0]);
  //   } else if (received_mood == HAPPY) {
  //     mood_notes = happy_note;
  //     mood_dur = happy_dur;
  //     array_size = sizeof(happy_note) / sizeof(happy_note[0]);
  //   }

  //   for (int i = 0; i < array_size; i++) {
  //     tone(BUZZER_PIN, mood_notes[i], mood_dur[i]);
  //     delay(mood_dur[i]); // Add delay for note duration
  //   }

  //   last_mood = received_mood;
  // }
}
