const byte buttons[12] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);

    // Setting all buttons to LOW state
    for (byte i = 0; i <= 12;) {
        pinMode(buttons[i], LOW);
        i++;
    }
}

void getButtonState(byte button) {
    byte buttonState = digitalRead(button);

    if (button < 6) {
        if (buttonState == 1) {
            Serial.print("left$$");
            Serial.print(button);
            Serial.print("\n");
            Serial.println("#");
        }
    }
    else {
        if (buttonState == 1) {
            Serial.print("right$$");
            Serial.print(button-6);
            Serial.print("\n");
            Serial.println("#");
        }
    }
}

void loop() {
    // put your main code here, to run repeatedly:
    for (byte i = 0; i <= 12;) {
        getButtonState(buttons[i]);
    }
}