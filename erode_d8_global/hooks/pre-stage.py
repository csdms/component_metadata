import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import choices_map


file_list = ['pixel_file']


def uppercase_choice(choice):
    """Formats a string for consumption by TopoFlow.

    Parameters
    ----------
    choice : str
      A parameter choice from WMT.

    """
    import string
    return string.join(choice.split(), '_').upper()


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['stop_code'] = 1  # my choice
    env['stop_time'] = env['run_duration']  # years
    env['n_steps'] = 1  # WMT needs something here
    env['save_grid_dt'] = 1.0  # years
    env['save_pixels_dt'] = 1.0  # years
    env['dt'] = 1.0  # years

    # TopoFlow needs site_prefix and case_prefix.
    env['site_prefix'] = 'default'
    env['case_prefix'] = 'WMT'

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        file_list.remove('pixel_file')
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    env['BC_method'] = uppercase_choice(env['BC_method'])
    env['make_z0_method'] = uppercase_choice(env['make_z0_method'])
    env['noise_method'] = uppercase_choice(env['noise_method'])

    env['A_units'] = 'm^2'
    env['LINK_FLATS'] = choices_map[env['LINK_FLATS']]
    env['FILL_PITS_IN_Z0'] = choices_map[env['FILL_PITS_IN_Z0']]
    env['LR_PERIODIC'] = choices_map[env['LR_PERIODIC']]
    env['TB_PERIODIC'] = choices_map[env['TB_PERIODIC']]

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
