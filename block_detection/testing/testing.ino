void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  for (byte i = 0; i <= 12;) {
    pinMode(buttons[i], LOW);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("left$$0");
  Serial.println("#");
  delay(5000);

  Serial.println("left$$1");
  Serial.println("#");
  delay(5000);

  Serial.println("left$$2");
  Serial.println("#");
  delay(5000);

  Serial.println("left$$3");
  Serial.println("#");
  delay(5000);

  Serial.println("left$$4");
  Serial.println("#");
  delay(5000);

  Serial.println("left$$5");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$0");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$1");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$2");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$3");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$4");
  Serial.println("#");
  delay(5000);

  Serial.println("right$$5");
  Serial.println("#");
  delay(5000);
}
