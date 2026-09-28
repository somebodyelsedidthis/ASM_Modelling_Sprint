import elements
import test_element
import numpy as np

def create_elements(element_info):
    '''
    Parameters
    ----------
    element_info : list[dict]

    Returns
    -------
    list[elements.Element]

    Description
    -----------
    Create a list of Element objects taking element information as as dictionary type inputs.
    Each dict contains:
        [REQ]
        node_i, node_j  : list of coordinates of each node
        E, A            : Young's modulus, cross-sectional area of the element
        [OPT]
        I               : second moment of intertia (defaults to 1.0 if not defined)
        rho             : density (defaults to 1.0 if not defined)
        element_type    : 'truss' or 'frame' (defaults to 'truss')
    '''
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

def main():
    pass