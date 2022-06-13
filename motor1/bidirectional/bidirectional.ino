//pins
const int controlPin1 = 2;
const int controlPin2 = 3;
const int enablePin = 9;
const int potPin = A0;

//input variables
String onOffState = "of";
String directionState = "cl";
String prev_onOffState = "of";
String prev_directionState = "cl";
String state = "";

//motor control variables
int motorEnabled = 0;
int motorSpeed = 0;
int motorDirection = 1;

void setup() {
  Serial.begin(9600);
  pinMode(controlPin1, OUTPUT);
  pinMode(controlPin2, OUTPUT);
  pinMode(enablePin, OUTPUT);
  state = Serial.readStringUntil('\n');
  onOffState = state.substring(0,2);
  directionState = state.substring(3,5);
  digitalWrite(enablePin, LOW);
}

void loop() {
  while (Serial.available() == 0){}
  state = Serial.readStringUntil('\n');
  Serial.print("Motor state: " + state);
  onOffState = state.substring(0,2);
  directionState = state.substring(3,5);

  //set motor speed
  motorSpeed = analogRead(potPin)/4;

  //Turn motor on or off
  if (onOffState != prev_onOffState){
    motorEnabled = !motorEnabled;
    prev_onOffState = onOffState;
  }
  
  //Change spinning direction
  if (directionState != prev_directionState){
    motorDirection = !motorDirection;
    prev_directionState = directionState;
  }
  
  //Set spinning direction
  if (motorDirection == 1){
    digitalWrite(controlPin1, LOW);
    digitalWrite(controlPin2, HIGH);
  } else {
    digitalWrite(controlPin1, HIGH);
    digitalWrite(controlPin2, LOW);
  }
  
  //Tell the motor how fast to spin
  if (motorEnabled == 1){
    analogWrite(enablePin, motorSpeed);  
  } else {
    analogWrite(enablePin, 0);  
  }
}
