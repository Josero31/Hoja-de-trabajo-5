import simpy
import random
import statistics

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

INTERVAL = 10
RAM_CAPACITY = 200
CPU_SPEED = 3
NUM_PROCESSES = 200

# Lista para almacenar los tiempos de finalización de todos los procesos
process_times = []

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

    def run(self):
        self.start_time = self.env.now
        print(f"Proceso {self.id} iniciado en tiempo {self.start_time}")
        yield self.env.process(self.get_ram())
        yield self.env.process(self.run_instructions())
        self.end_time = self.env.now
        print(f"Proceso {self.id} terminado en tiempo {self.end_time}")
        self.ram.put(self.ram_required)
        process_times.append(self.end_time - self.start_time)

    def get_ram(self):
        print(f"Proceso {self.id} solicitando RAM")
        yield self.ram.get(self.ram_required)

    def run_instructions(self):
        while self.instructions > 0:
            with self.cpu.request() as req:
                yield req
                yield self.env.timeout(1)
                self.instructions -= min(CPU_SPEED, self.instructions)
                print(f"Proceso {self.id} ejecutando instrucciones, restantes: {self.instructions}")

def process_generator(env, ram, cpu):
    for i in range(NUM_PROCESSES):
        process = Process(env, i, ram, cpu)
        env.process(process.run())
        yield env.timeout(random.expovariate(1.0 / INTERVAL))

env = simpy.Environment()
ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
cpu = simpy.Resource(env, capacity=1)
env.process(process_generator(env, ram, cpu))

env.run()

# Al final del programa, calculamos el tiempo promedio
average_time = statistics.mean(process_times)
std_dev = statistics.pstdev(process_times)

print(f"Tiempo promedio: {average_time}")
print(f"Desviación estándar: {std_dev}")