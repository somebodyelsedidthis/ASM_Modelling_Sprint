import numpy as np

class Node:
    def __init__(self,
                 x: float,
                 y: float,
                 D_x: float | None = None,
                 D_y: float | None = None,
                 F_x: float = 0.0,
                 F_y: float = 0.0):
        self.x = x
        self.y = y
        self.D_x = D_x
        self.D_y = D_y
        self.F_x = F_x
        self.F_y = F_y

    @property
    def coords(self) -> np.ndarray:
        return np.array([self.x, self.y])

    @property
    def forces(self) -> np.ndarray:
        return np.array([self.F_x, self.F_y])

    @property
    def displacements(self) -> np.ndarray:
        return np.array([self.D_x, self.D_y])

def create_nodes(node_info):
    '''
    Parameters
    ----------
    node_info : list[dict]

    Returns
    -------
    node_list : list[Node]

    Description
    -----------
    Create a list of Node objects taking node information as dictionary type inputs
    Each dict contains:
        [REQ]
        x, y        : x, y coordinates in global axes
        [OPT]
        F_x, F_y    : Forces in global x, y axes
        C_x, C_y    : boolean for whether the node is constrained in the x or y axis
    '''
    req_keys = {'x', 'y'}
    opt_keys = {'F_x', 'F_y', 'D_x', 'D_y'}

    node_list = []

    for i, spec in enumerate(node_info):
        missing = req_keys - spec.keys()
        if missing:
            raise ValueError(f'Element spec {i} is missing required keys: {missing}')
    
        unexpected = spec.keys() - (req_keys | opt_keys)
        if unexpected:
            raise ValueError(f'Element spec {i} has unexpected keys: {unexpected}')

        node = Node(
                    x=spec['x'],
                    y=spec['y'],
                    **{k: spec[k] for k in opt_keys if k in spec}
                )

        node_list.append(node)

    return node_list

def create_elements(element_info):
    '''
    Parameters
    ----------
    element_info : list[dict]

    Returns
    -------
    element_list : list[elements.Element]

    Description
    -----------
    Create a list of Element objects taking element information as as dictionary type inputs.
    Each dict contains:
        [REQ]
        node_i, node_j  : Node indices [integer]
        E, A            : Young's modulus, cross-sectional area of the element
        [OPT]
        I               : second moment of intertia (defaults to 1.0 if not defined)
        rho             : density (defaults to 1.0 if not defined)
        element_type    : 'truss' or 'frame' (defaults to 'truss')
    '''
    import elements
    
    req_keys = {'node_i', 'node_j', 'E', 'A'}
    opt_keys = {'I', 'rho', 'element_type'}

    element_list = []

    for i, spec in enumerate(element_info):
        missing = req_keys - spec.keys()

        if missing:
            raise ValueError(f'Element spec {i} is missing required keys: {missing}')

        unexpected = spec.keys() - (req_keys | opt_keys)
        if unexpected:
            raise ValueError(f'Element spec {i} has unexpected keys: {unexpected}')

        el = elements.Element(
            node_i=spec['node_i'],
            node_j=spec['node_j'],
            E=spec['E'],
            A=spec['A'],
            **{k: spec[k] for k in opt_keys if k in spec}
        )

        element_list.append(el)

    return element_list

def connectivity(element_list):
    '''
    Parameters
    ----------
    element_list : list[elements.Element]

    Returns
    -------
    connectivity_matrix : numpy.ndarray

    Description
    -----------
    Create the connectivity matrix
    '''
    connectivity_matrix = np.array([[elem.node_i, elem.node_j] for elem in element_list])

    return connectivity_matrix

def force_matrix(node_list):
    '''
    Parameters
    ----------
    node_list : list[Node]

    Returns
    -------
    F : np.ndarray

    Description
    -----------
    Creates a 2N x 1 array of all the external forces on each node
    '''
    return np.array([node.forces for node in node_list]).reshape(-1,1)

def prescribed_displacements(node_list):

    prescribed_dofs = []
    prescribed_values = []

    for i, node in enumerate(node_list):

        # x DOF
        if node.D_x is not None:
            prescribed_dofs.append(2 * i)
            prescribed_values.append(node.D_x)

        # y DOF
        if node.D_y is not None:
            prescribed_dofs.append(2 * i + 1)
            prescribed_values.append(node.D_y)

    return np.column_stack([
        prescribed_dofs,
        prescribed_values
    ])
