# Main library being tested
from physai import GraphSolver

# Library used for unit interconversions
import pint

# Library for coping of the class instances
import copy

# Registry entry used for all units
ureg = pint.UnitRegistry()


def Test(result):
    return result['solved']


'''
PROBLEM 1:
The first asteroid to be discovered is Ceres. It is the largest and most massive
 asteroid is our solar system's asteroid belt, having an estimated
  mass of 3.0 x 1021 kg and an orbital speed of 17900 m/s.
   Determine the amount of kinetic energy possessed by Ceres.
'''
def test_1():
    a = GraphSolver(Model='EnergyExchange', Debug = True)
    a.Import('m', 3.0e21, 'kg')
    a.Import('v1', 17900, 'm/s')
    a.Import_Solution('E_kin_1', 480614999999999998828430229504.00, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 2:
A 78-kg skydiver has a speed of 62 m/s at an altitude of 870 m above the ground.
a. Determine the kinetic energy possessed by the skydiver.
b. Determine the potential energy possessed by the skydiver.
c. Determine the total mechanical energy possessed by the skydiver.
'''
def test_2():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 78, 'kg')
    a.Import('v1', 62, 'm/s')
    a.Import('h1', 870, 'm')
    a.Import_Solution('E_kin_1', 149916.00, 'joule')
    a.Import_Solution('E_pot_1', 665706.60, 'joule')
    a.Import_Solution('E_tot', 815622.60, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 3:
Lee Ben Fardest (esteemed American ski jumper), has a mass of 59.6 kg. He is moving with a speed of 23.4 m/s at a height of 44.6 meters above the ground. Determine the total mechanical energy of Lee Ben Fardest.
'''
def test_3():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 59.6, 'kg')
    a.Import('v1', 23.4, 'm/s')
    a.Import('h1', 44.6, 'm')
    a.Import_Solution('E_tot', 42393.84, 'joule')
    result = a.Check()
    assert Test(result)


