import os
import shutil


def execute(env):
    env['n_steps'] = int(round(float(env['run_duration']) / float(env['dt'])))

    env['P'] = env['case_prefix'] + '_rain_rates.txt'
    env['slope_grid_file'] = env['site_prefix'] + '_slope.bin'
    env['aspect_grid_file'] = env['site_prefix'] + '_aspect.bin'

    # XXX: Binary files don't want to transfer?
    files_dir = '/data/web/htdocs/wmt/api/topoflow/db/components/meteorology/files'
    shutil.copy(os.path.join(files_dir, 'Treynor_aspect.bin'), os.curdir)
    shutil.copy(os.path.join(files_dir, 'Treynor_slope.bin'), os.curdir)

    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])
    env['pixel_file'] = env['case_prefix'] + '_outlets.txt'
