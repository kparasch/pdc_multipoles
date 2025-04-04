import numpy as np
import xtrack as xt
import itertools

def get_petra_iv(version, rms_dk1=None):
    line = xt.Line.from_json(f'line_thick_P4_H6BA_v{version}.json')
    #line.compensate_radiation_energy_loss()

    if rms_dk1 is not None:
        rng = np.random.default_rng(seed=1)
        for el in line.elements:
            if isinstance(el, xt.Quadrupole):
                el.k1 += el.k1*rng.normal(0, rms_dk1)

    pdc = line['pdcseptum']
    line.env.new('pdcseptum_mpoles', xt.Quadrupole, length=pdc.length, order=20)
    line.insert([line.env.place('pdcseptum_mpoles', at=0, from_='pdcseptum')])


    tt = line.get_table(attr=True)
    tt_bend = tt.rows[tt.element_type == 'Bend']
    tt_quad = tt.rows[tt.element_type == 'Quadrupole']
    tt_sext = tt.rows[tt.element_type == 'Sextupole']
    tt_oct = tt.rows[tt.element_type == 'Octupole']

    line.set(tt_oct, integrator='yoshida4', num_multipole_kicks=7)
    line.set(tt_sext, integrator='yoshida4', num_multipole_kicks=7)
    line.set(tt_bend, model='mat-kick-mat', integrator='teapot', num_multipole_kicks=1)
    line.set(tt_bend.rows['wgl.*'], model='drift-kick-drift-expanded',
             integrator='teapot', num_multipole_kicks=1)
    return line

def get_DA(line, dx=1, x_max=15, dy=0.3, y_max=4, delta=0, n_turns=2000):
    '''
    dx, xmax, dy, ymax in mm
    '''
    x_grid = np.arange(-x_max, x_max+0.1*dx, dx)*1e-3
    y_grid = np.arange(1e-6, y_max+0.1*dx, dy)*1e-3
    x_da, y_da = np.array([(ii[0], ii[1]) for ii in itertools.product(x_grid, y_grid)]).T

    line.configure_radiation(model='mean')
    twiss = line.twiss()
    line.configure_radiation(model='quantum')
    p_co = twiss.particle_on_co

    particles = line.build_particles(
        x=p_co.x[0] + x_da,
        px=p_co.px[0],
        y=p_co.y[0] + y_da,
        py=p_co.py[0],
        zeta=p_co.zeta[0],
        delta=p_co.delta[0] + delta
        )

    line.track(particles, num_turns=n_turns, time=True, with_progress=True)
    print(f'Tracking took: {line.time_last_track:.1f} s')
    particles.sort(by='particle_id', interleave_lost_particles=True)

    state_r = particles.state.reshape(len(x_grid), len(y_grid))
    # x_r = x_da.reshape(len(x_grid), len(y_grid))
    y_r = y_da.reshape(len(x_grid), len(y_grid))
    da = np.zeros(len(x_grid))
    for i in range(len(x_grid)):
        if state_r[i, 0] < 0:
            da[i] = y_r[i, 0]
            continue

        for j in range(len(y_grid)):
            if j+1 == len(y_grid) or state_r[i, j+1] < 0:
                da[i] = y_r[i,j]
                break

    da_area = np.sum(da*1e3)*dx
    print(f'Dynamic aperture area: {da_area:.1f} mm^2')
    return x_grid, da

def get_MA(line, dx=1, x_max=15, ddelta=0.005, delta_max=0.06, y=1e-6, n_turns=1000):
    '''
    dx, xmax, y in mm
    '''
    x_grid = np.arange(-x_max, x_max+0.1*dx, dx)*1e-3
    delta_grid = np.arange(1e-6, delta_max+0.1*dx, ddelta)
    x_da, delta_da = np.array([(ii[0], ii[1]) for ii in itertools.product(x_grid, delta_grid)]).T

    line.configure_radiation(model='mean')
    twiss = line.twiss()
    line.configure_radiation(model='quantum')
    p_co = twiss.particle_on_co

    particles = line.build_particles(
        x=p_co.x[0] + x_da,
        px=p_co.px[0],
        y=p_co.y[0] + y,
        py=p_co.py[0],
        zeta=p_co.zeta[0],
        delta=p_co.delta[0] + delta_da
        )

    line.track(particles, num_turns=n_turns, time=True, with_progress=True)
    print(f'Tracking took: {line.time_last_track:.1f} s')
    particles.sort(by='particle_id', interleave_lost_particles=True)

    state_r = particles.state.reshape(len(x_grid), len(delta_grid))
    # x_r = x_da.reshape(len(x_grid), len(y_grid))
    delta_r = delta_da.reshape(len(x_grid), len(delta_grid))
    ma = np.zeros(len(x_grid))
    for i in range(len(x_grid)):
        if state_r[i, 0] < 0:
            ma[i] = delta_r[i, 0]
            continue

        for j in range(len(delta_grid)):
            if j+1 == len(delta_grid) or state_r[i, j+1] < 0:
                ma[i] = delta_r[i,j]
                break

    ma_area = np.sum(ma)*dx
    print(f'Momentum aperture area: {ma_area:.3f} mm')
    return x_grid, ma