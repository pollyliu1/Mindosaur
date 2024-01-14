#include "pitches.h"
 
// Initalizations
int Q_NOTE = 500;  // 500 miliseconds
int E_NOTE = 250;
int PIN_IN = 8;

// Mood change note
int calm_note[] = {
  NOTE_A5
};
int calm_dur[] = {
  Q_NOTE
};

int anxious_note[] = {
  NOTE_A5
};
int anxious_dur[] = {
  Q_NOTE
};

int happy_note[] = {
  NOTE_F5,
  NOTE_AS5
};
int happy_dur[] = {
  Q_NOTE,
  E_NOTE
};
