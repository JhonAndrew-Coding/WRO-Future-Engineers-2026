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
