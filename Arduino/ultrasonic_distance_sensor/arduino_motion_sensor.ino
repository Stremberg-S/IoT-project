const int DISTANCE_THRESHOLD = 300; // cm
const int TRIGGER_PIN = 9;
const int ECHO_PIN = 10;
const int LED_PIN = 13;

bool cooldown = false;
bool motionState = true;

void setup() {
    Serial.begin(9600);
    pinMode(ECHO_PIN, INPUT);
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    long duration;
    long distance; // cm

    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration / 59;

    // NO MOTION:
    if (distance > DISTANCE_THRESHOLD ) {
        cooldown = false;
        digitalWrite(LED_PIN, LOW);
        if (motionState) {
            Serial.println("No motion..");
            motionState = false;
        }
    }
    // MOTION DETECTED:
    else if (distance <= DISTANCE_THRESHOLD && !cooldown) {
        Serial.print("Motion derected at ");
        Serial.print(distance);
        Serial.println(" cm");
        digitalWrite(LED_PIN, HIGH);
        cooldown = true;
        motionState = true;
    }
    delay(60);
}
