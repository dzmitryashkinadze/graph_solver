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
An African elephant can reach heights of 13 feet and possess a mass of as much as 6000 kg. Determine the weight of an African elephant in Newtons and in pounds. (Given: 1.00 N = .225 pounds)
'''
def test_1():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 6000, 'kg')
    a.Import('g-factor', 1, 'dimensionless')
    a.Import_Solution('F_g', 58860.00, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 2:
About twenty percent of the National Football League weighs more than 300 pounds. At this weight, their Body Mass Index (BMI) places them at Grade 2 obesity, which is one step below morbid obesity. Determine the mass of a 300 pound (1330 N) football player.
'''
def test_2():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 300, 'pound')
    a.Import('g-factor', 1, 'dimensionless')
    a.Import_Solution('m', 136.08, 'kilogram')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 3:
According to the National Center for Health Statistics, the average mass of an adult American male is 86 kg. Determine the mass and the weight of an 86-kg man on the moon where the gravitational field is one-sixth that of the Earth.
'''
def test_3():
    a = GraphSolver(Model='2ndNewtonLaw_New', Debug=True )
    a.Import('m', 86, 'kg')
    a.Import('g-factor', 1./6, 'dimensionless')
    a.Import_Solution('F_tot', 140.61, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 4:
The rising concern among athletic trainers and health advocates (and parents) regarding concussions and multiple concussions among high school football players has prompted numerous studies of the effectiveness of protective head gear and the forces and accelerations experienced by players. One study suggested that there is a 50% chance of concussions for impacts rated at 75 g's of acceleration (i.e., 75 multiplied by 9.8 m/s/s). (The average head impact results in 22 to 24 g's of acceleration.) If a player's head mass (with helmet) is 6.0 kg and considered to be a free body, then what net force would be required to produce an acceleration of 75 g's?
'''
def test_4():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 6, 'kg')
    a.Import('g-factor', 75, 'dimensionless')
    a.Import_Solution('F_tot', 4414.50, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 5:
Captain John Stapp of the U.S. Air Force tested the human limits of acceleration by riding on a rocket sled of his own design, known as the Gee Whiz. What net force would be required to accelerate the 82-kg Stapp at 450 m/s/s (the highest acceleration tested by Stapp)?
'''
def test_5():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 82, 'kg')
    a.Import('a', 450, 'm/s/s')
    a.Import_Solution('F_tot', 36900.00, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 6:
Sophia, whose mass is 52 kg, experienced a net force of 1800 N at the bottom of a roller coaster loop during her school's physics field trip to the local amusement park. Determine Sophia's acceleration at this location.
'''
def test_6():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 52, 'kg')
    a.Import('F_tot', 1800, 'N')
    a.Import_Solution('a', 34.62, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 9:
It's Friday night and Skyler has been assigned the noble task of baby-sitting Casey, his 2-year old brother. He puts a crash helmet on Casey, places him in the red wagon and takes him on a stroll through the neighborhood. As Skyler starts across the street, he exerts a 52 N forward force on the wagon. There is a 24 N resistance force and the wagon and Casey have a combined weight of 304 N. Construct a free body diagram depicting the types of forces acting upon the wagon. Then determine the net force, mass and acceleration of the wagon.
'''
def test_9():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('F1', 52, 'N')
    a.Import('F2', -24, 'N')
    a.Import('F3', 0, 'N')
    a.Import('F_g', 304, 'N')
    a.Import_Solution('F_tot', 28.00, 'kilogram * meter / second ** 2')
    a.Import_Solution('m', 30.99, 'kilogram')
    a.Import_Solution('a', 0.90, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 10:
After a lead-off single in the 8th inning, Earl makes an effort to steal second base. As he hits the dirt on his head first dive, his 73.2 kg body encounters 249 N of friction force. Construct a free body diagram depicting the types of forces acting upon Earl. Then determine the net force and acceleration.
'''
def test_10():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 73.2, 'kg')
    a.Import('F_tot', 249, 'N')
    a.Import_Solution('a', 3.40, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 11:
Mira and Tariq are lab partners for the Pulley and Bricks Lab. They have determined that the 2.15-kg brick is experiencing a forward tension force of 9.54 N and a friction force of 8.69 N as it is accelerated across the table top. Construct a free body diagram depicting the types of forces acting upon the brick. Then determine the net force and acceleration of the brick.
'''
def test_11():
    a = GraphSolver(Model='2ndNewtonLaw_New')
    a.Import('m', 2.15, 'kg')
    a.Import('F1', 9.54, 'N')
    a.Import('F2', -8.69, 'N')
    a.Import('F3', 0, 'N')
    a.Import_Solution('F_tot', 0.85, 'kilogram * meter / second ** 2')
    a.Import_Solution('a', 0.40, 'meter / second ** 2')
    result = a.Check()
    assert Test(result)



# '''
# PROBLEM 12:
# Moments after making the dreaded decision to jump out the door of the airplane, Darin's 82.5-kg body experiences 118 N of air resistance. Determine Darin's acceleration at this instant in time. HINT: begin by drawing a free body diagram and determine the net force.
# '''
# def test_12():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     #a.Import('m', 82.5)
#     a.Import('m', 82.5 kg')
#     a.Import('F2', -118 N')
#     a.Import('F1', F_g')
#     a.Import('F3 = 0 N')
#     SolutionA = a.Interactive_Solving_Hidden(VarName='F_tot')
#     SolutionB = a.Interactive_Solving_Hidden(VarName='a')
#     assert Test(SolutionA, 691.33, 'newton')
#     assert Test(SolutionB, 8.38, 'meter / second ** 2')



# '''
# PROBLEM 14:
# Skydiving tunnels have become popular attractions, appealing in part to those who would like a taste of the skydiving experience but are too overwhelmed by the fear of jumping out of a plane at several thousand feet. Skydiving tunnels are vertical wind tunnels through which air is blown at high speeds, allowing visitors to experience bodyflight. On Natalya's first adventure inside the tunnel, she changes her orientation and for an instant, her 46.8-kg body momentarily experiences an upward force of air resistance of 521 N. Determine Natalya's acceleration during this moment in time.
# '''
# def test_14():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 46.8 kg')
#     a.Import('F2 = -521 N')
#     a.Import('F3 = 0 N')
#     a.Import('F1 = F_g')
#     Solution = a.Interactive_Solving_Hidden(VarName='a')
#     assert Test(Solution, -1.32, 'meter / second ** 2')



# '''
# PROBLEM 16:
# A 0.104-kg model rocket accelerates at 45.9 m/s/s on takeoff. Determine the upward thrust experienced by the rocket.
# '''
# def test_16():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 0.104 kg')
#     a.Import('a = -45.9 m/s/s')
#     a.Import('F2 = F_g')
#     a.Import('F3 = 0 N')
#     Solution = a.Interactive_Solving_Hidden(VarName='F1')
#     assert Test(Solution, -5.79, 'newton')



# '''
# PROBLEM 18:
# Alejandra is attempting to drag her 32.6-kg Golden Retriever across the wooden
# floor by applying a horizontal force. What force must she apply to move the dog
# with a constant speed of 0.95 m/s? The coefficient of friction between the dog
# and the floor is 0.72.
# '''
# def test_18():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 32.6 kg')
#     a.Import('F_tot = 0 N')
#     a.Import('mu = 0.72')
#     a.Import('F2 = F_fr')
#     a.Import('F3 = 0 N')
#     Solution = a.Interactive_Solving_Hidden(VarName='F1')
#     assert Test(Solution, -230.26, 'newton')



# '''
# PROBLEM 19:
# The coefficient of friction between the wheels of Dawson's 1985 Ford Coupe and the dry pavement is 0.85. Determine the acceleration which the 1300-kg Coupe experiences while skidding to a stop.
# '''
# def test_19():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 1300 kg')
#     a.Import('mu = 0.85')
#     a.Import('F_tot = F_fr')
#     Solution = a.Interactive_Solving_Hidden(VarName='a')
#     assert Test(Solution, 8.34, 'meter / second ** 2')



# '''
# PROBLEM 21:
# Unbeknownst to most students, every time the school floors are waxed, the physics teachers get together to have a barrel of phun doing friction experiments in their socks (uhm - they do have clothes on; its just that they don't have any shoes on their feet). On one occasion, Mr. London applies a horizontal force to accelerate Mr. Schneider (mass of 84 kg) rightward at a rate of 1.2 m/s/s. If the coefficient of friction between Mr. Schneider 's socks and the freshly waxed floors is 0.35, then with what force (in Newtons) must Mr. London be pulling?
# '''
# def test_21():
#     a = GraphSolver(Model='2ndNewtonLaw_New', Debug= True)
#     a.Import('m = 84 kg')
#     a.Import('F_tot = F_fr * -1')
#     a.Import('a = 1.2 m/s/s')
#     Solution = a.Interactive_Solving_Hidden(VarName='F_tot')
#     assert Test(Solution, 100.80, 'newton')


#
# '''
# PROBLEM 22:
# Dexter Eius is running through the cafeteria when he slips on some mashed potatoes and falls to the floor. (Let that be a lesson for Dexter.) Dexter lands in a puddle of milk and skids to a stop with an acceleration of -4.8 m/s/s. Dexter weighs 780 Newtons. Determine the coefficient of friction between Dexter and the milky floor.
# '''
# def test_22():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('F_g = 780 N')
#     a.Import('F_tot = F_fr * -1')
#     a.Import('a = -4.8 m/s/s')
#     Solution = a.Interactive_Solving_Hidden(VarName='mu')
#     assert Test(Solution, 0.49, 'dimensionless')



# '''
# PROBLEM 23:
# The Harrier Jump Jet is a fixed wing military jet designed for vertical takeoff and landing (VTOL). It is capable of rotating its jets from a horizontal to a vertical orientation in order to takeoff, land and conduct horizontal maneuvers. Determine the vertical thrust required to accelerate an 8600-kg Harrier upward at 0.40 m/s/s.
# '''
# def test_23():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 8600 kg')
#     a.Import('F2 = F_g * -1')
#     a.Import('F3 = 0 N')
#     a.Import('a = 0.4 m/s/s')
#     Solution = a.Interactive_Solving_Hidden(VarName='F1')
#     assert Test(Solution, 87806.00, 'newton')



# '''
# PROBLEM 24:
# While skydiving, Dee Selerate opens her parachute and her 53.4-kg body immediately accelerates upward for an instant at 8.66 m/s/s. Determine the upward force experienced by Dee during this instant.
# '''
# def test_24():
#     a = GraphSolver(Model='2ndNewtonLaw_New')
#     a.Import('m = 53.4 kg')
#     a.Import('F2 = F_g * -1')
#     a.Import('F3 = 0 N')
#     a.Import('a = 8.66 m/s/s')
#     Solution = a.Interactive_Solving_Hidden(VarName='F1')
#     assert Test(Solution, 986.30, 'newton')
