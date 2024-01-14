#include <string.h>
#include "buzzer.h"

// Pins
int SERVO1_PIN = 8;
int SERVO2_PIN = 9;
int BUZZER_PIN = 10;

// Moods
int CALM = 0;
int ANXIOUS = 1;
int HAPPY = 2;
int last_mood = "";

void setup() {

}

void loop() {
  // LCD


  // Servos


  // Buzzer
  int received_mood = CALM; // CHANGE FOR PARSING
  if (last_mood != received_mood) {
    int* mood_notes;
    int* mood_dur;
    int array_size;

    if (received_mood == CALM) {
      mood_notes = calm_note;
      mood_dur = calm_dur;
      array_size = sizeof(calm_note) / sizeof(calm_note[0]);
    } else if (received_mood == ANXIOUS) {
      mood_notes = anxious_note;
      mood_dur = anxious_dur;
      array_size = sizeof(anxious_note) / sizeof(anxious_note[0]);
    } else if (received_mood == HAPPY) {
      mood_notes = happy_note;
      mood_dur = happy_dur;
      array_size = sizeof(happy_note) / sizeof(happy_note[0]);
    }

    for (int i = 0; i < array_size; i++) {
      tone(PIN_IN, mood_notes[i], mood_dur[i]);
      delay(mood_dur[i]); // Add delay for note duration
    }

    last_mood = received_mood;
  }
}
