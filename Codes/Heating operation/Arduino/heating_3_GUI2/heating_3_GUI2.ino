#include <LiquidCrystal.h>


//Control Software for the Electrical Resistance Idea

#include <MemoryFree.h>

//Define pin 12 as output called LED_PIN
#define LED_PIN 12

//Setting for amount of current to the heat pad (0-255)
int heatingValue;

//Include code for the thermocouple

#include <SPI.h>
#include <Adafruit_MAX31855.h>

//Define Software SPI pins for input
#define MAXDO   4
#define MAXCS   3
#define MAXCLK  2

#define Heat1 5

//Initialize thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

//Setting for goal nozzle temperature

float goalTemp, KFactor;
const float acceptableDeviation = 0.5;
char state[8], output[24]; //Open a string 'state' with 8 characters and a string 'output' with 24 characters
float endTime;
int delayTime = 1500;
int loopNum;
String str;
String T;
unsigned long tStart, treal;


//Control variables for heating
bool firstHeat = true; //Initiate first heat
bool decisionDelay = false; 
bool timeDelay = false;
bool TempControl = false;
void setup()
{
  //Set up input/output
  Serial.begin(9600); //Set the baud rate to 9600. Rate for signal transmission - Too large will mess up the signalling
  Serial.println("\nStarting the sketch...\n");
  pinMode(Heat1,OUTPUT);//Initiates Motor Channel A pin 
  establishContact(); //Enable contact with processing, send a byte to establish contact until processing responds  
}


void loop()
{if(Serial.available()>0){
  char val = Serial.read();

  if (val == ('S')){
    delay(300);
    str = Serial.readStringUntil('H'); //Read until the terminator 'H')
    char T2 = str.charAt(1); //Extract the second value of str
    char T1 = str.charAt(0); //Extract the first value of str
    char T4 = str.charAt(3); //Extract the fourth value of str
    int Temp = (100*(T1-'0')) + 10*(T2 -'0')+ (T4-'0'); //Convert str to int
    Serial.println(String(Temp));
    goalTemp = ((float) Temp)/10;// Convert temp to float
    Serial.println("Your setting temp is " + String(goalTemp));
    Serial.println(goalTemp);
    if (goalTemp > 24 && goalTemp < 65){
      TempControl = true;   
      tStart = millis();
      heatingValue = 250;
  }
  }
  if (val == ('P')){
    TempControl = false;
  }
}

  if (TempControl == true){
    float temperature = thermocouple.readCelsius(); //results from thermocouple  
      if(isnan(temperature)) {
      // if the reading temperature is not a number (isnan)
        Serial.println("N/A, N/A, N/A");
      }
      else {
        float error = goalTemp - temperature;
        if(!decisionDelay) { //if decisionDelay == false
          if(firstHeat) { //if firstHeat == true
            strcpy(state, "On");
            analogWrite(Heat1, heatingValue);
            if(error < 0){
              firstHeat = false;
              heatingValue = heatingValue/2;
          }
        }
        
        else if(abs(error) > acceptableDeviation) { //if not firstheat
          KFactor = heatingValue/6;
          heatingValue = heatingValue + error*KFactor; //Kfactor - To prevent temperature goes too high from goal temp
          if(heatingValue > 250) {
            heatingValue = 250;
          }
          else if(heatingValue < 0) {
            heatingValue = 0;
          }
          decisionDelay = true;
          timeDelay = true;
          endTime = millis() + delayTime; //?
          if(error>0) {
            Serial.println(goalTemp);
            Serial.println("Hello");
            strcpy(state, "On");
            analogWrite(Heat1, heatingValue);
          }
          else if(error<0) {
            strcpy(state, "Off");
            analogWrite(Heat1, 0);
          }  
        }
        else
        {
          strcpy(state,"On");
          Serial.println("Ohno");
          analogWrite(Heat1, heatingValue);
        }
      }
      else
      {
        if(millis() > endTime)
        {
          timeDelay = false;
        }
        if(error >= acceptableDeviation/2 && timeDelay == false)
        {
          decisionDelay = false;
        }
      }
    
      //Output Temperature and Heat Pad Status
      //strcpy(output, tempToAscii(temperature));//output = output + "," + state + ",";
      //sprintf(output, "%s,%s,%d", tempToAscii(temperature), state, heatingValue);  
      uint32_t treal = millis() - tStart;
      sprintf(output, "%s,%s,%d,%lu",tempToAscii(temperature), state, heatingValue, treal);
      Serial.println(output);
    }
    
  }

if (TempControl == false){  
  
    heatingValue = 0; 
    analogWrite(Heat1, 0);
    strcpy(state, "Off");    
}
    
}


//Convert interger to string
char* tempToAscii(double temp)
{
  char ascii[32];
  int frac;
  frac=(unsigned int)(temp*1000)%1000;  //get three numbers to the right of the deciaml point

  itoa((int)temp,ascii,10); //Store temp value to ascii array and convert the value to decimal base
  strcat(ascii,"."); //Add . to the end of array
  itoa(frac,&ascii[strlen(ascii)],10); //put the frac after the deciaml

  return ascii;
}

void establishContact(){
  while(Serial.available() <= 0){
    Serial.println("A"); //Send an A
    delay(300);
  }
}

