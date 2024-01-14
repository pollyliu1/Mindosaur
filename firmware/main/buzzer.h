#include "pitches.h"
 
// Initalizations
int Q_NOTE = 500;  // 500 miliseconds
int E_NOTE = 250;
int W_NOTE = 1000;
int PIN_IN = 8;

// Mood change note
int calm_note[] = { // longer notes
  NOTE_F5,
  NOTE_E5,
  NOTE_G5
};
int calm_dur[] = {
  Q_NOTE,
  Q_NOTE,
  W_NOTE
};

int anxious_note[] = {
  NOTE_F5,
  NOTE_E5,
  NOTE_DS5,
  NOTE_D5
};
int anxious_dur[] = {
  E_NOTE,
  E_NOTE,
  E_NOTE,
  Q_NOTE
};

int happy_note[] = { // arpeggio
  NOTE_F5,
  NOTE_A5,
  NOTE_C6
};
int happy_dur[] = {
  E_NOTE,
  E_NOTE,
  E_NOTE
};

int amogi_note[] = {
  NOTE_F5,
  NOTE_GS5,
  NOTE_AS5,
  NOTE_B5,
  NOTE_AS5,
  NOTE_GS5,
  NOTE_F5,
  NOTE_DS5,
  NOTE_GS5,
  NOTE_F5,
  NOTE_F4,
  NOTE_F4
};
int amogi_dur[] = {
  Q_NOTE,
  Q_NOTE,
  Q_NOTE,
  Q_NOTE,
  Q_NOTE,
  Q_NOTE,
  W_NOTE,
  E_NOTE,
  E_NOTE,
  W_NOTE,
  Q_NOTE,
  Q_NOTE
};
