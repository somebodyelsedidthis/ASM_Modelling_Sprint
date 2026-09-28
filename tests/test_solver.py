import numpy as np
from solver import Solver

def test_solver():
    K = np.array([
        [10.0, -10.0, 0.0],
        [-10.0, 20.0, -10.0],
        [0.0, -10.0, 10.0]
    ])

    forces =  np.array([
        [0,0.0]
    ])

    boundary_conditions = np.array([
        [0, 0]
    ])

    solver = Solver(K, forces, boundary_conditions)
    displacements = solver.displacement()

    expected_displacements = np.array([
        0.0,
        1.0,
        2.0
    ])

    assert np.allclose(displacements, expected_displacements)

def test_solver_prescribed_displacement():
    K = np.array([
        [10.0, -10.0]
        [-10.0, 10.0]
    ])

    forces = np.array([
        0.0,
        0.0
    ])

    boundary_conditions = np.array([
        [0, 0.01]
        [1, 0.01]
    ])

    solver = Solver(K, forces, boundary_conditions)
    displacements = solver.displacement()

    expected_displacements = np.array([
        0.01,
        0.01
    ])

    assert np.allclose(displacements, expected_displacements)

    if __name__ == "__main__":
        test_solver()
        test_solver_prescribed_displacement()

        print("All passed")