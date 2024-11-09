//initialise Camera, Lidar, IMU, RoverMovement

const float max_safe_slope = 20.0; // degrees; TBD
const float min_stability_score = 0.7; //TBD
const float max_obstacle_height = 0.3; // meters; TBD
const float safe_sand_speed = 20 //safe speed for traversing sand; TBD
const float sand_threshold = 20 //typical amount of wheel slip to suggest sand; TBD
const float wheel_slip_threshold = 30 //unsafe level of wheel slip


//Analyzing current variables
float currentSlope;
float stabilityScore;
float currentSpeed;
float wheelSlip;
String currentTerrain = "unknown";

void setup() {
  Camera.begin();
  Lidar.begin();
  IMU.begin();
  RoverMovement.begin();

}

void loop() {
  //Obtain sensor data; based on Camera, lidar, imu, set currentSlope, stabilityScore, currentSpeed
  currentTerrain = analyzeTerrain();
  //measure currentSlope using IMU
  if (currentTerrain == "bedrock") {
    traverseBedrock();
  } else if (currentTerrain == "outcrop") {
    traverseOutcrop();
  } else if (currentTerrain == "loose_sand"){
    traverseLooseSand();
  }
}

void analyzeTerrain() {
  //use image data and lidar; outputs string with name of current terrain type
}

void traverseBedrock() {

}

void traverseOutcrop() {
  if((currentSlope > max_safe_slope) || (stabilityScore - min_stability_score > 0.1)){ //0.1 TBC; ie very poor stability
    findAlternatePath();
  } else if (stabilityScore > min_stability_score) {
    currentSpeed = 1;
    moveForward(currentSpeed); //TBC; decrease speed
  } else {
    moveForward(currentSpeed);
  }

}

void traverseLooseSand() {
  currentSpeed = 1 //TBC; reduce speed
  //adjust wheel traction settings
  //increase motor torque

  if(wheelSlip > wheel_slip_threshold){ //if rover might be getting stuck in sand
    moveBackward(currentSpeed); //change the speed
  } else {
    moveForward(currentSpeed);
  }
}

void findAlternatePath() {

}

void moveForward(speed) {
  //move forward by speed
}

void moveBackward(speed) {
  //move backward by speed
}
