# Agent-Based-Simulation-COVID19
An Agent Based Simulation of the COVID19 infectivity using the classic SIR (Susceptible, Infected, Removed) epidemiological model in Python. 

## Directory guide
* The `Code` directory contains `Model.py` and `Run.py`
* `Model.py` contains the SIR model implementation using the `mesa` Python library. Contains class definitions for Model and Agents.  
* `Run.py` creates the data visualisation, and hosts the simulation GUI on a web server (See figure below)
* Run the `Run.py` file to start the simulation 

![image](https://user-images.githubusercontent.com/115394445/210131600-2b1aea95-a3b7-4d8a-8e1c-639c527ff36b.png)

## Model guide

### SIR Model
* The SIR model is a classic compartmentalised disease model described by 3 differential equations (See figure below)
* An agent can be any of the 3 possible states (Susceptible, Infected or Removed)
* The Infection rate (Beta) and the Recovery rate (Gamma) parameters used were based on real COVID 19 data in 2021 

![image](https://user-images.githubusercontent.com/115394445/210131799-68c2b01d-63ad-444a-87d9-a54a890ae60a.png)

### Agent Based Simulation
* Initially, 95% of agents generated are in Susceptible state, and 5% are Infected
* A grid is generated with the agents randomly distributed
* At each time-step, an agent will choose a random neighbouring cell in the grid adjacent to its current cell, based on Moore Neighbourhood, and move to it. 
* If an Infected agent and a Susceptible agent occupies the same cell, in Susceptible agent may be infected with the probablility based on the Infection rate

![image](https://user-images.githubusercontent.com/115394445/210132265-a4fb09e3-bb04-4a2a-880f-c26e0e61e811.png)
