#include <LiquidCrystal.h>

//pins for lcd
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

//initial states
int iState;
int iState2;

//pins for sensors
int thermistorPin = A0;
int waterLevelPin = A1;
int powerAndOut = 6;

//global values for thermistor
int vO;
float R1 = 10000;
float logR2, R2, T, Tc, Tf;
//constants for NTC sensors
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

unsigned long long lasttime;

//global values for water level sensor
int val = 0;
int level;


void setup() {
  // put your setup code here, to run once:
  //configuration of pin
  pinMode(powerAndOut, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3,OUTPUT);
  digitalWrite(powerAndOut, LOW);
  //initialization of serial communication
  Serial.begin(9600);
  //initialialization of LCD  
  lcd.begin(16, 2);
  iState = 0;
  iState2 = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //every ten seconds to avoid throttle on adafruit
  if (millis() - lasttime > 5000){
    lasttime = millis();
    vO = analogRead(thermistorPin);
    //calculating R2 using potential divider circuit
    R2 = R1 * (1023.0 / (float)vO - 1.0);
    //using Steinhart-Hart equation to convert resistance in a temperature reading
    logR2 = log(R2);
    T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
    //Celsius temperature
    Tc = T - 273.15;
    digitalWrite(powerAndOut, HIGH);  // Turn the sensor ON
    level = analogRead(waterLevelPin);  // Read the analog value from sensor

    //sending data to the bridge
    Serial.write(0xff);   //255
    Serial.write(0x02);
    Serial.write((char)(Tc));
    //sensor from 0 to 140
    Serial.write((char)level);
    Serial.write(0xfe);  //254

    // Showing temperature and water level
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp:       C  ");
    lcd.setCursor(6, 0);
    // Display Temperature in C
    lcd.print((int)Tc);
    //Display liquid level
    lcd.setCursor(0,1);
    lcd.print("Leak:");
    lcd.setCursor(10,1);
    //lcd.print(level);
    if(level < 40)    lcd.print("    ");
    else if(level >= 40 && level < 70)   lcd.print("Low    ");
    else if(level >= 70 && level <= 120) lcd.print("Med    "); 
    else    lcd.print("High   ");
  }

  int iFutureState;
  int iFutureState2;
  int iReceived;

  if (Serial.available()>0)
  { 
    iReceived = Serial.read();

    
    //back to the firste state
    iFutureState2 = 0;
    
    if (iState2==0 && iReceived=='W') iFutureState2=1;
    if (iState2==1 && iReceived=='N') iFutureState2=2;
    if (iState2==2 && iReceived=='W') iFutureState2=1;
    
    if (iReceived==10 || iReceived==13 || iReceived== 'W' || iReceived== 'N') iFutureState2=iState2;

    // onEnter Actions
    if (iFutureState2==1 && iState2==0){
      digitalWrite(3, HIGH);  // switch on from 0 to 1
      //lcd.clear();
      //lcd.setCursor(0, 0);
      //lcd.print("WARNING");
    }
    //if (iFutureState2==2 && iState2==0) digitalWrite(3, LOW);   //switch off from 0 to 2
    if (iFutureState2==1 && iState2==2){
      digitalWrite(3, HIGH);    // switch on from 2 to 1
      //lcd.clear();
      //lcd.setCursor(0, 0);
      //lcd.print("WARNING");
    }
    if (iFutureState2==2 && iState2==1) digitalWrite(3, LOW);    // switch on from 1 to 2

    //state transition
    iState2 = iFutureState2;

    
    //back to the first state
    iFutureState=0;

    if (iState==0 && iReceived=='O') iFutureState=1;
    if (iState==1 && iReceived=='N') iFutureState=2;
    if (iState==1 && iReceived=='F') iFutureState=3;
    if (iState==3 && iReceived=='F') iFutureState=4;
    if (iState==4 && iReceived=='O') iFutureState=1;
    if (iState==2 && iReceived=='O') iFutureState=1;
    
    // CR and LF are the EOL (no transition)
    if (iReceived==10 || iReceived==13) iFutureState=iState;

     // onEnter Actions
    if (iFutureState==2 && iState==1) digitalWrite(2, HIGH);  // switch on from 1 to 2
    if (iFutureState==4 && iState==3) digitalWrite(2, LOW);  // switch off from 3 to 4 


     // state transition
    iState = iFutureState;
  }
}
