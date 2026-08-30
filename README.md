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
* [Code of the robo](#code)

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

## Code Python <a class="anchor" id="code"></a>

```ino
//we create all the variables
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
//The angle required to turn correctly is calculated.
def calcular_angulo_pd(x_actual, x_objetivo):
    global var_ulti_error,var_kp,var_kd,var_var_rojo,var_var_verde,var_id_obj,var_x_coord,var_height,var_ultrasonico_1,var_ultrasonico_2,var_angulo,var_error,var_derivada,var_giro,var_angulo_seguro
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
//An escape maneuver is created to prevent the robot from colliding with the walls; ultrasonic sensors are used to calculate the distance to the wall.
def maniobra_escape(dist_derecha, dist_izquierda):
    global var_ulti_error,var_kp,var_kd,var_var_rojo,var_var_verde,var_id_obj,var_x_coord,var_height,var_ultrasonico_1,var_ultrasonico_2,var_angulo,var_error,var_derivada,var_giro,var_angulo_seguro,var_angulo_escape
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
//Everything is brought together, and the variables are defined to ensure everything works.
def task1():
    global var_ulti_error,var_kp,var_kd,var_var_rojo,var_var_verde,var_id_obj,var_x_coord,var_height,var_ultrasonico_1,var_ultrasonico_2,var_angulo
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
        if (((var_height > 250) or (var_ultrasonico_2 < 20)) or (var_ultrasonico_1 < 20)):
            rcu.SetLCDClear(0xF800)
            maniobra_escape(var_ultrasonico_2, var_ultrasonico_1)
            var_ulti_error = 0
        else:
            if (var_id_obj == var_var_rojo):
                rcu.SetLCDClear(0x07E0)
                calcular_angulo_pd(var_x_coord, 90)
                if (var_ultrasonico_1 < 150):
                    servo.SetMagneticServoDegreeSpeed(1, 140, 80)
                else:
                    servo.SetMagneticServoDegreeSpeed(1, var_angulo, 80)
                motor.SetMotor(1, 80)
            else:
                if (var_id_obj == var_var_verde):
                    rcu.SetLCDClear(0x07E0)
                    calcular_angulo_pd(var_x_coord, 520)
                    if (var_ultrasonico_2 < 150):
                        servo.SetMagneticServoDegreeSpeed(1, 40, 80)
                    else:
                        servo.SetMagneticServoDegreeSpeed(1, var_angulo, 80)
                    motor.SetMotor(1, 80)
                else:
                    rcu.SetLCDClear(0x001F)
                    servo.SetMagneticServoDegreeSpeed(1, 90, 70)
                    motor.SetMotor(1, 100)
                    var_ulti_error = 0
        rcu.SetWaitForTime(0.05)

task1()
