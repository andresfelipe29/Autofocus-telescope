//Definicion de pines
const int controlPin1 = 2;
const int controlPin2 = 3;
const int enablePin = 9;
const int directionSwitchPin = 4;
const int onOffSwitchStateSwitchPin = 5;
const int potPin = A0;

//Inicializacion de variables
int onOffSwitchState = LOW;
int previousOnOffSwitchState = LOW;
int directionSwitchState = LOW;
int previousDirectionSwitchState = LOW;
int done = 0;
float time_start = 0;
float time_end = 0;
float move_time = 0;
float time_parada = 0;

//Creacion de variables para el motor
int motorEnabled = 0;
int motorSpeed = 0;

//Definicion de salidas y entradas
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1000);
  pinMode(controlPin1, OUTPUT);
  pinMode(controlPin2, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(directionSwitchPin, INPUT); 
  pinMode(onOffSwitchStateSwitchPin, INPUT);
  pinMode(potPin, INPUT);
  analogWrite(enablePin, 0);
}

void loop() {
  //Lee el estado de prendido y la direccion
  onOffSwitchState = digitalRead(onOffSwitchStateSwitchPin);
  directionSwitchState = digitalRead(directionSwitchPin);

  //Prende el motor
  if (onOffSwitchState == HIGH && previousOnOffSwitchState == LOW){
    motorSpeed = analogRead(potPin)/4;
    delay(100);
    Serial.println(1); //Comunica a Python su inicio
    time_start = millis();
    digitalWrite(controlPin1, LOW);
    digitalWrite(controlPin2, HIGH);
    analogWrite(enablePin, motorSpeed);
    previousOnOffSwitchState = HIGH;
  }

//Para el motor
if (directionSwitchState == HIGH && previousDirectionSwitchState == LOW){
  analogWrite(enablePin, 0);
  time_parada = millis() - time_start;
  Serial.println(0); //Comunica a Python su fin
  while (Serial.available() == 0){
    delay(1000);
  }    

//Tiempos
float time_max = 1000.0*Serial.parseFloat();
float move_time = time_parada - time_max; 

//Cambio de direccion
motorSpeed = analogRead(potPin)/4;
digitalWrite(controlPin1, HIGH);
digitalWrite(controlPin2, LOW);
analogWrite(enablePin, motorSpeed);
time_end = millis();

//Condicion para que el motor sepa hasta donde retornar de acuerdo al tiempo enviado por Python
while (millis() - time_end < move_time){}
analogWrite(enablePin, 0); 
while (Serial.available() == 0){}
previousDirectionSwitchState = HIGH;
done = 1;
  
}
}