'''
PROBLEM 4:
Chloe leads South's varsity softball team in hitting. In a game against New Greer Academy this past weekend, Chloe slugged the 181-gram softball so hard that it cleared the outfield fence and landed on Lake Avenue. At one point in its trajectory, the ball was 28.8 m above the ground and moving with a speed of 19.7 m/s. Determine the total mechanical energy of the softball.
'''
def test_4():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 0.181, 'kg')
    a.Import('v1', 19.7, 'm/s')
    a.Import('h1', 28, 'm')
    a.Import_Solution('E_tot', 84.84, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 5:
Suzie Lavtaski (m=56 kg) is skiing at Bluebird Mountain. She is moving at 16 m/s across the crest of a ski hill located 34 m above ground level at the end of the run.
a. Determine Suzie's kinetic energy.
b. Determine Suzie's potential energy relative to the height of the ground at the end of the run.
c. Determine Suzie's total mechanical energy at the crest of the hill.
d. If no energy is lost or gained between the top of the hill and her initial arrival at the end of the run, then what will be Suzie's total mechanical energy at the end of the run?
e. Determine Suzie's speed as she arrives at the end of the run and prior to braking to a stop.
'''
def test_5():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 56, 'kg')
    a.Import('v1', 16, 'm/s')
    a.Import('h1', 34, 'm')
    a.Import('h2', 0, 'm')
    a.Import_Solution('E_kin_1', 7168.00, 'joule')
    a.Import_Solution('E_pot_1', 18678.24, 'joule')
    a.Import_Solution('E_tot', 25846.24, 'joule')
    a.Import_Solution('E_tot', 25846.24, 'joule')
    a.Import_Solution('v2', 30.38, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 6:
Nicholas is at The Noah's Ark Amusement Park and preparing to ride on The Point of No Return racing slide. At the top of the slide, Nicholas (m=72.6 kg) is 28.5 m above the ground.
a. Determine Nicholas' potential energy at the top of the slide.
b. Determine Nicholas's kinetic energy at the top of the slide.
c. Assuming negligible losses of energy between the top of the slide and his approach to the bottom of the slide (h=0 m), determine Nicholas's total mechanical energy as he arrives at the bottom of the slide.
d. Determine Nicholas' potential energy as he arrives at the bottom of the slide.
e. Determine Nicholas' kinetic energy as he arrives at the bottom of the slide.
f. Determine Nicholas' speed as he arrives at the bottom of the slide.
'''
def test_6():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 72.6, 'kg')
    a.Import('v1', 0, 'm/s')
    a.Import('h1', 28.5, 'm')
    a.Import('h2', 0, 'm')
    a.Import_Solution('E_pot_1', 20297.87, 'joule')
    a.Import_Solution('E_kin_1', 0.00, 'joule')
    a.Import_Solution('E_tot', 20297.87, 'joule')
    a.Import_Solution('E_pot_2', 0.00, 'joule')
    a.Import_Solution('E_kin_2', 20297.87, 'joule')
    a.Import_Solution('v2', 23.65, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 7:
Ima Scaarred (m=56.2 kg) is traveling at a speed of 12.8 m/s at the top of a 19.5-m high roller coaster loop.
a. Determine Ima's kinetic energy at the top of the loop.
b. Determine Ima's potential energy at the top of the loop.
c. Assuming negligible losses of energy due to friction and air resistance, determine Ima's total mechanical energy at the bottom of the loop (h=0 m).
d. Determine Ima's speed at the bottom of the loop.
'''
def test_7():
    a = GraphSolver(Model='EnergyExchange')
    a.Import('m', 56.2, 'kg')
    a.Import('v1', 12.8, 'm/s')
    a.Import('h1', 19.5, 'm')
    a.Import('h2', 0, 'm')
    a.Import_Solution('E_kin_1', 4603.90, 'joule')
    a.Import_Solution('E_pot_1', 10750.78, 'joule')
    a.Import_Solution('E_tot', 15354.68, 'joule')
    a.Import_Solution('v2', 23.38, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 8:
Renatta Gass is out with her friends. Misfortune occurs and Renatta and her friends find themselves getting a workout. They apply a cumulative force of 1080 N to push the car 218 m to the nearest fuel station. Determine the work done on the car.
'''
def test_8():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('F', 1080, 'N')
    a.Import('l', 218, 'm')
    a.Import_Solution('A', 235440.00, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 10:
Lamar Gant, U.S. powerlifting star, became the first man to deadlift five times his own body weight in 1985. Deadlifting involves raising a loaded barbell from the floor to a position above the head with outstretched arms. Determine the work done by Lamar in deadlifting 300 kg to a height of 0.90 m above the ground.
'''
def test_10():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('m', 300, 'kg')
    a.Import('l', 0.9, 'm')
    a.Import_Solution('A', 2648.70, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 12:
While training for breeding season, a 380 gram male squirrel does 32 pushups in a minute, displacing its center of mass by a distance of 8.5 cm for each pushup. Determine the total work done on the squirrel while moving upward (32 times).
'''
def test_12():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('m', 0.3, 'kg')
    a.Import('N_rep', 32, 'dimensionless')
    a.Import('l', 0.085, 'm')
    a.Import_Solution('A_rep', 8.00, 'joule')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 13:
During the Powerhouse lab, Jerome runs up the stairs, elevating his 102 kg body a vertical distance of 2.29 meters in a time of 1.32 seconds at a constant speed.
a. Determine the work done by Jerome in climbing the stair case.
b. Determine the power generated by Jerome.
'''
def test_13():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('m', 102, 'kg')
    a.Import('t', 1.32, 's')
    a.Import('l', 2.29, 'm')
    a.Import_Solution('A', 2291.42, 'joule')
    a.Import_Solution('P', 1735.92, 'watt')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 14:
A new conveyor system at the local packaging plan will utilize a motor-powered mechanical arm to exert an average force of 890 N to push large crates a distance of 12 meters in 22 seconds. Determine the power output required of such a motor.
'''
def test_14():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('F', 890, 'N')
    a.Import('t', 22, 's')
    a.Import('l', 12, 'm')
    a.Import_Solution('P', 485.45, 'watt')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 15:
Justin Thyme is traveling down Lake Avenue at 32.8 m/s in his 1510-kg 1992 Camaro.
He spots a police car with a radar gun and quickly slows down to a legal speed of 20.1 m/s.
a. Determine the initial kinetic energy of the Camaro.
b. Determine the kinetic energy of the Camaro after slowing down.
c. Determine the amount of work done on the Camaro during the deceleration.
'''
def test_15():
    a = GraphSolver(Model='WorkAndPower_New')
    a.Import('v', 16.8, 'm/s')
    a.Import('m', 1250, 'kg')
    a.Import_Solution('P', 206010.00, 'watt')
    result = a.Check()
    assert Test(result)
