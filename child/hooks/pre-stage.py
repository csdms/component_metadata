
def execute(env):
    from math import ceil


    duration_in_years = ceil(float(env['run_duration']) / 365.)
    env['run_duration'] = str(int(duration_in_years))
