import simpy
import random

def pedestrian_source(env, population, delay):
    for i in range(1, population+1):
        yield env.timeout(random.expovariate(1.0 / delay))
        env.process(pedestrian(env, i))

def pedestrian(env, id):
    print(f"Pedestrian {id} arrives at time {env.now}")
    gate = random.randint(1, 16)
    yield env.process(pedestrian_goto(env, id, gate))
    print(f"Pedestrian {id} reaches the gate {gate} at time {env.now}")
    population.discard(id)

def pedestrian_goto(env, id, gate):
    print(f"Pedestrian {id} starts moving to gate {gate} at time {env.now}")
    yield env.timeout(random.uniform(1, 5))

population = set()
evacuation_time = 0

def emergency(env, delay):
    global evacuation_time
    yield env.timeout(delay)
    print(f"Emergency occurs at time {env.now}")
    start_time = env.now
    for ped in list(population):
        env.process(pedestrian_goto(env, ped, random.randint(1, 16)))
        population.discard(ped)
    evacuation_time = env.now - start_time

env = simpy.Environment()

# Set your parameters
population_size = 50
emergency_delay = 1

#Run the process and print the evacuation time
env.process(pedestrian_source(env, population_size, 5))
env.process(emergency(env, emergency_delay))
env.run()
