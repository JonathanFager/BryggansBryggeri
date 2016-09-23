#include <Wire.h>
#include <SoftwareSerial.h>
#include <Suli.h>
#include <Four_Digit_Display_Arduino.h>

// Include the libraries we need
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

#include "DHT.h"

#define DHTPIN 5    // what pin we're connected to

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);


Four_Digit_Display_Arduino    disp;

int character1;
int character2;
int character3;
int character4;
int character5;
int character6;
int character7;
int character8;

int temperature = 22; // temperature of the liquid
int temperature2 = 22; // temperature in the room

int temperatureDHTlast;

int temperatureDHT1;
int temperatureDHT2;
int temperatureDHT3;
int temperatureDHT4;
int temperatureDHT5;
int temperatureDHT6;
int temperatureDHT7;
int temperatureDHT8;
int temperatureDHT9;
int temperatureDHT10;

int delayWrite1;
int delayWrite2;


void setup()
{
  Serial.begin(9600);
  sensors.begin();
  dht.begin();
  disp.begin(6, 7);
  disp.pointOn ();

  pinMode (A1, OUTPUT);
  pinMode (A5, OUTPUT);
}

void displaycharacter () {

  if (temperature <= 9) {
    character1 = 0;
    character2 = temperature - 0;
  }

  else if (temperature <= 19) {
    character1 = 1;
    character2 = temperature - 10;
  }

  else if (temperature <= 29) {
    character1 = 2;
    character2 = temperature - 20;
  }

  else if (temperature <= 39) {
    character1 = 3;
    character2 = temperature - 30;
  }

  else if (temperature <= 49) {
    character1 = 4;
    character2 = temperature - 40;
  }

  else if (temperature <= 59) {
    character1 = 5;
    character2 = temperature - 50;
  }

  else if (temperature <= 69) {
    character1 = 6;
    character2 = temperature - 60;
  }

  else if (temperature <= 79) {
    character1 = 7;
    character2 = temperature - 70;
  }

  else if (temperature <= 89) {
    character1 = 8;
    character2 = temperature - 80;
  }

  else if (temperature <= 99) {
    character1 = 9;
    character2 = temperature - 90;
  }

  else if (temperature >= 100) {
    character1 = 9;
    character2 = 9;
  }


}

void displaycharacter2 () {

  if (temperature2 <= 9) {
    character5 = 0;
    character6 = temperature2 - 0;
  }

  else if (temperature2 <= 19) {
    character5 = 1;
    character6 = temperature2 - 10;
  }

  else if (temperature2 <= 29) {
    character5 = 2;
    character6 = temperature2 - 20;
  }

  else if (temperature2 <= 39) {
    character5 = 3;
    character6 = temperature2 - 30;
  }

  else if (temperature2 <= 49) {
    character5 = 4;
    character6 = temperature2 - 40;
  }

  else if (temperature2 <= 59) {
    character5 = 5;
    character6 = temperature2 - 50;
  }

  else if (temperature2 <= 69) {
    character5 = 6;
    character6 = temperature2 - 60;
  }

  else if (temperature2 <= 79) {
    character5 = 7;
    character6 = temperature2 - 70;
  }

  else if (temperature2 <= 89) {
    character5 = 8;
    character6 = temperature2 - 80;
  }

  else if (temperature2 <= 99) {
    character5 = 9;
    character6 = temperature2 - 90;
  }

  else if (temperature2 >= 100) {
    character5 = 9;
    character6 = 9;
  }
}

void lcd1 () {

  disp.begin(6, 7);
  disp.display(0, character1);
  disp.display(1, character2);
  disp.display(2, character3);
  disp.display(3, character4);

}

void lcd2 () {

  disp.begin(8, 9);
  disp.display(0, character5);
  disp.display(1, character6);
  disp.display(2, character7);
  disp.display(3, character8);
}

void loop() {
  sensors.requestTemperatures();
  temperature = sensors.getTempCByIndex(0);
  temperatureDHT1 = dht.readTemperature();
  temperature2 = (((temperatureDHT1 + temperatureDHT2 + temperatureDHT3 + temperatureDHT4 + temperatureDHT5 + temperatureDHT6 + temperatureDHT7 + temperatureDHT8 + temperatureDHT9 + temperatureDHT10) / 10)  + temperatureDHTlast) / 2;
  //take the average of the last ten temperature readings of the dht11, we do this to get a more consistent result. On average the dht is accurate but individual readings are aweful.  Then calculate the average of the last 2 averages for a stable result.
  // I added 0,7 to the end result because my readings were consitently a bit lowish.
  //just dont buy the dht11 to be honest, by ANYTHING ELSE
  temperatureDHTlast = temperature2;
  Serial.println (temperature);
  Serial.println(temperature2);
  Serial.println(delayWrite1);
  Serial.println(delayWrite2);
  
  
  displaycharacter () ;
  delay(100);
  lcd1();
  delay(100);
  displaycharacter2 ();
  delay(100);
  lcd2();
  delay(100);

  //MOVE ALL THE PREVIOUS TEMPERATUREREADINGS OF THE DHT11 ONE SPOT UP:

  temperatureDHT10 = temperatureDHT9;
  temperatureDHT9 = temperatureDHT8;
  temperatureDHT8 = temperatureDHT7;
  temperatureDHT7 = temperatureDHT6;
  temperatureDHT6 = temperatureDHT5;
  temperatureDHT5 = temperatureDHT4;
  temperatureDHT4 = temperatureDHT3;
  temperatureDHT3 = temperatureDHT2;
  temperatureDHT2 = temperatureDHT1;

  //The communication code from NANO to WEMOS
  // This code sends a HIGH to one of the wemos,s digital ports for the duration of temperature in Celcius times 100. example: 22 degrees equals a 2200 ms pulse. We use a normal delay function for this.
  //The wemos counts how long it is being pulsed and divides the number back by 100 to get the last temperature readings from the NANO.

  delayWrite1 = temperature * 100;
  delayWrite2 = temperature2 * 100;

  digitalWrite (A1, HIGH);
  delay(delayWrite1);
  digitalWrite (A1, LOW);


//  digitalWrite (A5, HIGH);
//  delay(delayWrite2);
//  digitalWrite (A5, LOW);

}



