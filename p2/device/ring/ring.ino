void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(12, INPUT);
  pinMode(13, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(13, LOW);
  digitalWrite(4, HIGH);
}

char rx_byte = 0;

void loop() {
  // put your main code here, to run repeatedly:
  if ((rx_byte == 0) && (digitalRead(13)== HIGH)){
        Serial.println("Anomaly");
  }
  if (digitalRead(12) == HIGH) {
        Serial.println("Knock");
        delay(5000);
  }
  if (Serial.available() > 0) {
    rx_byte = Serial.read();
    if ((rx_byte > '0')){
        digitalWrite(13, HIGH);
        Serial.println("Open");
        delay(5000);
        digitalWrite(13, LOW);
        Serial.println("Close");
      } else if ((rx_byte == '0')) {
        digitalWrite(13, LOW);
        Serial.println("Close");
        delay(100); 
      }
      rx_byte = 0;
  }
  delay(100);
}
