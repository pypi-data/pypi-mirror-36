import wcxf
from wilson.parameters import p as default_parameters
import ckmutil.ckm
import ckmutil.diag
from wilson.util import smeftutil
import numpy as np
from collections import OrderedDict


def arrays2wcxf(C):
    """Convert a dictionary with Wilson coefficient names as keys and
    numbers or numpy arrays as values to a dictionary with a Wilson coefficient
    name followed by underscore and numeric indices as keys and numbers as
    values. This is needed for the output in WCxf format."""
    d = {}
    for k, v in C.items():
        if np.shape(v) == ():
            d[k] = v
        else:
            ind = np.indices(v.shape).reshape(v.ndim, v.size).T
            for i in ind:
                name = k + '_' + ''.join([str(int(j) + 1) for j in i])
                d[name] = v[tuple(i)]
    return d


def wcxf2arrays(d):
    """Convert a dictionary dictionary with a Wilson coefficient
    name followed by underscore and numeric indices as keys and numbers as
    values to a dictionary with Wilson coefficient names as keys and
    numbers or numpy arrays as values. This is needed for the parsing
    of input in WCxf format."""
    C = {}
    for k, v in d.items():
        name = k.split('_')[0]
        s = smeftutil.C_keys_shape[name]
        if s == 1:
            C[k] = v
        else:
            ind = k.split('_')[-1]
            if name not in C:
                C[name] = np.zeros(s, dtype=complex)
            C[name][tuple([int(i) - 1 for i in ind])] = v
    return C


def smeft_toarray(wc_name, wc_dict):
    """Construct a numpy array with Wilson coefficient values from a
    dictionary of label-value pairs corresponding to the non-redundant
    elements."""
    shape = smeftutil.C_keys_shape[wc_name]
    C = np.zeros(shape, dtype=complex)
    for k, v in wc_dict.items():
        if k.split('_')[0] != wc_name:
            continue
        indices = k.split('_')[-1]  # e.g. '1213'
        indices = tuple(int(s) - 1 for s in indices)  # e.g. (1, 2, 1, 3)
        C[indices] = v
    C = smeftutil.symmetrize({wc_name: C})[wc_name]
    return C


def smeft_fromarray(wc_name, C):
    wc_dict = OrderedDict()
    ind = np.indices(C.shape).reshape(C.ndim, C.size).T
    for i in ind:
        label = ''.join([str(j + 1) for j in i])
        wc_dict[wc_name + '_' + label] = C[tuple(i)]
    return wc_dict


def warsaw_to_warsawmass(C, parameters=None):
    """Translate from the Warsaw basis to the 'Warsaw mass' basis.

    Parameters used:
    - `Vus`, `Vub`, `Vcb`, `gamma`: elements of the unitary CKM matrix (defined
      as the mismatch between left-handed quark mass matrix diagonalization
      matrices).
    """
    p = default_parameters.copy()
    if parameters is not None:
        # if parameters are passed in, overwrite the default values
        p.update(parameters)
    # start out with a 1:1 copy
    C_out = C.copy()
    # rotate left-handed up-type quark fields in uL-uR operator WCs
    C_rotate_u = ['uphi', 'uG', 'uW', 'uB']
    for name in C_rotate_u:
        _array = smeft_toarray(name, C)
        V = ckmutil.ckm.ckm_tree(p["Vus"], p["Vub"], p["Vcb"], p["gamma"])
        UuL = V.conj().T
        _array = UuL.conj().T @ _array
        _dict = smeft_fromarray(name, _array)
        C_out.update(_dict)
    # diagonalize dimension-5 Weinberg operator
    _array = smeft_toarray('llphiphi', C)
    _array = np.diag(ckmutil.diag.msvd(_array)[1])
    _dict = smeft_fromarray('llphiphi', _array)
    C_out.update(_dict)
    return C_out


def warsaw_to_warsaw_up(C, parameters=None):
    """Translate from the Warsaw basis to the 'Warsaw mass' basis.

    Parameters used:
    - `Vus`, `Vub`, `Vcb`, `gamma`: elements of the unitary CKM matrix (defined
      as the mismatch between left-handed quark mass matrix diagonalization
      matrices).
    """
    C_in = wcxf2arrays(C)
    C_in = smeftutil.symmetrize(C_in)
    C_in = smeftutil.scale_dict(C_in)
    p = default_parameters.copy()
    if parameters is not None:
        # if parameters are passed in, overwrite the default values
        p.update(parameters)
    Uu = Ud = Ul = Ue = np.eye(3)
    V = ckmutil.ckm.ckm_tree(p["Vus"], p["Vub"], p["Vcb"], p["gamma"])
    Uq = V.conj().T
    C_out = smeftutil.flavor_rotation(C_in, Uq, Uu, Ud, Ul, Ue)
    C_out = smeftutil.unscale_dict(C_out)
    C_out = arrays2wcxf(C_out)
    warsawup = wcxf.Basis['SMEFT', 'Warsaw up']
    allkeys = set(warsawup.all_wcs)  # to speed up lookup
    return {k: v for k, v in C_out.items() if k in allkeys}


def warsaw_up_to_warsaw(C, parameters=None):
    """Translate from the 'Warsaw up' basis to the Warsaw basis.

    Parameters used:
    - `Vus`, `Vub`, `Vcb`, `gamma`: elements of the unitary CKM matrix (defined
      as the mismatch between left-handed quark mass matrix diagonalization
      matrices).
    """
    C_in = wcxf2arrays(C)
    C_in = smeftutil.symmetrize(C_in)
    C_in = smeftutil.scale_dict(C_in)
    p = default_parameters.copy()
    if parameters is not None:
        # if parameters are passed in, overwrite the default values
        p.update(parameters)
    Uu = Ud = Ul = Ue = np.eye(3)
    V = ckmutil.ckm.ckm_tree(p["Vus"], p["Vub"], p["Vcb"], p["gamma"])
    Uq = V
    C_out = smeftutil.flavor_rotation(C_in, Uq, Uu, Ud, Ul, Ue)
    C_out = smeftutil.unscale_dict(C_out)
    C_out = arrays2wcxf(C_out)
    warsaw = wcxf.Basis['SMEFT', 'Warsaw']
    all_wcs = set(warsaw.all_wcs)  # to speed up lookup
    return {k: v for k, v in C_out.items() if k in all_wcs}
