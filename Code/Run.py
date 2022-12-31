from Model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_appearance(agent):

    if agent.state == State.INFECTED:
        appearance = {"Shape" : "circle", "Filled" : "true",
                     "Layer" : 0, "Color" : "red",
                     "r" : 0.3}
    elif agent.state == State.SUSCEPTIBLE:
        appearance = {"Shape" : "circle", "Filled" : "true",
                     "Layer" : 0, "Color" : "blue",
                     "r" : 0.3}
    else:
        appearance = {"Shape" : "circle", "Filled" : "true",
                     "Layer" : 0, "Color" : "green",
                     "r" : 0.3}
    return appearance

#10x10 grid, 500x500 pixels 
grid = CanvasGrid(agent_appearance, 11, 11, 500, 500)

#Chart
chart1 = ChartModule([{"Label": "Susceptible",
                      "Color": "Blue"},
                      {"Label": "Infected",
                      "Color": "Red"},
                      {"Label": "Recovered",
                       "Color": "Green"},
                      {"Label": "Dead",
                       "Color": "Black"}],
                    data_collector_name='datacollector')

#Server settings
server = ModularServer(disease_model, [grid, chart1], "COVID19 Spread")
server.port = 8521
server.launch()

