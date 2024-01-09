import time
import matplotlib.pyplot as plt


GRAVITY = 6.67430 * 10 ** -11
EARTH_MASS = 5.97219 * 10 ** 24
EARTH_RADIUS = 6.371 * 10 ** 6
earthPos = (0,0)
t = 0
time_step = 1


class Spacecraft:
    def __init__(self, mass, position, velocity, thrust):
        self.thrust = thrust
        self.mass = mass + (thrust.getFuelMass() * thrust.getNumOfThrusters())#in Kg
        self.position = position #a coordinate
        self.velocity = velocity #a vector
        
    def updatePosAndVel(self, force, time_step, thrust):
        acceleration = (force[0] / self.mass, force[1] / self.mass)
        self.velocity = (self.velocity[0] + acceleration[0] * time_step, 
                                self.velocity[1] + acceleration[1] * time_step)
        self.position = (self.position[0] + self.velocity[0] * time_step,
                         self.position[1] + self.velocity[1] * time_step)
        self.mass = self.mass + (thrust.getFuelMass() * thrust.getNumOfThrusters())
    def getPos(self):
        return (self.position[0], self.position[1] - EARTH_RADIUS)
    def getPosX(self):
      return self.position[0]
    def getPosY(self):
      return self.position[1]
    def getMass(self):
      return self.mass
    def getVelocity(self):
      return self.velocity


class thrust:
  def __init__(self, vol, fuelMass, burn, t, numberOfThrusters):
    self.vol = vol
    self.fuelMass = fuelMass
    self.burn = burn
    self.t = t
    self.numberOfThrusters = numberOfThrusters
  def getFuelMass(self):
    return self.fuelMass
  def getNumOfThrusters(self):
    return self.numberOfThrusters


def thrustForce(thrusters):
  thrustPerThruster = 150000
  totalThrust = thrustPerThruster * thrusters.numberOfThrusters
  if thrusters.fuelMass > 0:
    thrusters.fuelMass -= thrusters.burn * time_step
    return (0, totalThrust)
  return (0,0)

def simulate(Spacecraft, duration, thrust):
    for _ in range(duration):
        Fth = thrustForce(thrust)
        Fg = gravForce(Spacecraft, earthPos)
        Fn = normForce(Spacecraft)
        force = (Fth[0] + Fg[0] + Fn[0], Fth[1] + Fg[1] + Fn[1])
        print("Thrust", Fth)
        print("Fuel Mass", thrust.getFuelMass())
        print("Gravity", Fg)
        print("Normal", Fn)
        print("Mass", Spacecraft.getMass())
        Spacecraft.updatePosAndVel(force, time_step, thrust)
        print("Velocity", Spacecraft.getVelocity())
        print("Position", Spacecraft.getPos())
        plt.plot(Spacecraft.getPosX(), Spacecraft.getPosY(), 'bo')
        plt.pause(0.01)  # Pause to update the plot (adjust the interval as needed)
        time.sleep(1) 


def gravForce(Spacecraft, earthPos):
    distanceX = Spacecraft.getPosX() - earthPos[0]
    distanceY = Spacecraft.getPosY() - earthPos[1]
    distance = (distanceX ** 2 + distanceY ** 2) ** .5
    gravForce = (GRAVITY * EARTH_MASS * Spacecraft.getMass()) / (distance ** 2)
    gravForceX = gravForce * distanceX / distance
    gravForceY = gravForce * distanceY / distance
    return (-gravForceX, -gravForceY)

def normForce(Spacecraft):
    Fg = gravForce(Spacecraft, earthPos)
    if Spacecraft.getPosY() <= EARTH_RADIUS:
        return (-Fg[0], -Fg[1])
    return (0,0)



thrusters = thrust(100, 150, 2.5, t, 2)
firstSpaceCraft = Spacecraft(13000, (0,EARTH_RADIUS), (0, 0), thrusters)

plt.figure(figsize = (8, 8))  # Adjust the figure size as needed
plt.axis('equal')  # Ensure the aspect ratio is equal for 2D simulation

simulate(firstSpaceCraft, 5, thrusters)
plt.show()
