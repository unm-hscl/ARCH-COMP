'''
Created by Hyst v1.5
Hybrid Automaton in Hylaa
Converted from file: 
Command Line arguments: -gen drivetrain "-theta 2 -init_scale 0.3 -reverse_errors -switch_time 0.20001" -passes sub_constants "" simplify -p -o hylaa_drivetrain_theta2_initscale0_3.py -tool hylaa ""
'''

import numpy as np
from hylaa.hybrid_automaton import LinearHybridAutomaton, LinearConstraint
from hylaa.engine import HylaaSettings
from hylaa.engine import HylaaEngine
from hylaa.containers import PlotSettings, SimulationSettings

def define_ha():
    '''make the hybrid automaton and return it'''

    ha = LinearHybridAutomaton()
    ha.variables = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "t"]


    negAngle = ha.new_mode('negAngle')
    a_matrix = np.array([ \
        [0, 0, 0, 0, 0, 0, 0.0833333333333333, 0, -1, 0, 0, 0], \
        [13828.8888888889, -26.6666666666667, 60, 60, 0, 0, -5, -60, 0, 0, 0, 0], \
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, -714.285714285714, -0.04, 0, 0, 0, 714.285714285714, 0, 0], \
        [-2777.77777777778, 3.33333333333333, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], \
        [100, 0, 0, 0, 0, 0, 0, -1000, -0.01, 1000, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
        [0, 0, 0, 0, 1000, 0, 0, 1000, 0, -2000, -0.01, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        ], dtype=float)
    c_vector = np.array([0, 716.666666666667, 0, 5, 0, 0, -83.3333333333333, 0, 3, 0, 0, 1], dtype=float)
    negAngle.set_dynamics(a_matrix, c_vector)
    negAngle.inv_list.append(LinearConstraint([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -0.03)) # x1 <= -0.03

    deadzone = ha.new_mode('deadzone')
    a_matrix = np.array([ \
        [0, 0, 0, 0, 0, 0, 0.0833333333333333, 0, -1, 0, 0, 0], \
        [-60, -26.6666666666667, 60, 60, 0, 0, -5, -60, 0, 0, 0, 0], \
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, -714.285714285714, -0.04, 0, 0, 0, 714.285714285714, 0, 0], \
        [0, 3.33333333333333, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, -1000, -0.01, 1000, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
        [0, 0, 0, 0, 1000, 0, 0, 1000, 0, -2000, -0.01, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        ], dtype=float)
    c_vector = np.array([0, 300, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1], dtype=float)
    deadzone.set_dynamics(a_matrix, c_vector)
    deadzone.inv_list.append(LinearConstraint([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0.03)) # -0.03 <= x1
    deadzone.inv_list.append(LinearConstraint([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0.03)) # x1 <= 0.03

    posAngle = ha.new_mode('posAngle')
    a_matrix = np.array([ \
        [0, 0, 0, 0, 0, 0, 0.0833333333333333, 0, -1, 0, 0, 0], \
        [13828.8888888889, -26.6666666666667, 60, 60, 0, 0, -5, -60, 0, 0, 0, 0], \
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, -714.285714285714, -0.04, 0, 0, 0, 714.285714285714, 0, 0], \
        [-2777.77777777778, 3.33333333333333, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], \
        [100, 0, 0, 0, 0, 0, 0, -1000, -0.01, 1000, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
        [0, 0, 0, 0, 1000, 0, 0, 1000, 0, -2000, -0.01, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        ], dtype=float)
    c_vector = np.array([0, -116.666666666667, 0, 5, 0, 0, 83.3333333333333, 0, -3, 0, 0, 1], dtype=float)
    posAngle.set_dynamics(a_matrix, c_vector)
    posAngle.inv_list.append(LinearConstraint([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -0.03)) # 0.03 <= x1

    negAngleInit = ha.new_mode('negAngleInit')
    a_matrix = np.array([ \
        [0, 0, 0, 0, 0, 0, 0.0833333333333333, 0, -1, 0, 0, 0], \
        [13828.8888888889, -26.6666666666667, 60, 60, 0, 0, -5, -60, 0, 0, 0, 0], \
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, -714.285714285714, -0.04, 0, 0, 0, 714.285714285714, 0, 0], \
        [-2777.77777777778, 3.33333333333333, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], \
        [100, 0, 0, 0, 0, 0, 0, -1000, -0.01, 1000, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
        [0, 0, 0, 0, 1000, 0, 0, 1000, 0, -2000, -0.01, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        ], dtype=float)
    c_vector = np.array([0, 116.666666666667, 0, -5, 0, 0, -83.3333333333333, 0, 3, 0, 0, 1], dtype=float)
    negAngleInit.set_dynamics(a_matrix, c_vector)
    negAngleInit.inv_list.append(LinearConstraint([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 0.20001)) # t <= 0.20001

    error = ha.new_mode('error')
    a_matrix = np.array([ \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        ], dtype=float)
    c_vector = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    error.set_dynamics(a_matrix, c_vector)

    _error = ha.new_mode('_error')
    _error.is_error = True

    trans = ha.new_transition(negAngleInit, negAngle)
    trans.condition_list.append(LinearConstraint([-0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -1], -0.20001)) # t >= 0.20001

    trans = ha.new_transition(negAngle, deadzone)
    trans.condition_list.append(LinearConstraint([-1, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0], 0.03)) # x1 >= -0.03

    trans = ha.new_transition(deadzone, posAngle)
    trans.condition_list.append(LinearConstraint([-1, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0], -0.03)) # x1 >= 0.03

    trans = ha.new_transition(deadzone, error)
    trans.condition_list.append(LinearConstraint([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -0.03)) # x1 <= -0.03

    trans = ha.new_transition(posAngle, error)
    trans.condition_list.append(LinearConstraint([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0.03)) # x1 <= 0.03

    trans = ha.new_transition(error, _error)

    return ha

def define_init_states(ha):
    '''returns a list of (mode, list(LinearConstraint])'''
    # Variable ordering: [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, t]
    rv = []
    
    constraints = []
    constraints.append(LinearConstraint([1, 0, 0, -0.0005600000000000003, 0, 0, 0, 0, 0, 0, 0, 0], -0.06000000000000001)) # 1.0 * x1 + 0.04488 = 0.0005600000000000003 * x4 - 0.01512000000000001
    constraints.append(LinearConstraint([-1, -0, -0, 0.0005600000000000003, -0, -0, -0, -0, -0, -0, -0, -0], 0.06000000000000001)) # 1.0 * x1 + 0.04488 = 0.0005600000000000003 * x4 - 0.01512000000000001
    constraints.append(LinearConstraint([0, 1, 0, -0.4669999999999999, 0, 0, 0, 0, 0, 0, 0, 0], -25.009999999999998)) # 1.0 * x2 + 12.401 = 0.4669999999999999 * x4 - 12.609
    constraints.append(LinearConstraint([-0, -1, -0, 0.4669999999999999, -0, -0, -0, -0, -0, -0, -0, -0], 25.009999999999998)) # 1.0 * x2 + 12.401 = 0.4669999999999999 * x4 - 12.609
    constraints.append(LinearConstraint([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0)) # x3 = 0.0
    constraints.append(LinearConstraint([-0, -0, -1, -0, -0, -0, -0, -0, -0, -0, -0, -0], -0)) # x3 = 0.0
    constraints.append(LinearConstraint([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 0)) # x5 = 0.0
    constraints.append(LinearConstraint([-0, -0, -0, -0, -1, -0, -0, -0, -0, -0, -0, -0], -0)) # x5 = 0.0
    constraints.append(LinearConstraint([0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0], 0)) # 1.0 * x6 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([-0, -0, -0, 1, -0, -1, -0, -0, -0, -0, -0, -0], -0)) # 1.0 * x6 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([0, 0, 0, -12, 0, 0, 1, 0, 0, 0, 0, 0], 0)) # 1.0 * x7 - 324.0 = 12.0 * x4 - 324.0
    constraints.append(LinearConstraint([-0, -0, -0, 12, -0, -0, -1, -0, -0, -0, -0, -0], -0)) # 1.0 * x7 - 324.0 = 12.0 * x4 - 324.0
    constraints.append(LinearConstraint([0, 0, 0, -0.000060000000000000015, 0, 0, 0, 1, 0, 0, 0, 0], -0.0031200000000000004)) # 1.0 * x8 + 0.0015 = 0.000060000000000000015 * x4 - 0.0016200000000000003
    constraints.append(LinearConstraint([-0, -0, -0, 0.000060000000000000015, -0, -0, -0, -1, -0, -0, -0, -0], 0.0031200000000000004)) # 1.0 * x8 + 0.0015 = 0.000060000000000000015 * x4 - 0.0016200000000000003
    constraints.append(LinearConstraint([0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0], 0)) # 1.0 * x9 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([-0, -0, -0, 1, -0, -0, -0, -0, -1, -0, -0, -0], -0)) # 1.0 * x9 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([0, 0, 0, -0.000060000000000000015, 0, 0, 0, 0, 0, 1, 0, 0], -0.0031200000000000004)) # 1.0 * x10 + 0.0015 = 0.000060000000000000015 * x4 - 0.0016200000000000003
    constraints.append(LinearConstraint([-0, -0, -0, 0.000060000000000000015, -0, -0, -0, -0, -0, -1, -0, -0], 0.0031200000000000004)) # 1.0 * x10 + 0.0015 = 0.000060000000000000015 * x4 - 0.0016200000000000003
    constraints.append(LinearConstraint([0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0], 0)) # 1.0 * x11 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([-0, -0, -0, 1, -0, -0, -0, -0, -0, -0, -1, -0], -0)) # 1.0 * x11 - 27.0 = 1.0 * x4 - 27.0
    constraints.append(LinearConstraint([0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0], -27)) # 27.0 <= x4
    constraints.append(LinearConstraint([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 33)) # x4 <= 33.0
    constraints.append(LinearConstraint([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 0)) # t = 0.0
    constraints.append(LinearConstraint([-0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -0, -1], -0)) # t = 0.0
    rv.append((ha.modes['negAngleInit'], constraints))
    
    return rv


def define_settings():
    'get the hylaa settings object'
    plot_settings = PlotSettings()
    plot_settings.plot_mode = PlotSettings.PLOT_NONE
    plot_settings.xdim = 0
    plot_settings.ydim = 2

    settings = HylaaSettings(step=5.0E-4, max_time=2.0, plot_settings=plot_settings)

    return settings

def run_hylaa(settings):
    'Runs hylaa with the given settings, returning the HylaaResult object.'
    ha = define_ha()
    init = define_init_states(ha)

    engine = HylaaEngine(ha, settings)
    engine.run(init)

    return engine.result

if __name__ == '__main__':
    run_hylaa(define_settings())
