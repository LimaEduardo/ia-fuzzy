import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

import time
import sys

distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')
velocidade = ctrl.Antecedent(np.arange(0, 101, 1), 'velocidade')
pressao = ctrl.Consequent(np.arange(0, 101, 1), 'pressao')

distancia.automf(5)
velocidade.automf(5)

pressao['muito_baixo'] = fuzz.trapmf(pressao.universe, [0, 0, 5, 10])
pressao['baixo'] = fuzz.trapmf(pressao.universe, [7.5, 15, 25, 32.5])
pressao['medio'] = fuzz.trapmf(pressao.universe, [28, 35, 68, 72])
pressao['alto'] = fuzz.trapmf(pressao.universe, [68, 75, 75, 77.5])
pressao['muito_alto'] = fuzz.trapmf(pressao.universe, [77.5, 80, 100, 100])

#Disatancias: 'muito perto' -> 'muito longe'
# Available options: 'poor'; 'mediocre'; 'average'; 'decent', or 'good'.
# distancia.view()
# velocidade.view()
pressao.view()

plt.show()


# velocidade          distancia         tempo
# good                  poor            0.036
# decent                mediocre        1.2
# average               average         3.6
# mediocre              decent          10.8
# poor                  good            360

rule1 = ctrl.Rule(distancia['poor'] & velocidade['good'], pressao['muito_alto'])
rule2 = ctrl.Rule(distancia['mediocre'] | velocidade['decent'], pressao['muito_alto'])
rule3 = ctrl.Rule(distancia['average'] | velocidade['average'], pressao['alto'])
rule4 = ctrl.Rule(distancia['decent'] | velocidade['mediocre'], pressao['baixo'])
rule5 = ctrl.Rule(distancia['good'] & velocidade['poor'], pressao['muito_baixo'])
rule6 = ctrl.Rule(distancia['good'] & velocidade['good'], pressao['medio'])
rule7 = ctrl.Rule(distancia['poor'] | velocidade['poor'], pressao['alto'])
# rule6 = ctrl.Rule(distancia['poor'] | velocidade['good'], pressao['muito_alto'])
# rule7 = ctrl.Rule(distancia['mediocre'] | velocidade['decent'], pressao['alto'])
# rule8 = ctrl.Rule(distancia['average'] | velocidade['average'], pressao['medio'])
# rule9 = ctrl.Rule(distancia['decent'] | velocidade['mediocre'], pressao['baixo'])
# rule10 = ctrl.Rule(distancia['good'] | velocidade['poor'], pressao['muito_baixo'])


pressao_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
quantidade_pressao = ctrl.ControlSystemSimulation(pressao_ctrl)

quantidade_pressao.input['distancia'] = int(sys.argv[1])
quantidade_pressao.input['velocidade'] = int(sys.argv[2])

# Crunch the numbers
quantidade_pressao.compute()

print(quantidade_pressao.output['pressao'])
pressao.view(sim=quantidade_pressao)
