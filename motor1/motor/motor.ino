const int motorPin = 9;
String focusing = "null";

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
  //attachInterrupt(digitalPinToInterrupt(switchPin), ISR, RISING);
}

void loop() {
  if (Serial.available() > 0){
    focusing = Serial.readStringUntil('\n');
    if (focusing == "on"){
      digitalWrite(motorPin, HIGH);
      Serial.println("focusing");
    }
    if (focusing == "done"){
      Serial.println("finished");
      focusing = "";
      digitalWrite(motorPin, LOW);
    }
  }  
}
