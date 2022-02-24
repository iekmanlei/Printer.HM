import controlP5.*;
import processing.serial.*;

Serial port;

ControlP5 cp5; //create ControlP5 object

String val, status;
boolean firstContact = false;
boolean TempControl = false;

float value;
float X, Y;
float settemp;
float TimeMea, TempMea;

void setup(){
  size(800,600); //Size of the window (width, height)
  background(220,220,220); // Background color of window (R,G,B)
  textSize(32);
  fill(6,47,102);
  text("Stage Heater Temperature Control", 130,50);
  textSize(20);
  text("Real-time temperature measurement", 100,280);
  //Set up measurement graph
  strokeWeight(1);
  stroke(6,47,102);
  textSize(15);
  //y axis
  line(100,305,100,550);
 
  line(100,310,105,310);
  text("50C",62,315);
  line(100,350,105,350);
  text("45C",62,355);
  line(100,390,105,390);
  text("40C",62,395);
  line(100,430,105,430);
  text("35C",62,435);
  line(100,470,105,470);
  text("30C",62,475);
  line(100,510,105,510);
  text("25C",62,515);
  text("20C",62,555);
  
  //x axis
  line(100,550, 750, 550);
  line(140,550,140,555);
  line(180,550,180,555);
  line(220,550,220,555);
  line(260,550,260,555);
  line(300,550,300,555);
  line(340,550,340,555);
  line(380,550,380,555);
  line(420,550,420,555);
  line(460,550,460,555);
  line(500,550,500,555);
  line(540,550,540,555);
  line(580,550,580,555);
  line(620,550,620,555);
  line(660,550,660,555);
  line(700,550,700,555);
  text("min",730,575);
  point (100,550);//Origin
  
  //label
  textSize(10);
  text("Range: 20-50C, in format: XX.XC",120,165);
  textSize(20);
  //fill(15,72,132);
  text("Status", 420,140);
  text("Temp", 420, 220);
 
  
  //printArray(Serial.list()); //prints all available serial ports
  port = new Serial(this, "/dev/ttyUSB0", 9600); 
  port.bufferUntil('\n'); //Store the incoming data into a buffer until we see (\n)
  
  
  cp5 = new ControlP5(this); //instantiate controlP5
  
  //Add buttons    
  cp5.addButton("START")
   .setPosition(180,80)
   .setSize (90,70)
   .setColorBackground(color(44,149,178))
   .setFont(createFont("arial",20))
  ;
  
  cp5.addTextfield("T")
     .setPosition(100,80)
     .setSize(80,70)
     .setColorBackground(color(177,234,249))
     //.setColorActive(color(177,234,249))
     .setAutoClear(false)
     .setFont(createFont("arial",20))
     .setColorValue(color(24,89,107))
     ;
     
  cp5.addButton("STOP")
     .setPosition (100,180)
     .setSize(170,70)
     .setColorBackground(color(229,98,68))
     .setFont(createFont("arial",25))
     ;

     
}

void draw(){
  
 fill(220,220,220);
 noStroke();
 rect(500,110,150,200);
  if (TimeMea <= 15){
    textSize(15);
    fill(6,47,102);
    text("1",137,575);
    text("2",177,575);
    text("3",217,575);
    text("4",257,575);
    text("5",297,575);
    text("6",337,575);
    text("7",377,575);
    text("8",417,575);
    text("9",457,575);
    text("10",490,575);
    text("11",530,575);
    text("12",570,575);
    text("13",610,575);
    text("14",650,575);
    text("15",690,575);
  }
  if (TimeMea > 15 && TimeMea <= 30){
    textSize(15);
    fill(6,47,102);
    text("16",137,575);
    text("17",177,575);
    text("18",217,575);
    text("19",257,575);
    text("20",297,575);
    text("21",337,575);
    text("22",377,575);
    text("23",417,575);
    text("24",457,575);
    text("25",490,575);
    text("26",530,575);
    text("27",570,575);
    text("28",610,575);
    text("29",650,575);
    text("30",690,575);
  }
  if (TimeMea > 30 && TimeMea <= 45){
    textSize(15);
    fill(6,47,102);
    text("31",137,575);
    text("32",177,575);
    text("33",217,575);
    text("34",257,575);
    text("35",297,575);
    text("36",337,575);
    text("37",377,575);
    text("38",417,575);
    text("39",457,575);
    text("40",490,575);
    text("41",530,575);
    text("42",570,575);
    text("43",610,575);
    text("44",650,575);
    text("45",690,575);
  }
 
  strokeWeight(3);
  stroke(89,20,16);
  if (TempControl == true){
    if (str(TempMea) != "NaN" && status != null){
      point(X,Y);
      textSize(50);
      text(str(TempMea), 500,230);
      text(status, 500,150);
  }
  }
  if (TempControl == false){
      textSize(50);
      text("N/A", 500,230);
      text("OFF", 500,150);
  }
  delay(50);

}


void serialEvent(Serial port){ //this function is called when a carriage return
  val = port.readStringUntil('\n');
  if (val != null){
    //trim whitespace and formatting characters
    val = trim(val);
    //println(val);
    if (firstContact == false){
      if (val.equals("A")){
        port.clear(); //Empty the buffer
        firstContact = true;
        port.write("A");
        println("contact");
      }
    }
    else { //already established contact, keep receiving data
      println(val);
      TempMea = float(getValue(val,',',0)); //Extract temp measurment
      TimeMea = float(getValue(val,',',3))/60000; //Extract time measurment
      X = map(TimeMea, 0, 15, 100, 700);
      Y = map(TempMea, 20, 50, 550, 310); 
      status = getValue(val,',',1); // Extract status
    }
  }
}

void START(){
  
  background(220,220,220);
  textSize(32);
  fill(6,47,102);
  text("Stage Heater Temperature Control", 130,50);
  textSize(20);
  text("Real-time temperature measurement", 100,280);
  
  //Set up measurement graph
  strokeWeight(1);
  stroke(6,47,102);
  textSize(15);
  
  //y axis
  line(100,305,100,550);
  line(100,310,105,310);
  text("50C",62,315);
  line(100,350,105,350);
  text("45C",62,355);
  line(100,390,105,390);
  text("40C",62,395);
  line(100,430,105,430);
  text("35C",62,435);
  line(100,470,105,470);
  text("30C",62,475);
  line(100,510,105,510);
  text("25C",62,515);
  text("20C",62,555);
  //x axis
  line(100,550, 750, 550);
  line(140,550,140,555);
  line(180,550,180,555);
  line(220,550,220,555);
  line(260,550,260,555);
  line(300,550,300,555);
  line(340,550,340,555);
  line(380,550,380,555);
  line(420,550,420,555);
  line(460,550,460,555);
  line(500,550,500,555);
  line(540,550,540,555);
  line(580,550,580,555);
  line(620,550,620,555);
  line(660,550,660,555);
  line(700,550,700,555);
  text("min",730,575);
  point (100,550);//Origin
  
  //label 
  textSize(10);
  text("Range: 20-50C, in format: XX.XC",120,165);
  textSize(20);
  fill(15,72,132);
  text("Status", 420,140);
  text("Temp", 420, 220);
  port.write("S"); //start
  
  //port.clear();
  String inputtemp=cp5.get(Textfield.class,"T").getText();
  port.write(inputtemp + "H"); 
  println(inputtemp+"H");
  port.clear();
  TempControl = true;
}


void STOP(){
  port.write("P"); //Pause
  TempControl = false;
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
