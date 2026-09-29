import nodes, elements, rotation, global_stiffness, solver, post_proc

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcl

def main(node_info: list[dict], element_info: list[dict]):

    # Create Node, Element objects #

    node_list = nodes.create_nodes(node_info)
    element_list = nodes.create_elements(element_info)
    connectivity_matrix = nodes.connectivity(element_list)
    forces = nodes.force_matrix(node_list)
    prescribed_displacements = nodes.prescribed_displacements(node_list)

    # Calculate angles #

    angles = rotation.rotation_angles(element_list, node_list)

    # Assemble local stiffness matrices #

    for elem in element_list:
        elem.stiffness_matrix(node_list)

    # Construct Global Stiffness Matrix #

    structure = global_stiffness.TrussStructure(
        elements=element_list,
        nodes=node_list,
        connectivity_matrix=connectivity_matrix,
        angles=angles
    )

    K_global = structure.assemble_global_stiffness_matrix()

    # Solve for global node displacements #

    fem_solver = solver.Solver(
        global_stiffness_matrix=K_global,
        forces=forces,
        prescribed_displacements=prescribed_displacements
    )

    displacements = fem_solver.displacement()

    # Post-processing #

    reactions = post_proc.reaction(K_global, displacements, forces)
    strains = post_proc.strain(
        element_list,
        node_list,
        connectivity_matrix,
        displacements,
        angles,
        structure
    )
    stresses = post_proc.stress(element_list, strains)

   ##################
   ##################
   ## Visalisation ##
   ##################
   ##################

    def visualise(node_coords, elements, displacements, stresses, scale_factor=10.0):
        '''
        Parameters
        ----------
        node_coords     : dict/array of original node coordinates
        elements        : List of tuples connecting nodes
        displacements   : dict/array of nodal displacements
        stresses        : List/array of stresses for each element
        scale_factor    : scale factor for emphasising displacements

        Return
        ------
        Visual display

        Description
        -----------
        Visualise truss structure deformation, and stress colourmapping
        '''

        fig, ax = plt.subplots(figsize=(12,7))

        disp = np.asarray(displacements, dtype=float).reshape(-1, 2)
        stresses = np.asarray(stresses, dtype=float).flatten()

        # Colour map
        cmap = plt.get_cmap('coolwarm')
        max_abs_stress = max(max(abs(np.array(stresses))), 1e-9)
        norm = mcl.Normalize(vmin=-max_abs_stress, vmax=max_abs_stress)
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        # Plot elements
        for i, (n1, n2) in enumerate(connectivity_matrix):
            x0, y0 = node_coords[n1]
            x1, y1 = node_coords[n2]

            def_x0, def_y0 = node_coords[n1] + disp[n1] * scale_factor
            def_x1, def_y1 = node_coords[n2] + disp[n2] * scale_factor

            ax.plot([x0, x1], [y0, y1], 'k--', alpha=0.3, linewidth=1.5, zorder=1)

            color = cmap(norm(stresses[i]))
            ax.plot([def_x0, def_x1], [def_y0, def_y1], color=color, linewidth=3, zorder=2)

        # Plot nodes
        for n_id, (x, y) in enumerate(node_coords):
            
            dx, dy = disp[n_id]

            ax.plot(x, y, 'ko', markersize=4, alpha=0.3, zorder=3)

            ax.plot(x + dx * scale_factor, y + dy * scale_factor, 'ko', markersize=6, zorder=4)

        ax.set_title(f"Truss Deformation and Stress Distribution (Scale Factor: {scale_factor}x)", fontsize=14)
        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.axis('equal')

        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('Element Stress', rotation=270, labelpad=15)

        plt.tight_layout()
        plt.show()

    # Return Results #
    
    print('Visualisation Generating')
    node_coords = np.vstack([node.coords for node in node_list])
    visualise(node_coords,element_list,displacements,stresses)
    

    return {
        'displacements' : displacements,
        'reactions' : reactions,
        'strains' : strains,
        'stresses' : stresses
    }