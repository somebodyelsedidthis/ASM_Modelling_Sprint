import nodes, elements, rotation, global_stiffness, solver, post_proc

import numpy as np

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

    # Return Results #
    
    return {
        'displacements' : displacements,
        'reactions' : reactions,
        'strains' : strains,
        'stresses' : stresses
    }

def visualise():
    