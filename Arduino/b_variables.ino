
unsigned long timeNow = 0;
unsigned long timeLast = 0;
int timeBlynkLast;
int blynkCalled;
int hours = startingHour;
int minutesCounter = 0;  
int timeEstimate = 0;
int timeTemp = 0;
int temperature;

int hop = 1; 

int buzzer = 0;

int heater1 = 0;
int heater2 = 0;

int heaterElement1 = D3;
int heaterElement2 = D4;

int heaterBlynk1 = LOW;

int iceNeeded = liters;

int switchState = 0;
int switch1 = 0;
 
//TEMPERATURE SENSOR NANO

int button;
int buttonPrevious = LOW;
int LED1  ;
int LED2 ;

int message = 23;
int message2 = 23;

int button2;
int buttonPrevious2 = LOW;

long timeNowNano;
long timeLastNano;

String LCD1 = "HELLO WORLD";
String LCD2 = "HELLO WORLD";



