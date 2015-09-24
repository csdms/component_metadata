import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file


file_list = ['rti_file',
             'code_file',
             'slope_file',
             'pixel_file']


def get_typeof_parameter(parameter_value):
    """Get the TopoFlow type of a parameter."""
    try:
        float(parameter_value)
    except ValueError:
        return 'string'
    else:
        return 'float'


def assign_parameter_type_and_value(env):
    """Assign the value of a TopoFlow input parameter.

    A subset of TopoFlow input parameters can take a scalar value, or,
    through an uploaded file, a time series, a grid, or a grid
    sequence. This function assigns the parameter a scalar value, or
    the name of a file, based on the user's selection in WMT.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    for key in env.copy().iterkeys():
        if key.endswith('_type'):
            key_root = str(key[:-5])
            if env[key] == 'Scalar':
                env[key_root] = env[key_root + '_scalar']
            else:
                env[key_root] = env[key_root + '_file']
                file_list.append(key_root)
            env['typeof_' + key_root] = get_typeof_parameter(env[key_root])


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['n_steps'] = int(round(float(env['run_duration']) / float(env['dt'])))
    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])

    # TopoFlow needs site_prefix and case_prefix.
    env['site_prefix'] = os.path.splitext(env['rti_file'])[0]
    env['case_prefix'] = 'scenario'

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        file_list.remove('pixel_file')
        env['pixel_file'] = '_outlets.txt'

    # Translate the roughness choice to TopoFlow flags.
    env['MANNING'] = env['roughness_option'].startswith('Manning') * 1
    env['LAW_OF_WALL'] = 1 - env['MANNING']

    env['nval_type'] = env['z0val_type'] = env['roughness_type']
    env['nval_scalar'] = env['z0val_scalar'] = env['roughness_scalar']
    env['nval_file'] = env['z0val_file'] = env['roughness_file']    

    assign_parameter_type_and_value(env)

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
