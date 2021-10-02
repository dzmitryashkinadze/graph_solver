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
In the 2008 Olympics, Jamaican sprinter Usain Bolt shocked the world as he ran the 100-meter dash in 9.69 seconds. Determine Usain's average speed for the race.
SOLUTION:
'''
def test_1():
    a = GraphSolver(Model='ConsecLinearMovement_New')
    a.Import('d1', 100, 'm')
    a.Import('T1', 9.69, 's')
    a.Import_Solution('v1', 10.32, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 2:
In the Funny Car competition at the Joliet Speedway in Joliet, Illinois in October of 2004, John Force complete the 1/4-mile dragster race in a record time of 4.437 seconds. Determine the average speed of the dragster in mi/hr and m/s. GIVEN: (1.000 mi =1609 m)
'''
def test_2():
    a = GraphSolver(Model='ConsecLinearMovement_New')
    # converted miles to meters during the input of the data
    a.Import('d1', 1./4, 'mi')
    a.Import('T1', 4.437, 's')
    a.Import_Solution('v1', 90.68, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 3:
In the qualifying round of the 50-yd freestyle in the sectional swimming championship, Dugan got an early lead by finishing the first 25.00 yd in 10.01 seconds. Dugan finished the return leg (25.00 yd distance) in 10.22 seconds. a. Determine Dugan's average speed for the entire race. b. Determine Dugan's average speed for the first 25.00 yd leg of the race. c. Determine Dugan's average velocity for the entire race.
'''
def test_3():
    a = GraphSolver(Model='ConsecLinearMovement_New')
    a.Import('d1', 25, 'yd')
    a.Import('T1', 10.01, 's')
    a.Import('d2', -25, 'yd')
    a.Import('T2', 10.22, 's')
    a.Import('T3', 0, 's')
    a.Import('d3', 0, 'm')
    a.Import('T4', 0, 's')
    a.Import('d4', 0, 'm')
    a.Import_Solution('Vs_av', 2.26, 'meter / second')
    a.Import_Solution('v1', 2.28, 'meter / second')
    a.Import_Solution('V_av', 0.00, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 4:
In last week's Homecoming victory, Al Konfurance, the star halfback of South's football team, broke a tackle at the line of scrimmage and darted upfield untouched. He averaged 9.8 m/s for an 80-yard (73 m) score. Determine the time for Al to run from the line of scrimmage to the end zone.
'''
def test_4():
    a = GraphSolver(Model='ConsecLinearMovement_New')
    a.Import('d1', 73, 'm')
    a.Import('v1', 9.8, 'm/s')
    a.Import_Solution('T1', 7.45, 'second')
    result = a.Check()
    assert Test(result)







'''
PROBLEM 6:
Ken Runfast is the star of the cross-country team. During a recent morning run, Ken averaged a speed of 5.8 m/s for 12.9 minutes. Ken then averaged a speed of 6.10 m/s for 7.1 minutes. Determine the total distance which Ken ran during his 20 minute jog.
'''
def test_6():
    a = GraphSolver(Model='ConsecLinearMovement_New')
    a.Import('v1', 5.8, 'm/s')
    a.Import('T1', 12.9, 'minute')
    a.Import('v2', 6.1, 'm/s')
    a.Import('T2', 7.1, 'minute')
    a.Import('d3', 0, 'm')
    a.Import('d4', 0, 'm')
    a.Import_Solution('L_tot', 7087.80, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 7:
The Lamborghini Murcielago can accelerate from 0 to 27.8 m/s (100 km/hr or 62.2 mi/hr) in a time of 3.40 seconds. Determine the acceleration of this car in both m/s/s and mi/hr/s.
'''
def test_7():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v1', 27.8, 'm/s')
    a.Import('v0', 0, 'm/s')
    a.Import('T1', 3.4, 's')
    a.Import_Solution('a', 8.18, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 8:
Homer Agin leads the Varsity team in home runs. In a recent game, Homer hit a 96 mi/hr sinking curve ball head on, sending it off his bat in the exact opposite direction at 56 mi/hr. The actually contact between ball and bat lasted for 0.75 milliseconds. Determine the magnitude of the average acceleration of the ball during the contact with the bat. Express your answer in both mi/hr/s and in m/s/s. (Given: 1.00 m/s = 2.24 mi/hr)
'''
def test_8():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', -96, 'mi/hr')
    a.Import('v1', 56, 'mi/hr')
    a.Import('T1', 0.75, 's')
    a.Import_Solution('a', 90.60, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 9:
A Formula One car is a single-seat racing car with an open cockpit and substantial wings located in the front and rear. At high speeds, the aerodynamics of the car help to create a strong downward force which allows the car to brake from 27.8 m/s (100 km/hr or 62.2 mi/hr) to 0 in as small of a distance as 17 meters. Determine the deceleration rate (i.e., acceleration) achieved by such a car.
'''
def test_9():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', 27.8, 'm/s')
    a.Import('v1', 0, 'm/s')
    a.Import('d1', 17, 'm')
    a.Import_Solution('a', -22.73, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 10:
A Cessna 150 airplane has a takeoff speed of 28 m/s (63 mi/hr). Determine the minimum length of the runway which would be required for the plane to take off if it averages an acceleration of 1.9 m/s/s.
'''
def test_10():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', 1.9, 'm/s/s')
    a.Import('v1', 28, 'm/s')
    a.Import('v0', 0, 'm/s')
    a.Import_Solution('d1', 206.32, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 11:
Cynthia competes in luge competitions during the winter months. She rides solo on a small sled 3 inches off the ground down icy slopes, turning only by use of her feet and the shifting of her weight on the sled. During the initial stage of one downhill luge, Cynthia accelerated from rest at 6.84 m/s/s for 2.39 seconds. Determine the distance she moved during this acceleration phase.
'''
def test_11():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', 6.84, 'm/s/s')
    a.Import('T1', 2.39, 's')
    a.Import('v0', 0, 'm/s')
    a.Import_Solution('d1', 19.54, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 12:
Suzie Lavtaski has reached the end of the ski slope and abruptly decelerates from 29.0 m/s to 1.8 m/s in 1.45 seconds. Determine Suzie' acceleration rate and the distance she moved during this braking period.
'''
def test_12():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('T1', 1.45, 's')
    a.Import('v1', 1.8, 'm/s')
    a.Import('v0', 29.0, 'm/s')
    a.Import_Solution('a', -18.76, 'meter / second ** 2')
    a.Import_Solution('d1', 22.33, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 13:
Captain John Stapp is often referred to as the "fastest man on Earth." In the late 1940s and early 1950s, Stapp ran the U.S. Air Force's Aero Med lab, pioneering research into the accelerations which humans could tolerate and the types of physiological effects which would result. After several runs with a 185-pound dummy named Oscar Eightball, Captain Stapp decided that tests should be conducted upon humans. Demonstrating his valor and commitment to the cause, Stapp volunteered to be the main subject of subsequent testing. Manning the rocket sled on the famed Gee Whiz track, Stapp tested acceleration and deceleration rates in both the forward-sitting and backward-sitting positions. He would accelerate to aircraft speeds along the 1200-foot track and abruptly decelerate under the influence of a hydraulic braking system. On one of his most intense runs, his sled decelerated from 282 m/s (632 mi/hr) to a stop at -201 m/s/s. Determine the stopping distance and the stopping time.
'''
def test_13():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', -201, 'm/s/s')
    a.Import('v1', 0, 'm/s')
    a.Import('v0', 282, 'm/s')
    a.Import_Solution('d1', 197.82, 'meter')
    a.Import_Solution('T1', 1.40, 'second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 14:
Julietta and Jackson are playing miniature golf. Julietta's ball rolls into a long. straight upward incline with a speed of 2.95 m/s and accelerates at -0.876 m/s/s for 1.54 seconds until it reaches the top of the incline and then continues along an elevated section. Determine the length of the incline.
'''
def test_14():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', -0.876, 'm/s/s')
    a.Import('v0', 2.95, 'm/s')
    a.Import('T1', 1.54, 's')
    a.Import_Solution('d1', 3.50, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 15:
Rickey Henderson, baseball's record holder for stolen bases, approaches third base. He dives head first, hitting the ground at 6.75 m/s and reaching the base at 5.91 m/s, accelerating at -5.11 m/s/s. Determine the distance Rickey slides across the ground before touching the base.
'''
def test_15():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', -5.11, 'm/s/s')
    a.Import('v0', 6.75, 'm/s')
    a.Import('v1', 5.91, 'm/s')
    a.Import_Solution('d1', 1.04, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 16:
Win Blonehare and Kent Swimtashore are sailboating in Lake Gustastorm. Starting from rest near the shore, they accelerate with a uniform acceleration of 0.29 m/s/s, How far are they from the shore after 18 seconds?
'''
def test_16():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('a', 0.29, 'm/s/s')
    a.Import('v0', 0, 'm/s')
    a.Import('T1', 18, 's')
    a.Import_Solution('d1', 46.98, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 17:
For years, the tallest tower in the United States was the Phoenix Shot Tower in Baltimore, Maryland. The shot tower was used from 1828 to1892 to make lead shot for pistols and rifles and molded shot for cannons and other instruments of warfare. Molten lead was dropped from the top of the 234-foot (71.3 meter) tall tower into a vat of water. During its free fall, the lead would form a perfectly spherical droplet and solidify. Determine the time of fall and the speed of a lead shot upon hitting the water at the bottom.
'''
def test_17():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('d1', 71.3, 'm')
    a.Import('a', 9.81, 'm/s/s')
    a.Import('v0', 0, 'm/s')
    a.Import_Solution('T1', 3.81, 'second')
    a.Import_Solution('v1', 37.40, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 18:
According to Guinness, the tallest man to have ever lived was Robert Pershing Wadlow of Alton, Illinois. He was last measured in 1940 to be 2.72 meters tall (8 feet, 11 inches). Determine the speed which a quarter would have reached before contact with the ground if dropped from rest from the top of his head.
'''
def test_18():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('d1', 2.72, 'm')
    a.Import('a', 9.81, 'm/s/s')
    a.Import('v0', 0, 'm/s')
    a.Import_Solution('T1', 0.74, 'second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 19:
A California Condor is approaching its nest with a large chunk of carrion in its beak. As it approaches, it makes an upward swoop, achieving a momentary upward velocity of 12.8 m/s when the carrion falls from its mouth, hitting a cliff outcropping 32.1 m below. Determine the speed of the carrion upon hitting the outcropping.
'''
def test_19():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', -12.8, 'm/s')
    a.Import('d1', 32.1, 'm')
    a.Import('a', 9.81, 'm/s/s')
    a.Import_Solution('v1', 28.17, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 20:
During his recent skydiving adventure, Luke Autbeloe had reached a terminal speed of 10.4 m/s as he approached the ground with his parachute. During an attempt to snap one last photo with his camera, Luke fumbled it from a height of 52.1 m above the ground. a. Determine the speed with which the camera hits the ground. b. Determine the time for the camera to free fall from Luke's hands to the ground.
'''
def test_20():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', 10.4, 'm/s')
    a.Import('d1', 52.1, 'm')
    a.Import('a', 9.81, 'm/s/s')
    a.Import_Solution('v1', 33.62, 'meter / second')
    a.Import_Solution('T1', 2.37, 'second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 21:
The speed required of a military jet when taking off from the deck of an aircraft carrier is dependent upon the speed of the carrier and the speed of the wind into which the carrier is moving. The takeoff speed required of a military jet relative to the deck of the carrier is 45 m/s when the carrier travels at 45 mi/hr into a 20 mi/hr wind. And when the aircraft carrier is traveling at 10 mi/hr into a 5 mi/hr wind, the takeoff speed relative to the deck of the carrier is 71 m/s. Determine the acceleration which a military jet must have to take off under these two conditions from the 126-m long runway of the USS Ronald Reagan aircraft carrier.
'''
def test_21():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', 0, 'm/s')
    a.Import('v1', 45, 'm/s')
    a.Import('d1', 126, 'm')
    a.Import_Solution('a',8.04, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)

    b = GraphSolver(Model='LinearMovement_New')
    b.Import('v0', 0, 'm/s')
    b.Import('v1', 71, 'm/s')
    b.Import('d1', 126, 'm')
    b.Import_Solution('a', 20.00, 'meter / second ** 2')
    result = b.Check()
    assert Test(result)



'''
PROBLEM 22:
The Zero Gravity Research Facility at NASA-operated Glenn Research Center in Ohio is used to test the behavior of fluids, flames, equipment and other objects in free fall. It consists of a 467-foot long, 12-foot diameter, steel vacuum chamber. The steel chamber resides inside of a concrete lined shaft which extends 510 feet below ground level. Objects falling through the tower experience free fall over a distance of 432 feet (132 meters). a. Determine the falling time for objects dropped from rest. b. Determine the final speed of the objects before the braking period begins.
'''
def test_22():
    a = GraphSolver(Model='LinearMovement_New')
    a.Import('v0', 0, 'm/s')
    a.Import('d1', 132, 'm')
    a.Import('a', 9.81, 'm/s/s')
    a.Import_Solution('T1', 5.19, 'second')
    a.Import_Solution('v1', 50.89, 'meter / second')
    result = a.Check()
    assert Test(result)


# Very difficult to solve fully automatically!!!! Therefore I manually added an if branching at the end...
'''
PROBLEM 23:
It's breakfast time and Mr. H entertains himself once more by watching the daily beetle race across the 35.7-cm length of the Wheaties box top. Angie the beetle typically averages 3.77 mm/s and Bessie the beetle averages 4.78 mm/s. If Bessie gives Angie a 5.4 cm head start, then which beetle wins and by what distance?
'''
def test_23():
    b1 = GraphSolver(Model='ConsecLinearMovement_New')
    b1.Import('x0', 5.4, 'cm')
    b1.Import('x1', 35.7, 'cm')
    b1.Import('v1', 3.77, 'mm/s')
    b1.Import_Solution('T1', 80.37, 'second')
    result = b1.Check()
    assert Test(result)

    b2 = GraphSolver(Model='ConsecLinearMovement_New')
    b2.Import('d1', 35.7, 'cm')
    b2.Import('v1', 4.78, 'mm/s')
    b2.Import_Solution('T1', 74.69, 'second')
    result = b2.Check()
    assert Test(result)
