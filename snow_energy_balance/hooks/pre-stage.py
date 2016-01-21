import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import assign_parameters


file_list = ['rti_file',
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

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
