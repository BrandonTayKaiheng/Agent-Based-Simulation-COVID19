import time
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid    #Each cell can contain >1 objects
from mesa.datacollection import DataCollector

#Disease model based on SIR Compartmentalized model


class State:        
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

def Compile_S(model):
    s = 0
    for agent in model.schedule.agents:
        if agent.state == State.SUSCEPTIBLE:
            s += 1
    return s

def Compile_I(model):
    i = 0
    for agent in model.schedule.agents:
        if agent.state == State.INFECTED:
            i+=1
    return i

def Compile_R(model):
    r = 0
    for agent in model.schedule.agents:
        if agent.state == State.RECOVERED:
            r += 1
    return r

def Compile_D(model):
    s = Compile_S(model)
    i = Compile_I(model)
    r = Compile_R(model)
    return 50 - (s+i+r)

class disease_model(Model):

    def __init__(self, N=50, width=11, height=11, ptrans=0.7, death_rate=0.002,
                 recovery_days=21, recovery_sd=7):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.recovery_days = recovery_days
        self.recovery_sd = recovery_sd
        self.ptrans = ptrans
        self.death_rate = death_rate
        self.schedule = RandomActivation(self) #Activates all agents once per step
        self.running = True
        self.dead = []

        #Generation of Agents
        for i in range(self.num_agents):
            a = agent(i, self)
            self.schedule.add(a) #Adds an agent to a grid cell Start Point
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        #Infected agents: np.random.choice(sample array, p = associated probability array)
            infected = np.random.choice([0,1], p = [0.95, 0.05])
            if infected == 1:
                a.state = State.INFECTED  #Change agent state to infected
                a.recovery_time = self.get_recovery_time()
    

        #Collect data on the state of agent        
        self.datacollector = DataCollector(model_reporters = {'Infected': Compile_I,
                                                              'Susceptible': Compile_S,
                                                              'Recovered': Compile_R,
                                                              'Dead': Compile_D},
                                           agent_reporters = {'State':'state'})
                                           #,model_reporters = {'Disease Status': SIR })

    def get_recovery_time(self):
        return int(self.random.normalvariate(self.recovery_days, self.recovery_sd))
        #Normally distibuted recovery time. 14 days mild cases, 28 days severe cases

    def step(self):
        self.datacollector.collect(self)  #Collect data every step
        self.schedule.step()
        
class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = State.SUSCEPTIBLE      
        self.time_infected = 0
    

    def move(self): #Movement of agents: Define Moore Neighbourhood >> Choose pos >> Move
        possible_steps = self.model.grid.get_neighborhood(self.pos,
                                                           moore = True,
                                                           include_center = True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def status(self): #Check agent status, adjust the agent states
        if self.state == State.INFECTED:
            death = self.model.death_rate
            alive = np.random.choice([0,1], p = [death, 1-death])
            if alive == 0:   #Remove the dead agent from schedule 
                self.model.schedule.remove(self)
            t = self.model.schedule.time - self.time_infected #Runtime-Agentinfected time
            if t >= self.recovery_time:
                self.state = State.RECOVERED

    def contact(self): #Infect the close contacts in the same cell
        occupancy = self.model.grid.get_cell_list_contents([self.pos]) #List of occupants 
        if len(occupancy) > 1:
            for other in occupancy:
                if self.random.random() > self.model.ptrans:
                    continue
                if (self.state is State.INFECTED and other.state is State.SUSCEPTIBLE):
                    other.state = State.INFECTED
                    other.infection_time = self.model.schedule.time
                    other.recovery_time = self.model.get_recovery_time()

    def step(self):
        self.status()
        self.move()
        self.contact()


