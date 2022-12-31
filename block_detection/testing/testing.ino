void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i<=360 ; i++) {
    int rand = random(1, 2);
    int randplot;
    switch (rand) {
      case 1:
        randplot = random(5);
        Serial.print("left$$");
        Serial.print(randplot);
        Serial.print("$$");
        Serial.print(i);
        Serial.print("\n");
        Serial.println("#");
        delay(1000);
      case 2:
        randplot = random(5);
        Serial.print("right$$");
        Serial.print(randplot);
        Serial.print("$$");
        Serial.print(i);
        Serial.print("\n");
        Serial.println("#");
        delay(1000);
    }
  }
}