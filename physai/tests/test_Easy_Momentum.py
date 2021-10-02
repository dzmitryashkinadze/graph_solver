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
Determine the momentum of
a. an electron (m= 9.1 x10-31 kg) moving at 2.18 x 106 m/s (as if it were in a Bohr orbit in the H atom).
b. a 0.45 Caliber bullet (m = 0.162 kg) leaving the muzzle of a gun at 860 m/s.
c. a 110-kg professional fullback running across the line at 9.2 m/s.
d. a 360,000-kg passenger plane taxiing down a runway at 1.5 m/s
'''
def test_1():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 0.162, 'kg')
    a.Import('v1', 860, 'm/s')
    a.Import_Solution('p1', 139.32, 'kilogram * meter / second')
    result = a.Check()
    assert Test(result)







'''
PROBLEM 3:
According to the Guinness Book of World Records, the fastest recorded baseball pitch was delivered by Nolan Ryan in 1974. The pitch was clocked at 100.9 mi/hr (45.0 m/s). Determine the impulse required to give a 0.145-kg baseball such a momentum.
'''
def test_3():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 0.145, 'kg')
    a.Import('v1', 45, 'm/s')
    a.Import_Solution('p1', 6.53, 'kilogram * meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 4:
Jerome plays middle linebacker for South's varsity football team. In a game against cross-town rival North, he delivered a hit to North's 82-kg running back, changing his eastward velocity of 5.6 m/s into a westward velocity of 2.5 m/s.
a. Determine the initial momentum of the running back.
b. Determine the final momentum of the running back.
c. Determine the momentum change of the running back.
d. Determine the impulse delivered to the running back.
'''
def test_4():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 82, 'kg')
    a.Import('v1', 5.6, 'm/s')
    a.Import('v2', -2.5, 'm/s')
    a.Import_Solution('p1', 459.20, 'kilogram * meter / second')
    a.Import_Solution('p2', -205.00, 'kilogram * meter / second')
    a.Import_Solution('Delta_p', -664.20, 'kilogram * meter / second')
    a.Import_Solution('Delta_p', -664.20, 'kilogram * meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 5:
Kara Less was applying her makeup when she drove into South's busy parking lot last Friday morning. Unaware that Lisa Ford was stopped in her lane 30 feet ahead, Kara rear-ended Lisa's rented Taurus. Kara's 1300-kg car was moving at 11 m/s and stopped in 0.14 seconds.
a. Determine the momentum change of Kara's car.
b. Determine the impulse experienced by Kara's car.
c. Determine the magnitude of the force experienced by Kara's car.
'''
def test_5():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 1300, 'kg')
    a.Import('v1', 11, 'm/s')
    a.Import('v2', 0, 'm/s')
    a.Import('Delta_t', 0.14, 's')
    a.Import_Solution('Delta_p', -14300.00, 'kilogram * meter / second')
    a.Import_Solution('Delta_p', -14300.00, 'kilogram * meter / second')
    a.Import_Solution('F', -102142.86, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 6:
An interesting story is often told of baseball star Johnny Bench when he was a rookie catcher in 1968. During a Spring Training game, he kept signaling to star pitcher Jim Maloney to throw a curve ball. Maloney continuously shook off Bench's signal, opting to throw fastballs instead. The rookie catcher walked to the mound and told the veteran Maloney that his fastball wasn't fast enough and that he should throw some curve balls. Bench again signaled for a curve. Maloney shook of the signal and threw a fastball. Before the ball reached the plate, Bench took off his glove; he then caught the pitch barehanded.
a. Determine the impulse required to stop a 0.145-kg baseball moving at 35.7 m/s (80.0 mi/hr).
b. If this impulse is delivered to the ball in 0.020 seconds, then what is magnitude of the force acting between the bare hand and the ball?
'''
def test_6():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 0.145, 'kg')
    a.Import('v1', 35.7, 'm/s')
    a.Import('v2', 0, 'm/s')
    a.Import('Delta_t', 0.02, 's')
    a.Import_Solution('Delta_p', -5.18, 'kilogram * meter / second')
    a.Import_Solution('F', -258.82, 'kilogram * meter / second ** 2')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 8:
