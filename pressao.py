import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

import time

distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')
velocidade = ctrl.Antecedent(np.arange(0, 101, 1), 'velocidade')
pressao = ctrl.Consequent(np.arange(0, 101, 1), 'pressao')

distancia.automf(5)
velocidade.automf(5)

pressao['muito_baixo'] = fuzz.trimf(pressao.universe, [0, 0, 25])
pressao['baixo'] = fuzz.trimf(pressao.universe, [15, 25, 50])
pressao['medio'] = fuzz.trimf(pressao.universe, [40, 50, 75])
pressao['alto'] = fuzz.trimf(pressao.universe, [65, 75, 100])
pressao['muito_alto'] = fuzz.trimf(pressao.universe, [90, 100, 100])

#Disatancias: 'muito perto' -> 'muito longe'
# Available options: 'poor'; 'mediocre'; 'average'; 'decent', or 'good'.
distancia.view()
velocidade.view()
pressao.view()

# plt.show()

rule1 = ctrl.Rule(distancia['poor'] & velocidade['good'], pressao['muito_alto'])
rule2 = ctrl.Rule(distancia['mediocre'] | velocidade['decent'], pressao['muito_alto'])
rule3 = ctrl.Rule(distancia['average'] | velocidade['average'], pressao['alto'])
rule4 = ctrl.Rule(distancia['decent'] | velocidade['mediocre'], pressao['medio'])
rule5 = ctrl.Rule(distancia['good'] & velocidade['poor'], pressao['muito_baixo'])
rule6 = ctrl.Rule(distancia['good'] & velocidade['good'], pressao['medio'])
rule7 = ctrl.Rule(distancia['poor'] & velocidade['poor'], pressao['alto'])
# rule6 = ctrl.Rule(distancia['poor'] | velocidade['good'], pressao['muito_alto'])
# rule7 = ctrl.Rule(distancia['mediocre'] | velocidade['decent'], pressao['alto'])
# rule8 = ctrl.Rule(distancia['average'] | velocidade['average'], pressao['medio'])
# rule9 = ctrl.Rule(distancia['decent'] | velocidade['mediocre'], pressao['baixo'])
# rule10 = ctrl.Rule(distancia['good'] | velocidade['poor'], pressao['muito_baixo'])


pressao_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
quantidade_pressao = ctrl.ControlSystemSimulation(pressao_ctrl)

quantidade_pressao.input['distancia'] = 100
quantidade_pressao.input['velocidade'] = 100

# Crunch the numbers
quantidade_pressao.compute()

print(quantidade_pressao.output['pressao'])
pressao.view(sim=quantidade_pressao)
