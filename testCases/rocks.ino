//! Libraries for camera, LiDAR, and ultrasonic sensors
//! #include <SomeCameraLibrary.h>
//! #include <SomeLidarLibrary.h>
//! #include <SomeUltrasonicLibrary.h>
#include <Wire.h>

// Define constants and variables
const int ANGLE_SEGMENTS = 8;       // Number of angle segments
const int DISTANCE_THRESHOLD = 200; // distance in cm
const int ROVER_WIDTH = 50;         // Rover width in cm

int lidarData[ANGLE_SEGMENTS]; // Array for LiDAR data
int selectedAngle = -1;
bool pathClear = true; // Flag

// TODO Function prototypes
void getImageData();
void getLidarData();
void getUltrasonicData();
int selectAngle();
bool isPathClear(int angle);

void setup() {
    Serial.begin(9600);
    initCamera();
    initLidar();
    initUltrasonic();
}

void loop() {
    // data from camera and LiDAR
    getImageData();
    getLidarData();

    // Detect large objects and find a clear path
    selectedAngle = selectAngle();

    // Clear path and navigate
    while (pathClear) {
        if (isPathClear(selectedAngle)) {
            // Move 
            moveRover(selectedAngle);
        } else {
            // If no clear path
            selectedAngle = selectAngle();
            if (selectedAngle == -1) {
                // stop rover if no clear path
                stopRover();
                break;
            }
        }
    }
}

// TODO Function to obtain image data from camera
void getImageData() {
    // TODO Placeholder for camera data processing
    Serial.println("Obtaining image data...");
    // TODO Process image data here
}

// TODO Function to obtain terrain data from LiDAR
void getLidarData() {
    for (int i = 0; i < ANGLE_SEGMENTS; i++) {
        lidarData[i] = getLidarDistance(i);
    }
}

//? detect large objects and select an angle segment with clear path
int selectAngle() {
    int maxDistance = 0;
    int bestAngle = -1;

    // Find the furthest large object beyond the distance threshold
    for (int i = 0; i < ANGLE_SEGMENTS; i++) {
        if (lidarData[i] > DISTANCE_THRESHOLD && lidarData[i] > maxDistance) {
            maxDistance = lidarData[i];
            bestAngle = i;
        }
    }

    return bestAngle;
}

// TODO Function to check if the selected path is clear using ultrasonic data
bool isPathClear(int angle) {
    Serial.println("Checking path clearance...");
    int ultrasonicData = getUltrasonicDistance(angle);

    // if path width is enough for rover to pass
    if (ultrasonicData >= ROVER_WIDTH) {
        return true;
    } else {
        return false;
    }
}

// TODO Function to move rover in the selected angle
void moveRover(int angle) {
    Serial.print("Moving rover in direction: ");
    Serial.println(angle);
    // Move commands for motor control to go in the desired angle
}

// TODO Function to stop the rover
void stopRover() {
    Serial.println("Stopping rover, no clear path.");
    // Stop all motors
}
