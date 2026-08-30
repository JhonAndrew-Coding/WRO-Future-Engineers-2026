## WRO Future Engineers 2026 - Team Nova
This repository contains the software and documentation developed for an autonomous vehicle designed to compete in the WRO Future Engineers 2026 competition.

The project focuses on autonomous navigation, obstacle detection, trajectory planning, and real-time decision-making. The vehicle is designed to interpret sensor data from its environment and use this information to determine and execute appropriate movements throughout the competition field.

## Project Overview

The autonomous system integrates sensor processing, vehicle control, and navigation algorithms to achieve reliable and precise movement. The software continuously processes information from the vehicle's sensors and adjusts its trajectory according to the detected conditions.

The main objectives of the system are:

 - Autonomous navigation of the competition field.
 - Detection and avoidance of obstacles.
 - Real-time trajectory planning and adjustment.
 - Precise steering and motor control.
 - Reliable decision-making based on sensor data.
 - Autonomous execution of the required maneuvers.
 - Technical Approach

The project combines embedded programming, robotics, sensor integration, control systems, and computational geometry.

The navigation system uses sensor measurements to estimate the vehicle's position and identify relevant elements of the environment. Based on this information, the control algorithms determine the appropriate steering and movement commands required to follow the planned trajectory.

Special attention is given to reliability, repeatability, and adaptability, ensuring that the vehicle can operate under different configurations of the competition field.

## Repository Structure

The repository contains the source code and supporting resources required for the development and operation of the autonomous vehicle.

The code is organized to facilitate the development, testing, and modification of the different components of the autonomous system.

## Competition

World Robot Olympiad – Future Engineers 2026

This project is developed as part of our participation in the WRO Future Engineers category, with the objective of designing and implementing a reliable autonomous robotic system capable of completing the competition challenges.

