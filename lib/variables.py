import sys
import os

lidarPort   = ''
imuPort     = ''
arduinoPort = ''


leftServo = 'l'
rightServo = 'r'
bothServos = 'b'

leftThruster = 'l'
rightThruster = 'r'
backThrusters = 'b'
frontThrusters = 'f'
allThrusters = 'a'

##Motors Information
numberOfMotors    = 2
numberOfBatteries = 2

maxSpeed = 9.8

boatWeight = 25 #Kg

thrusterMinRotationalSpeed = 300  #rev/min
thrusterMaxRotationalSpeed = 3800 #rev/min

thrusterOperatingVoltage = 14.8 #V

thrusterLength 		= 113 #mm
thrusterDiameter 	= 100 #mm
propellerDiameter 	= 76 #mm
thrusterWeightWater = 156 #g
thrusterWeightAir 	= 344 #g


#Single Thruster calculations
#st = Single Thruster
stFowardMaxThrust16V  = 5.1  #kgf
stReverseMaxThrust16V = 4.1  #kgf

stRowardMaxThrust12V  = 3.55 #kgf
stReverseMaxThrust12V = 3.0  #kgf

thrusterBatteryVoltage = 14.8

#Voltage of the battery = 14.8
stForwardMaxThrust14V = (thrusterBatteryVoltage * stFowardMaxThrust16V)  / 16  #kgf
stReverseMaxThrust14V = (thrusterBatteryVoltage * stReverseMaxThrust16V) / 16 #kgf

stTopForwardAcc  = (stForwardMaxThrust14V * 9.8 ) / boatWeight #m/s²
stTopBackwardAcc = (stReverseMaxThrust14V * 9.8) / boatWeight #m/s²

#Full Boat Calculations
##4 Batteries 1 each Motor
fourBatForwardMaxThrust = stForwardMaxThrust14V * 4 #kgf
fourBatBackwardMaxThrust= stReverseMaxThrust14V * 4 #kgf
fourBatTopForwardAcc	= (fourBatForwardMaxThrust * 9.8 ) / boatWeight 		#m/s²
fourBatTopBackwardAcc	= (fourBatBackwardMaxThrust * 9.8 ) / boatWeight     #m/s²

##2 Batteries
twoBatForwardMaxThrust  = (thrusterBatteryVoltage/2 * stFowardMaxThrust16V)  / 16 #kgf
twoBatBackwardMaxThrust = (thrusterBatteryVoltage/2 * stReverseMaxThrust16V) / 16 #kgf
twoBatTopForwardAcc		= (twoBatForwardMaxThrust  * 9.8 ) / boatWeight 		#m/s²
twoBatTopBackwardAcc 	= (twoBatBackwardMaxThrust * 9.8 ) / boatWeight 		#m/s²

##3 Batteries 1 For each rear thruster 1 for the two front thrusters
threeBatForwardMaxThrust = (stForwardMaxThrust14V  * 2) + twoBatForwardMaxThrust  	#kgf
threeBatBackwardMaxThrust= (stForwardMaxThrust14V * 2) + twoBatBackwardMaxThrust 	#kgf
threeBatTopForwardAcc	 = (threeBatForwardMaxThrust  * 9.8 ) / boatWeight 		#m/s²
threeBatTopBackwardAcc	 = (threeBatBackwardMaxThrust * 9.8 ) / boatWeight 		#m/s²
