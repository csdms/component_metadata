import os
import shutil
import numpy as np

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file, yaml_dump
from topoflow_utils.hook import assign_parameters


file_list = ['rti_file',
             'aspect_grid_file',
             'slope_grid_file',
             'pixel_file']


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
    env['case_prefix'] = 'WMT'

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        file_list.remove('pixel_file')
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    assign_parameters(env, file_list)

    # If P_ptype is Scalar, replicate the scalar value as a Time_Series.
    # This works around the issue described in https://trello.com/c/LaOMPpOa.
    if env['P_ptype'] == 'Scalar':
        env['P_ptype'] = 'Time_Series'
        env['P_dtype'] = 'string'
        file_name = env['case_prefix'] + '_rain_rates.txt'
        time_series = np.ones(env['n_steps']) * float(env['P'])
        np.savetxt(file_name, time_series, fmt='%8.3f')
        env['P'] = env['P_file'] = file_name

    # yaml_dump('_env.yaml', env)  # helpful for debugging

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
