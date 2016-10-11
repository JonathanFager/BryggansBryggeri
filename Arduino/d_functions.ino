

//BLYNK SERVERS ONLY ALLOW 10 REQUESTS PER SECOND. IF YOU MAKE MORE REQUESTS YOUR PROJECT WILL BE DISCONNECTED AND RECONNECTED CAUSING A LOT OF APPLICATIONS TO CRASH.
//THAT IS WHY WE CALL 3 DIFFERENT FUNCTIONS HERE TO ENSURE ONLY A LIMITED AMOUNT OF REQUESTS IS MADE EVERY SECOND.



void blynkUpdate1 () {

  if ((timeNow - timeBlynkLast) > 5 && blynkCalled == 0) {

    Blynk.virtualWrite(9, minutesCounter);
    Blynk.virtualWrite(2, heater1);
    Blynk.virtualWrite(4, heater2);
    Blynk.virtualWrite(5, minutes);
    Blynk.virtualWrite(10, temperature);

    blynkCalled = 1;

  }

}




void blynkUpdate2 () {

  if ((timeNow - timeBlynkLast) > 10 && blynkCalled == 1) {

    Blynk.virtualWrite(6, brewStage);
    Blynk.virtualWrite(7, temperature);
   // Blynk.virtualWrite(8, timeEstimate);
    blynkCalled = 2;

  }

}

void blynkUpdate3 () {

  if ((timeNow - timeBlynkLast) > 15 && blynkCalled == 2) {


    lcd.clear();
    lcd.print(0, 0, LCD1); // use: (position X: 0-15, position Y: 0-1, "Message you want to print")
    lcd.print(0, 1, LCD2); // use: (position X: 0-15, position Y: 0-1, "Message you want to print")
    timeBlynkLast = timeNow;
    blynkCalled = 0;
  }
}


////THE FUNCTIONS BELOW READ THE VALUES OF THE SLIDE BARS IN THE APP - THIS IS NOT STABLE YET, UNCOMMENT AT OWN RISK
//BLYNK_WRITE(V30)
//{
//  boilTemp = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V31)
//{
//mashTemp =  param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V37)
//{
//  liters = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V32)
//{
//  yeastPitchTemperature = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V33)
//{
//  fermentationTemperatureMax = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V34)
//{
//  fermentTimeprimary = param.asInt(); 
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V35)
//{
//  mashTime = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V36)
//{
//  boilTime = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//BLYNK_WRITE(V40)
//{
//  HopTime1= param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V41)
//{
//  HopTime2 = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V42)
//{
//  HopTime3 = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}
//
//BLYNK_WRITE(V43)
//{
//  HopTime4 = param.asInt();
//  Serial.println(param.asInt());
//  // You can also use:
//  // int i = param.asInt() or
//  // double d = param.asDouble()
//}





//function buzzer, to be written


void temperatureFunction2 () {
  timeNowNano = millis();
  button2 = digitalRead(D0);

  if (button2 == HIGH && buttonPrevious2 == LOW) {
    timeLastNano = timeNowNano;
    buttonPrevious2 = HIGH;
  }

  else if (button2 == LOW && buttonPrevious2 == HIGH) {
    message2 = (timeNowNano - timeLastNano) / 100;
    buttonPrevious2 = LOW;
  }

 

//
//
//Serial.print("button2           ");
//  Serial.println(button2);
////
// Serial.print("Message2           :");
// Serial.println(message2);


}


void IceFunction () {

  iceNeeded = liters / 2;


}
//This function tells you how much ice you need to cool your boiling wort
// The formula may seem simple here, but it is dependant on many factors and not 100 procent accurate. A lot of research went into this easy formula. According to http://hyperphysics.phy-astr.gsu.edu/hbase/thermo/cice.html
// the phase change caused by adding 50% ice to your total volume, makes the temperature drop from 100 Celsius to 40 Celsius very fast
//The remaing temperature will be dropped by vapor, the difference in temperature with the ice,the pouring to the fermenter and the difference in temperature with roomtemperature.
//The risk of off flavors is also reduced significantly one the wort is cooled under 50 degrees celcius, so those last 30 degrees can take a little longer

//NOTE: THE ICE SHOULD BE ADDED IN THE FORM OF FROZEN BOTTLES, SO THAT YOU CAN TAKE THEM OUT AFTERWARDS WITHOUT DILUTING YOUR WORT.
