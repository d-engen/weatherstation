const int sensorPin = A0;   // Anslut vindmätaren till A0
const float vRef = 3.3;     // Referensspänning (för Arduino Uno är det normalt 5V)
const int adcMax = 1023;    // 10-bitars ADC (0–1023)
float last_windspeed = 1.0;
void setup() {
  Serial.begin(9600);
  analogReference(EXTERNAL); //Använder 3.3 som A
}

void loop() {
  int rawValue = analogRead(sensorPin);       // Läs råvärde
  float voltage = (rawValue * vRef) / adcMax; // Räkna om till spänning
  float windSpeed = (voltage - 0.4) * 20.25;  // Räkna om till m/s

  // Se till att inte få negativa värden
  if (windSpeed < 0.14) windSpeed = 0;
  if (windSpeed > 32.4) windSpeed = last_windspeed;

  Serial.println(windSpeed, 1);
  last_windspeed = windSpeed;

  delay(500);  // uppdatera var 0.5 s
}