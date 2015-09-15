import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file


file_list = ['rti_file',
             'aspect_grid_file',
             'slope_grid_file',
             'P',
             'pixel_file']


def execute(env):
    env['n_steps'] = int(round(float(env['run_duration']) / float(env['dt'])))
    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])

    # Determine TopoFlow site_prefix from RTI filename.
    env['site_prefix'] = os.path.splitext(env['rti_file'])[0]

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'None':
        file_list.remove('pixel_file')
        env['pixel_file'] = '_outlets.txt'

    env['P'] = env['case_prefix'] + '_rain_rates.txt'

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
