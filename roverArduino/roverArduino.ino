#include <SabertoothSimplified.h>

SabertoothSimplified Steve; 
int MAX_POWER = 25; //This equates to ~ 5v, present max for testing

int throttle(int power){

  if(power > MAX_POWER)
  {
    return 25;
  }
  
  else if(power < -MAX_POWER)
  {
    return -25; 
  }

  return power; 
}


void setup() {
    Serial3.begin(9600);

    SabertoothTXPinSerial.begin(9600); 
  
    Steve.drive(0);
    Steve.turn(0);

}

void loop() {
  if (Serial3.available()){
    String command = Serial3.readString();

    //f for forward
    if (command == "f"){
      Steve.drive(throttle(5));
      Steve.turn(0);
    //r for turn right
    } else if (command == "r"){
      Steve.turn(16);
    //l for turn left
    } else if (command == "l"){
      Steve.turn(-16);
    }
  }

}
