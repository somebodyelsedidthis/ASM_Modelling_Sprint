import numpy as np

class Solver:
    def __init__(self, global_stiffness_matrix, forces, boundary_conditions):
        self.K  = np.asarray(global_stiffness_matrix, dtype=float)
        self.forces =  np.asarray(forces, dtype=float)
        self.boundary_conditions = np.asarray(boundary_conditions, dtype=float)

    def displacement(self):
        prescribed_dofs = self.boundary_conditions[:, 0].astype(int)
        prescribed_values = self.boundary_conditions[:, 1]

        all_dofs = np.arange(len(self.forces))
        free_dofs = np.setdiff1d(all_dofs, prescribed_dofs)

        K_ff = self.K[np.ix_(free_dofs, free_dofs)]
        K_fp = self.K[np.ix_(free_dofs, prescribed_dofs)]

        F_f= self.forces[free_dofs]
        F_red = F_f -K_fp @ prescribed_values

        free_u = np.linalg.solve(K_ff, F_red)

        # Displacement vector finalize
        displacements = np.zeros(len(self.forces))
        displacements[free_dofs] = free_u
        displacements[prescribed_dofs] = prescribed_values

        return displacements
    