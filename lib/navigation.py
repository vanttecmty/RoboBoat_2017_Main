import lib.variables as var
import lib.motors as motors

#Navigation class



def move_left():
	motors.move_servos(var.servoMoveLeft - 90);

def move_right():
	motors.move_servos(var.servoMoveRight - 90);

def move_init_pos():
	motors.move_servos(var.servoMoveInitP - 90);

def move_forward():
	motors.move_servos(var.servoMoveInitP - 90) ;
	motors.move_thrusters(var.thrusterMoveBack - 1500) ;
	
def move_backward():
	motors.move_thrusters(var.thrusterMoveBack - 1500 ) ;

