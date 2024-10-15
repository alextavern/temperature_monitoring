  const int sensorPin = A0;
  const float baselineTemp = 20.0;

void setup() {
  // setup arduino port
  Serial.begin(9600);

}

void loop() { 
  
  // setup temperature sensor output data stream
  // output value between 0 and 1023 (10bits)
  int sensorVal = analogRead(sensorPin);
  //Serial.print("Sensor Value: ");
  //Serial.print(sensorVal);

  // convert to voltage (it is 0 to 5 Volts)
  float voltage = (sensorVal/1024.0) * 5.0;
  //Serial.print(", Volts: ");
  //Serial.print(voltage);

  //convert to celcius (deltaV=0.5 mV -> 1 deg)
  float temperature = (voltage - .5) * 100;
  Serial.print("Temperature (C): ");
  Serial.print(temperature);
  Serial.print("\n");
  
  // one measurement every 2 secs
  delay(2000);

}
