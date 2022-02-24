// Define pin numbers
// Printhead 1
const int En1 = 23;
const int MS11 = 25;
const int MS21 = 27;
const int MS31 = 29;
const int RST1 = 31;
const int SLP1 = 33; 
const int StepPin1 = 35;
const int DirPin1 = 37;

// Printhead 2
const int En2 = 6;
const int MS12 = 7;
const int MS22 = 8;
const int MS32 = 9;
const int RST2 = 10;
const int SLP2 = 11; 
const int StepPin2 = 12;
const int DirPin2 = 13;

// Printhead 3
const int En3 = 28;
const int MS13 = 26;
const int MS23 = 24;
const int MS33 = 22;
const int RST3 = 2;
const int SLP3 = 3; 
const int StepPin3 = 4;
const int DirPin3 = 5;

// Printhead 4
const int En4 = 44;
const int MS14 = 42;
const int MS24 = 40;
const int MS34 = 38;
const int RST4 = 36;
const int SLP4 = 34; 
const int StepPin4 = 32;
const int DirPin4 = 30;

int delaytime;
int data; // Receive python signal
int input_number; 


void setup() {
  Serial.begin(2400); 
  // Printhead 1; Set as 1/16 step resolution
  pinMode(En1, OUTPUT);
  pinMode(MS11, OUTPUT);
  pinMode(MS21, OUTPUT);
  pinMode(MS31, OUTPUT);
  pinMode(RST1, OUTPUT);
  pinMode(SLP1, OUTPUT);
  pinMode(StepPin1, OUTPUT);
  pinMode(DirPin1, OUTPUT);
  digitalWrite(RST1,HIGH);
  
  // Printhead 2; Set as 1/16 step resolution 
  pinMode(En2, OUTPUT);
  pinMode(MS12, OUTPUT);
  pinMode(MS22, OUTPUT);
  pinMode(MS32, OUTPUT);
  pinMode(RST2, OUTPUT);
  pinMode(SLP2, OUTPUT);
  pinMode(StepPin2, OUTPUT);
  pinMode(DirPin2, OUTPUT);
  digitalWrite(RST2,HIGH);

  // Printhead 3; Set as 1/16 step resolution
  pinMode(En3, OUTPUT);
  pinMode(MS13, OUTPUT);
  pinMode(MS23, OUTPUT);
  pinMode(MS33, OUTPUT);
  pinMode(RST3, OUTPUT);
  pinMode(SLP3, OUTPUT);
  pinMode(StepPin3, OUTPUT);
  pinMode(DirPin3, OUTPUT);
  digitalWrite(RST3,HIGH);
  
  // Printhead 4; Set as 1/16 step resolution
  pinMode(En4, OUTPUT);
  pinMode(MS14, OUTPUT);
  pinMode(MS24, OUTPUT);
  pinMode(MS34, OUTPUT);
  pinMode(RST4, OUTPUT);
  pinMode(SLP4, OUTPUT);
  pinMode(StepPin4, OUTPUT);
  pinMode(DirPin4, OUTPUT);
  digitalWrite(RST4,HIGH);
  
  while (Serial.available()<=0){}
    int input_number=Serial.read()-48;
    Serial.print(input_number);
    while(Serial.available()<input_number){}
    delaytime =Serial.parseInt();
    Serial.println('i');
    Serial.print(delaytime);
}


void loop() {
    while (Serial.available()){
    data=Serial.read();
    }
if (data =='1'){
  // Switch on printhead 1
  digitalWrite(En1, LOW); 
  digitalWrite(En2, HIGH);
  digitalWrite(En3, HIGH);
  digitalWrite(En4, HIGH);
  digitalWrite(SLP1, HIGH);
  digitalWrite(SLP2, LOW);
  digitalWrite(SLP3, LOW);
  digitalWrite(SLP4, LOW);
  //1/2 step
  digitalWrite(MS11, LOW);
  digitalWrite(MS21, LOW);
  digitalWrite(MS31, LOW);
  digitalWrite(DirPin1, HIGH); 
  digitalWrite(StepPin1, HIGH);
  delayMicroseconds(delaytime); 
  digitalWrite(StepPin1, LOW);
  delayMicroseconds(delaytime); 
}
 
if (data =='2'){
  // Switch on printhead 2
  digitalWrite(En1, HIGH); 
  digitalWrite(En2, LOW);
  digitalWrite(En3, HIGH);
  digitalWrite(En4, HIGH);
  digitalWrite(SLP1, LOW);
  digitalWrite(SLP2, HIGH);
  digitalWrite(SLP3, LOW);
  digitalWrite(SLP4, LOW);
  
  digitalWrite(MS12, HIGH);
  digitalWrite(MS22, HIGH);
  digitalWrite(MS32, HIGH);
  digitalWrite(DirPin2, HIGH); 
  digitalWrite(StepPin2, HIGH);
  delayMicroseconds(delaytime); 
  digitalWrite(StepPin2, LOW);
  delayMicroseconds(delaytime); 
}

if (data =='3'){
  // Switch on printhead 3
  digitalWrite(En1, HIGH); 
  digitalWrite(En2, HIGH);
  digitalWrite(En3, LOW);
  digitalWrite(En4, HIGH);
  digitalWrite(SLP1, LOW);
  digitalWrite(SLP2, LOW);
  digitalWrite(SLP3, HIGH);
  digitalWrite(SLP4, LOW);
  
  digitalWrite(MS13, HIGH);
  digitalWrite(MS23, HIGH);
  digitalWrite(MS33, HIGH);
  digitalWrite(DirPin3, HIGH); 
  digitalWrite(StepPin3, HIGH);
  delayMicroseconds(delaytime); 
  digitalWrite(StepPin3, LOW);
  delayMicroseconds(delaytime); 
}

if (data == '4'){
  // Switch on printhead 4
  digitalWrite(En1, HIGH); 
  digitalWrite(En2, HIGH);
  digitalWrite(En3, HIGH);
  digitalWrite(En4, LOW);
  digitalWrite(SLP1, LOW);
  digitalWrite(SLP2, LOW);
  digitalWrite(SLP3, LOW);
  digitalWrite(SLP4,HIGH);
  
  digitalWrite(MS14, HIGH);
  digitalWrite(MS24, HIGH);
  digitalWrite(MS34, HIGH);
  digitalWrite(DirPin4, HIGH); 
  digitalWrite(StepPin4, HIGH);
  delayMicroseconds(delaytime); 
  digitalWrite(StepPin4, LOW);
  delayMicroseconds(delaytime); 
}



else if (data =='5'){  
  // Turn off all printheads
  digitalWrite(En1, HIGH);
  digitalWrite(En2, HIGH);
  digitalWrite(En3, HIGH);
  digitalWrite(En4, HIGH);
  digitalWrite(SLP1, LOW);
  digitalWrite(SLP2, LOW);
  digitalWrite(SLP3, LOW);
  digitalWrite(SLP4, LOW);
  //digitalWrite(StepPin1, LOW);
  //digitalWrite(StepPin2, LOW);
  //digitalWrite(StepPin3, LOW);
}
}