NASA's Langley Research Center has been experimenting with the use of air bags to soften the landings of crew exploration vehicles (CEV) on land. What stopping time will be required in order to safely stop a 7250 kg CEV moving at 7.65 m/s with an average force of 426000 N (an average force of 6 Gs)?
'''
def test_8():
    a = GraphSolver(Model='Momentum')
    a.Import('m', 7250, 'kg')
    a.Import('v1', 7.65, 'm/s')
    a.Import('v2', 0, 'm/s')
    a.Import('F', -426000, 'N')
    a.Import_Solution('Delta_t', 0.13, 'second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 9:
In a study conducted by a University of Illinois researcher, the football team at Unity High School in Tolono, IL was equipped for an entire season with helmets containing accelerometers. Information about every impact in practice and in games was sent to a computer present on the sidelines. The study found that the average force on a top of the head impact was 1770 N and endured for 7.78 milliseconds. Using a head mass of 5.20 kg and presuming the head to be a free body, determine the velocity change experienced in such an impact.
'''
def test_9():
    a = GraphSolver(Model='Momentum')
    a.Import('F', 1770, 'N')
    a.Import('v2', 0, 'm/s')
    a.Import('Delta_t', 7.78e-3, 's')
    a.Import('m', 5.2, 'kg')
    a.Import_Solution('v1', -2.65, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 10:
Mr. H ignites the enthusiasm of the class with a home-made cannon demonstration. The 1.27-kg cannon is loaded with a 54-gram tennis ball and placed on the floor. Mr. H adds the fuel, waits for its vapors to fill the reaction chamber and then brings a match nearby. The explosion stuns the crowd and propels the ball forward. A photogate measurement determines that the cannon recoiled backwards with a speed of 7.8 m/s. Determine the speed of the ball.
'''
def test_10():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 1.27, 'kg')
    a.Import('m2', 0.054, 'kg')
    a.Import('v1_0', 0, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v1_1', -7.8, 'm/s')
    a.Import_Solution('v2_1', 183.44, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 11:
An 82-kg male and a 48-kg female pair figure skating team are gliding across the ice at 7.4 m/s, preparing for a throw jump maneuver. The male skater tosses the female skater forward with a speed of 8.6 m/s. Determine the speed of the male skater immediately after the throw.
'''
def test_11():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 82, 'kg')
    a.Import('m2', 48, 'kg')
    a.Import('v1_0', 7.4, 'm/s')
    a.Import('v2_0', 7.4, 'm/s')
    a.Import('v2_1', 8.6, 'm/s')
    a.Import_Solution('v1_1', 6.70, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 12:
A candy-filled pinata is hung from a tree for Matthew s birthday. During an unsuccessful attempt to break the 4.4-kg pinata, Hayden cracks it with a 0.54-kg stick moving at 4.8 m/s. The stick stops and the pinata undergoes a gentle swinging motion. Determine the swing speed of the pinata immediately after being cracked by the stick.
'''
def test_12():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 4.4, 'kg')
    a.Import('m2', 0.54, 'kg')
    a.Import('v1_0', 0, 'm/s')
    a.Import('v2_0', 4.8, 'm/s')
    a.Import('v2_1', 0, 'm/s')
    a.Import_Solution('v1_1', 0.59, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 13:
During an in-class demonstration of momentum change and impulse, Mr. H asks Jerome (102 kg) and Michael (98 kg) to sit on a large 14-kg skate cart. Mr. H asks Suzie (44 kg) to sit on a second 14-kg skate cart. The two carts are placed on low friction boards in the hallway. Jerome pushes off of Suzie's cart. Measurements are made to determine that Suzie's cart acquired a post-impulse speed of 9.6 m/s. Determine the expected recoil speed of Jerome and Michael's cart.
'''
def test_13():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1_1', 102, 'kg')
    a.Import('m1_2', 98, 'kg')
    a.Import('m1_3', 14, 'kg')
    a.Import('m2_1', 44, 'kg')
    a.Import('m2_2', 14, 'kg')
    a.Import('m2_3', 0, 'kg')
    a.Import('v1_0', 0, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v2_1', 9.6, 'm/s')
    a.Import_Solution('v1_1', -2.60, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 14:
A 70.9-kg boy and a 43.2-kg girl, both wearing skates face each other at rest on a skating rink. The boy pushes the girl, sending her eastward with a speed of 4.64 m/s. Neglecting friction, determine the subsequent velocity of the boy.
'''
def test_14():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 70.9, 'kg')
    a.Import('m2', 43.2, 'kg')
    a.Import('v1_0', 0, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v2_1', 4.64, 'm/s')
    a.Import_Solution('v1_1', -2.83, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 15:
To Mr. H's disgust, a 450-g black crow is raiding the recently-filled bird feeder. As Mr. H runs out the back door with his broom in an effort to scare the crow away, it pushes off the 670-gram feeder with a takeoff speed of 1.5 m/s. Determine the speed at which the feeder initially recoils backwards.
'''
def test_15():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 0.450, 'kg')
    a.Import('m2', 0.67, 'kg')
    a.Import('v1_0', 0, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v1_1', 1.5, 'm/s')
    a.Import_Solution('v2_1', -1.01, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 16:
Jaclyn plays singles for South's varsity tennis team. During the match against North, Jaclyn won the sudden death tiebreaker point with a cross-court passing shot. The 57.5-gram ball hit her racket with a northward velocity of 26.7 m/s. Upon impact with her 331-gram racket, the ball rebounded in the exact opposite direction (and along the same general trajectory) with a speed of 29.5 m/s.
a. Determine the pre-collision momentum of the ball.
b. Determine the post-collision momentum of the ball.
c. Determine the momentum change of the ball.
d. Determine the velocity change of the racket.
'''
def test_16():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 0.0575, 'kg')
    a.Import('m2', 0.331, 'kg')
    a.Import('v1_0', 26.7, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v1_1', -29.5, 'm/s')
    a.Import_Solution('p1_0', 1.54, 'kilogram * meter / second')
    a.Import_Solution('p1_1', -1.70, 'kilogram * meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 17:
Anna Litical and Noah Formula are doing The Cart and the Brick Lab. They drop a brick on a 2.6 kg cart moving at 28.2 cm/s. After the collision, the dropped brick and cart are moving together with a velocity of 15.7 cm/s. Determine the mass of the dropped brick.
'''
def test_17():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 2.6, 'kg')
    a.Import('v1_0', 0.282, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v1_1', 0.157, 'm/s')
    a.Import('v2_1', 0.157, 'm/s')
    a.Import_Solution('m2', 2.07, 'kilogram')
    result = a.Check()
    assert Test(result)



# '''
# PROBLEM 18:
# A Roller Derby exhibition recently came to town. They packed the gym for two consecutive weekend nights at South's field house. On Saturday evening, the 68-kg Anna Mosity was moving at 17 m/s when she collided with 76-kg Sandra Day O'Klobber who was moving forward at 12 m/s and directly in Anna's path. Anna jumped onto Sandra's back and the two continued moving together at the same speed. Determine their speed immediately after the collision.
# '''
# def test_18():
#     a = GraphSolver(Model='TwoBodyColissionMomentum_New')
#     a.Import('m1 = 68, 'kg')
#     a.Import('m2 = 76, 'kg')
#     a.Import('v1_0 = 17, 'm/s')
#     a.Import('v2_0 = 12, 'm/s')
#     a.Import('v1_1 = v2_1')
#     Solution = a.Interactive_Solving_Hidden(VarName='v1_1')
#     assert Test(Solution, 14.36, 'meter / second')



# '''
# PROBLEM 19:
# Ima Rilla Saari rushes to her car in order to hurry home and get dressed for work. Failing to realize the dangers of driving under slick and icy conditions, she collides her 940-kg Mazda Miata into the rear of a 2460-kg pick-up truck which was at rest at the light on Lake Avenue. Ima's pre-collision speed was 12.5 m/s. Determine the post-collision speed of the two entangled cars as they slide across the ice.
# '''
# def test_19():
#     a = GraphSolver(Model='TwoBodyColissionMomentum_New')
#     a.Import('m1 = 940 kg')
#     a.Import('m2 = 2460 kg')
#     a.Import('v1_0 = 12.5 m/s')
#     a.Import('v2_0 = 0 m/s')
#     a.Import('v1_1 = v2_1')
#     Solution = a.Interactive_Solving_Hidden(VarName='v1_1')
#     assert Test(Solution, 3.46, 'meter / second')



# '''
# PROBLEM 20:
# In a goal line stand against New Greer Academy, South's linebackers Jerome (m=102 kg) and Michael (m=98 kg) meet the 84-kg halfback moving southward through the air at 6.4 m/s. Upon contact, Jerome and Michael are both moving at 3.6 m/s in the exact opposite direction. Determine the post-collision speed and direction of the collection of three players. Assume they move together after the collision.
# '''
# def test_20():
#     a = GraphSolver(Model='TwoBodyColissionMomentum_New')
#     a.Import('m1_1 = 102 kg')
#     a.Import('m1_2 = 98 kg')
#     a.Import('m1_3 = 0 kg')
#     a.Import('m2 = 84 kg')
#     a.Import('v1_0 = 3.6 m/s')
#     a.Import('v2_0 = -6.4 m/s')
#     a.Import('v1_1 = v2_1')
#     Solution = a.Interactive_Solving_Hidden(VarName='v1_1')
#     assert Test(Solution, 0.64, 'meter / second')



# '''
# PROBLEM 21:
# Hayden (m=24.3-kg) is gliding along the sidewalk on his skateboard at 8.6 ft/s. As he travels under a low-hanging branch of the tree where Matthew is sitting, he grabs the 4.5-kg bag of soccer balls from Matthew's hands. Determine the speed of Hayden immediately after grabbing the bag of soccer balls.
# '''
# def test_21():
#     a = GraphSolver(Model='TwoBodyColissionMomentum_New')
#     a.Import('m1 = 24.3 kg')
#     a.Import('m2 = 4.5 kg')
#     a.Import('v1_0 = 8.6 ft/s')
#     a.Import('v2_0 = 0 m/s')
#     a.Import('v1_1 = v2_1')
#     Solution = a.Interactive_Solving_Hidden(VarName='v1_1')
#     assert Test(Solution, 2.21, 'meter / second')



'''
PROBLEM 22:
Rex (m=86 kg) and Tex (92 kg) board the bumper cars at the local carnival. Rex is moving at a full speed of 2.05 m/s when he rear-ends Tex who is at rest in his path. Tex and his 125-kg car lunge forward at 1.40 m/s. Determine the post-collision speed of Rex and his 125-kg car.
'''
def test_22():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1_1', 86, 'kg')
    a.Import('m1_2', 125, 'kg')
    a.Import('m1_3', 0, 'kg')
    a.Import('m2_1', 92, 'kg')
    a.Import('m2_2', 125, 'kg')
    a.Import('m2_3', 0, 'kg')
    a.Import('v1_0', 2.05, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v1_1', 1.4, 'm/s')
    a.Import_Solution('v2_1', 0.63, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 23:
Polly Ester and Ray Ahn are doing the Elastic Collision lab on a low-friction track. Cart A has a mass of 1.00 kg and is moving rightward at 27.6 cm/s prior to the collision with Cart B. Cart B has a mass of 0.50 kg and is moving leftward with a speed of 42.9 cm/s. After the magnetic repulsion of the two carts, Cart A is moving leftward at 10.1 cm/s. Determine the post-collision speed and direction of cart B.
'''
def test_23():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 1, 'kg')
    a.Import('m2', 0.5, 'kg')
    a.Import('v1_0', 0.276, 'm/s')
    a.Import('v2_0', -0.429, 'm/s')
    a.Import('v1_1', -0.101, 'm/s')
    a.Import_Solution('v2_1', 0.33, 'meter / second')
    result = a.Check()
    assert Test(result)



'''
PROBLEM 24:
Bailey is on the tenth frame of her recent bowling competition and she needs to pick up the last pin for a spare and the first place trophy. She rolls the 7.05-kg ball down the lane and it hits the 1.52-kg pin head on. The ball was moving at 8.24 m/s before the collision. The pin went flying forward at 13.2 m/s. Determine the post-collision speed of the ball.
'''
def test_24():
    a = GraphSolver(Model='TwoBodyColissionMomentum_New')
    a.Import('m1', 7.05, 'kg')
    a.Import('m2', 1.52, 'kg')
    a.Import('v1_0', 8.24, 'm/s')
    a.Import('v2_0', 0, 'm/s')
    a.Import('v2_1', 13.2, 'm/s')
    a.Import_Solution('v1_1', 5.39, 'meter / second')
    result = a.Check()
    assert Test(result)
