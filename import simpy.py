import simpy
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

INTERVAL = 1
RAM_CAPACITY = 100
CPU_SPEED = 3
NUM_PROCESSES = 50

class Process:
    def __init__(self, env, id, ram, cpu):
        self.env = env
        self.id = id
        self.ram_required = random.randint(1, 10)
        self.instructions = random.randint(1, 10)
        self.cpu = cpu
        self.ram = ram
        self.start_time = 0
        self.end_time = 0
