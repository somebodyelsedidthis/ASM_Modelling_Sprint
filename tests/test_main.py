import pytest
import numpy as np
import main, elements, nodes, rotation, global_stiffness, solver, post_proc

##############
# Test: main #
##############

def test_main_truss_analysis():
    node_info = [
        {'x':0.0,'y':0.0, 'D_x': 0.0, 'D_y': 0.0},
        {'x':2.0,'y':0.0},
        {'x':1.0,'y':1.0, 'F_x': 0.0, 'F_y': -1500.0}
    ]

    E = 200e9
    A = 0.001

    element_info = [
        {'node_i':0,'node_j':1,'E': E,'A': A},
        {'node_i':1,'node_j':2,'E': E,'A': A},
        {'node_i':2,'node_j':1,'E': E,'A': A},
    ]

    results = main.main(node_info, element_info)

# Check for outputs #

    assert 'displacements' in results
    assert 'reactions' in results
    assert 'strains' in results
    assert 'stresses' in results

    displacements = results['displacements']
    reactions = results['reactions']
    stresses = results['stresses']

# Check boundary conditions are respected #

    assert np.isclose(displacements[0], 0.0)
    assert np.isclose(displacements[1], 0.0)
    assert np.isclose(displacements[2], 0.0)
    assert np.isclose(displacements[3], 0.0)

# Check displacement #

    assert np.isclose(displacements[4], 0.0, atol=1e-8)
    assert displacements[5] < 0.0

# Check equilibrium of forces #
    vertical_reactions = reactions[1] + reactions[3]
    assert np.isclose(vertical_reactions, 1500.0)

# Check stress #

    assert np.isclose(stresses[1], stresses[2])
    assert stresses[1] < 0.0

##############################
# Test: main [invalid input] #
##############################

invalid_node_info = [{'x': 0.0}]
element_info = [{'node_i': 0, 'node_j': 1, 'E': 200e9, 'A': 0.001}]

with pytest.raises(ValueError):
    main.main(invalid_node_info, element_info)