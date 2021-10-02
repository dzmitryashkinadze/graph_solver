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
Dylan and Sophia are walking along Bluebird Lake on a perfectly calm day.
Dylan, determined to impress Sophia by his ability to skip rocks,
picks up the flattest rock he can find and gives it a sidearm launch
from the edge of the water. The rock acquires a completely horizontal
velocity of 26 m/s from a height of 0.45 m above the water surface.
a. How much time does it take the rock to fall to the water surface?
b. How far from the edge of the water does the rock travel before it
makes its first skip?
'''
def test_1():
    a = GraphSolver(Model='ThrowNew')
    a.Import('v0x', 26, 'm/s')
    a.Import('v0y', 0, 'm/s')
    a.Import('y0', 0.45, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('t1', 0.30, 'second')
    a.Import_Solution('x1', 7.88, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 2:
In an effort to create a cannonball-style splash, eight-year old Matthew runs off the edge of the board of the high dive at 4.6 m/s and falls 2.3 m to the water below. a. Determine the time for Matthew to fall the 2.3 m to the water. b. What horizontal distance from the edge of the board will Matthew plunge into the water? c. With what speed does Matthew enter the water?
'''
def test_2():
    a = GraphSolver(Model='ThrowNew', Trace=True)
    a.Import('v0x', 4.6, 'm/s')
    a.Import('v0y', 0, 'm/s')
    a.Import('y0', 2.3, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('t1', 0.68, 'second')
    a.Import_Solution('x1', 3.15, 'meter')
    a.Import_Solution('v1', 8.14, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 3:
Ima Peode wishes to throw a 2.8-kg pumpkin horizontally off the top of the school roof in order to hit Mr. H's car. The car is parked a distance of 13.4 m away from the base of the building below the point where Ima is standing. The building's roof is 10.4 m high. Assuming no air resistance, with what horizontal speed must Ima toss the pumpkin in order to hit Mr. H's car.
'''
def test_3():
    a = GraphSolver(Model='ThrowNew')
    a.Import('x1', 13.4, 'm')
    a.Import('v0y', 0, 'm/s')
    a.Import('y0', 10.4, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('v0x', 9.20, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 4:
The La Quebrada Cliff Divers provide daily entertainment for the crowds at Acapulco, Mexico. As a group of professional high divers, they dive off the cliff of La Quebrada and fall 45.1 m (148 feet) to the water below. More than an act of bravery, the cliff divers must time their dive so that they hit the water when the crest of an incoming wave has arrived. Determine the speed with which Pedro must run off the cliff in order to land in the water a horizontal distance of 17.8 m from the edge of the cliff.
'''
def test_4():
    a = GraphSolver(Model='ThrowNew')
    a.Import('x1', 17.8, 'm')
    a.Import('v0y', 0, 'm/s')
    a.Import('y0', 45.1, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('v0x', 5.87, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 5:
An emergency relief plane is dropping a care package from a plane to a group of medical personnel working for a relief agency in an African village. The package is designed to land in a small lake, inflate an attached raft upon impact, and finally resurface with the raft side down. The plane will be moving horizontally with a ground speed of 59.1 m/s. The package will be dropped a horizontal distance of 521 m from the intended target location. At what altitude above the pond must the plane be flying in order to successfully accomplish this feat?
'''
def test_5():
    a = GraphSolver(Model='ThrowNew')
    a.Import('v0x', 59.1, 'm/s')
    a.Import('v0y', 0, 'm/s')
    a.Import('y1', 0, 'm')
    a.Import('x1', 521, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('y0', 381.19, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 6:
The Choo Choo Restaurant in DesPlaines, IL is a 50's style diner which is notorious for the delivery of food from the kitchen to the dining room by an O-scale model train. Dinner baskets filled with hot dogs, hamburgers, French fries and the like are mounted to the tops of flatbed train cars and transported to table tops. On Matthew's fifth birthday, a French fry rolled off the top of the pile on a tight turn moving at a speed of 1.25 m/s and fell to the floor. a. Determine the time for the French fry to fall 113 cm from the top of the pile to the floor. b. Determine the horizontal displacement of the fry from the edge of the track. c. Determine the speed of the French fry upon striking the floor.
'''
def test_6():
    a = GraphSolver(Model='ThrowNew')
    a.Import('v0x', 1.25, 'm/s')
    a.Import('v0y', 0, 'm/s')
    a.Import('y0', 113, 'cm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('t1', 0.48, 'second')
    a.Import_Solution('x1', 0.60, 'meter')
    a.Import_Solution('v1', 4.87, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 7:
Aaron Agin and Bud Derfenger are lab partners who last year earned a reputation for breaking beakers, spilling acid, mixing the wrong chemicals, breaking thermometers and accidentally lighting Sophia's hair on fire with a Bunsen burner. And now to the delight of the physics class, Mr. H has made the mistake of allowing them to partner again. In a recent lab which utilized expensive tracks and carts, Aaron and Bud lived up to their reputation. Despite strong warnings from Mr. H, they allowed a cart to roll off the track and then off the table with a speed of 208 cm/s. The crash of the cart to the floor a horizontal distance of 96.3 cm from the table's edge turned the entire classroom silent. Use this information to determine the height of the lab tables in Mr. H's lab.
'''
def test_7():
    a = GraphSolver(Model='ThrowNew')
    a.Import('v0x', 208, 'cm/s')
    a.Import('v0y', 0, 'm/s')
    a.Import('x1', 96.3, 'cm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('y0', 1.05, 'meter')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 11:
On New Year's eve of 2007, Robbie Maddison set the world record for the longest motorcycle jump, traveling 98.3 m through the air from ramp to ramp. (The record has since been broken several times by Maddision himself.) Assuming a launch angle of 45, insignificant air resistance and a landing location at the same height as the launch height, determine the speed with which Maddison left the ramp.
'''
def test_11():
    a = GraphSolver(Model='ThrowNew')
    a.Import('x1', 98.3, 'm')
    a.Import('alpha', 45, 'degree')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import('y0', 0, 'm')
    a.Import_Solution('v0', 31.05, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 12:
Mr. Udadi takes his three children to the park for some summertime recreation. Olive Udadi is enjoying swinging and jumping. On one jump, Olive leaves the swing at a 30 angle to the horizontal with a speed of 2.2 m/s. She lands on the ground a horizontal distance of 1.09 m from the launch location. a. Determine the horizontal and the vertical components of the initial velocity. b. Determine the time which Olive is in the air. c. Determine the vertical height (relative to the landing location) from which Olive jumped.
'''
def test_12():
    a = GraphSolver(Model='ThrowNew')
    a.Import('v0', 2.2, 'm/s')
    a.Import('alpha', 30, 'degree')
    a.Import('x1', 1.09, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import_Solution('y0', 0.98, 'meter')
    a.Import_Solution('v0x', 1.91, 'meter / second')
    a.Import_Solution('v0y', 1.10, 'meter / second')
    a.Import_Solution('t1', 0.57, 'second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 13:
In an apparent effort to earn an appearance on the Destroyed in Seconds show, Caleb attempts a bicycle maneuver in which he jumps between two ramps whose elevated edges are located a distance of 1.8 meters apart. The ramps are angled at 35 and located at the same height. Determine the speed (in m/s and mi/hr) that Caleb must acquire to accomplish this stunt. (Given: 1.00 m/s', 2.24 mi/hr)
'''
def test_13():
    a = GraphSolver(Model='ThrowNew')
    a.Import('alpha', 35, 'degree')
    a.Import('x1', 1.8, 'm')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import('y0', 0, 'm')
    a.Import_Solution('v0', 4.33, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 14:
Albert is South's star punter for the varsity football team. His best hang time this past season was for a punt which he kicked at 74 above the horizontal. The punt had a 6.2 second hang time. a. Determine the speed at which the ball was punted. b. Determine the horizontal distance which the ball traveled.
'''
def test_14():
    a = GraphSolver(Model='ThrowNew')
    a.Import('alpha', 74, 'degree')
    a.Import('t1', 6.2, 's')
    a.Import('y1', 0, 'm')
    a.Import('x0', 0, 'm')
    a.Import('y0', 0, 'm')
    a.Import_Solution('v0', 31.64, 'meter / second')
    a.Import_Solution('x1', 54.07, 'meter')
    result = a.Check()
    assert Test(result)