## Table of Contents
* [The Team](#team)
* [Robot Photos](#robot-image)
* [Python Code](#py-code)
* [Robocode Block Code](#block-code)

## The Team <a class="anchor" id="team"></a>

### Juan Andrés Guerra
<p align="center">
  <img src="./t-photos/juan A photo .jpeg" alt="Juan Andrés Guerra" width="80%">
</p>

<b>High School:</b> Windsor School, Valledupar, Colombia

---

### Angel Valeria Ruiz

<p align="center">
  <img src="./t-photos/angel photo.jpeg" alt="Angel Valeria Ruiz" width="80%">
</p>

<b>High School:</b> Ciberkids, Valledupar, Colombia

---

### Team Photo
<p align="center">
  <img src="./t-photos/Team photo.jpeg" alt="Team Photo" width="80%">
</p>

## Vehicle's photos <a class="anchor" id="robot-image"></a>

| <img src="./v-photos/front.jpeg" width="90%" /> | <img src="./v-photos/back.jpeg" width="85%" /> | 
| :--: | :--: | 
| *Front* | *Back* |
| <img src="./v-photos/left.jpeg" width="90%" /> | <img src="./v-photos/right.jpeg" width="85%" /> | 
| *Left* | *Right* |
| <img src="./v-photos/top.jpeg" width="90%" /> | <img src="./v-photos/bottom.jpeg" width="85%" /> | 
| *Top* | *Bottom* |

## Code Python <a class="anchor" id="py-code"></a>
This program controls an autonomous robot using an AI camera, ultrasonic sensors, a servo motor, and drive motors. The robot is designed to detect colored objects, adjust its direction according to their position, and avoid obstacles while moving through its environment.

### Libraries and Variables

The program starts by importing the libraries needed to communicate with and control the different hardware components of the robot. It also defines several global variables that will store information such as detected objects, sensor measurements, steering angles, and the values required for the PD controller.
```ino
import rcu, aicam, servo, sensor, motor

var_ulti_error = 0
var_kp = 0
var_kd = 0
var_var_rojo = 0
var_var_verde = 0
var_id_obj = 0
var_x_coord = 0
var_height = 0
var_ultrasonico_1 = 0
var_ultrasonico_2 = 0
var_angulo = 0
var_error = 0
var_derivada = 0
var_giro = 0
var_angulo_seguro = 0
var_angulo_escape = 0
```
### PD Steering Control
The "calcular_angulo_pd()" function is responsible for determining how the robot should steer based on the position of the object detected by the AI camera. It calculates the difference between the object's current position and the desired position, then uses proportional and derivative values to create a smooth steering correction. The resulting angle is also limited to keep the servo within a safe range.
```ino
def calcular_angulo_pd(x_actual, x_objetivo):
    var_error = x_objetivo - x_actual
    var_derivada = var_error - var_ulti_error
    var_giro = (var_error * var_kp) + (var_derivada * var_kd)
    var_ulti_error = var_error
    var_angulo = 90 + var_giro

    if (var_angulo > 140):
        var_angulo_seguro = 140
    else:
        if (var_angulo < 40):
            var_angulo_seguro = 40
        else:
            var_angulo_seguro = var_angulo
```
### Escape Maneuver
The "maniobra_escape()" function is designed to prevent the robot from colliding with nearby walls or obstacles. When an obstacle is detected, the robot stops and uses the distances measured by the ultrasonic sensors to determine the safest direction to turn. It then moves backward to create space before returning the servo to its central position.
```ino
def maniobra_escape(dist_derecha, dist_izquierda):
    motor.SetMotor(1, 0)
    rcu.SetWaitForTime(0.2)

    if (dist_izquierda < 100):
        var_angulo_escape = 140
    else:
        if (dist_derecha < 100):
            var_angulo_escape = 40
        else:
            var_angulo_escape = 90

    servo.SetMagneticServoDegreeSpeed(1, var_angulo_escape, 90)
    motor.SetMotor(1, -70)
    rcu.SetWaitForTime(1)

    servo.SetMagneticServoDegreeSpeed(1, 90, 90)
    motor.SetMotor(1, 0)
    rcu.SetWaitForTime(0.2)
```
### Main Control System
The "task1()" function brings together all the main components of the robot and establishes their initial configuration. It sets the values for the PD controller, assigns identification numbers to the red and green objects, configures the AI camera for color detection, and places the servo in its starting position. After this setup, the robot continuously reads information from its camera and ultrasonic sensors.
```ino
def task1():
    var_ulti_error = 0
    var_kp = 0.08
    var_kd = 0.005

    var_var_rojo = 1
    var_var_verde = 2

    aicam.SetWaitAICamCmd(5, "color")
    servo.SetMagneticServoDegreeSpeed(1, 90, 70)

    while True:
        var_id_obj = aicam.GetAICam(5, 1, 1)
        var_x_coord = aicam.GetAICamIDData(5, 1, 1)
        var_height = aicam.GetAICamIDData(5, 1, 4)

        var_ultrasonico_1 = sensor.GetUltrasound(2)
        var_ultrasonico_2 = sensor.GetUltrasound(3)
```
### Object Detection and Navigation
This section contains the main decision-making logic of the robot. It first checks whether an obstacle is dangerously close and, if so, activates the escape maneuver. If the path is clear, the robot checks which color has been detected and uses the PD controller to adjust its steering. When no recognized color is detected, the robot continues moving forward with the servo centered while searching for a target.
```ino
if (((var_height > 250) or (var_ultrasonico_2 < 20)) or 
    (var_ultrasonico_1 < 20)):

    maniobra_escape(var_ultrasonico_2, var_ultrasonico_1)
    var_ulti_error = 0

else:
    if (var_id_obj == var_var_rojo):
        calcular_angulo_pd(var_x_coord, 90)
        servo.SetMagneticServoDegreeSpeed(1, var_angulo, 80)
        motor.SetMotor(1, 80)

    else:
        if (var_id_obj == var_var_verde):
            calcular_angulo_pd(var_x_coord, 520)
            servo.SetMagneticServoDegreeSpeed(1, var_angulo, 80)
            motor.SetMotor(1, 80)

        else:
            servo.SetMagneticServoDegreeSpeed(1, 90, 70)
            motor.SetMotor(1, 100)
            var_ulti_error = 0

    rcu.SetWaitForTime(0.05)
```
### Starting the Program 
The final line calls the "task1()" function, which starts the entire control system. Once this function is executed, the robot begins its autonomous operation and continuously repeats the process of detecting objects, checking for obstacles, calculating steering corrections, and controlling its movement.
```ino
task1()
```
## Block Code <a class="anchor" id="block-code"></a>
This part uses RoboCode blocks to program an autonomous robot capable of detecting colored objects, adjusting its direction, and avoiding obstacles using ultrasonic sensors.
### PD Steering Control
The "calcular_angulo_pd" function controls the robot's steering according to the position of the detected object. It calculates the error between the current and target positions, then uses proportional and derivative control to determine the necessary steering correction. The final angle is limited between 40° and 140° to prevent excessive turns.
*Block code:*
<p align="center">
  <img src="./src/PD_Control.png" alt="PD Control" width="80%">
</p>
### Escape Maneuver
The maniobra_escape function is responsible for preventing collisions with walls or obstacles. The robot first stops and checks the distance detected by the ultrasonic sensors. Depending on which side is closer to an obstacle, it chooses a direction to turn, moves backward, and finally returns the servo to the center.
*Block code:*
<p align="center">
  <img src="./src/Escape_Maneuver.png" alt="Esc Maneuver" width="80%">
</p>

