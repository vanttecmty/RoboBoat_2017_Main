import lib.variables as var
import lib.motors as motors

#Navigation class



def move_left():
	motors.move_servos(var.servoBoth, var.servoMoveLeft, var.servoMoveLeft)

def move_right():
	motors.move_servos(var.servoBoth, var.servoMoveRight, var.servoMoveRight)

def move_init_pos():
	motors.move_servos(var.servoBoth,var.servoMoveInitP,var.servoMoveInitP);

def move_forward():
	motors.move_servos(var.servoBoth, var.servoMoveInitP, var.servoMoveInitP)
	motors.move_thrusters(var.thrustersAll, var.thrusterMoveFront, var.thrusterMoveFront)

def move_backward():
	motors.move_thrusters(var.thrustersAll, var.thrusterMoveBack, var.thrusterMoveBack)

def move_horizonatl_left():
	motors.move_servos(var.servoBoth, var.servoMoveLeft, var.servoMoveLeft)
	motors.move_thrusters(var.thrustersAll, var.thrusterMoveFront, var.thrusterMoveFront)

def move_horizonatl_right():
	motors.move_servos(var.servoBoth, var.servoMoveRight, var.servoMoveRight)
	motors.move_thrusters(var.thrustersAll, var.thrusterMoveFront, var.thrusterMoveFront)

