import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file


def execute(env):
    env['n_steps'] = int(round(float(env['run_duration']) / float(env['dt'])))

    # Determine TopoFlow site_prefix from RTI filename.
    env['site_prefix'] = os.path.splitext(env['rti_file'])[0]

    env['P'] = env['case_prefix'] + '_rain_rates.txt'
    env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    ### Special temporary fix!
    # env['slope_grid_file'] = env['site_prefix'] + '_slope.bin'
    # env['aspect_grid_file'] = env['site_prefix'] + '_aspect.bin'
    env['slope_grid_file'] = 'Treynor_slope.bin'
    env['aspect_grid_file'] = 'Treynor_aspect.bin'

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    prepend_to_path('WMT_INPUT_FILE_PATH',
                    os.path.join(site['db'], 'components', 'topoflow', 'files'))
    file_list = ['rti_file', 'P', 'aspect_grid_file',
                 'slope_grid_file', 'pixel_file']
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)

    ### Special temporary fix!
    env['slope_grid_file'] = env['site_prefix'] + '_slope.bin'
    env['aspect_grid_file'] = env['site_prefix'] + '_aspect.bin'
    shutil.move('Treynor_aspect.bin', env['aspect_grid_file'])
    shutil.move('Treynor_slope.bin', env['slope_grid_file'])

    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])
