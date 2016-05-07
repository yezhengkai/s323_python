# most modify code from 
# web:https://docs.obspy.org/tutorial/code_snippets/travel_time.html
# code:https://docs.obspy.org/tutorial/code_snippets/travel_time_body_waves.py
# by kmo 

import numpy as np
import matplotlib.pyplot as plt
from obspy.taup import TauPyModel

# modify font size
plt.rcParams.update({'font.size': 18})


model = TauPyModel(model='iasp91')
phase_name_radius = model.model.radius_of_planet * 1.1

# ax_right is used for paths plotted on the right half.
fig, ax_right = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
ax_right.set_theta_zero_location('N')
ax_right.set_theta_direction(-1)
ax = ax_right

#arrivals = model.get_ray_paths(500, realdist, phase_list=[phase])
arrivals = model.get_ray_paths(500, 80, phase_list=['P','P410s' ,'P660s'])
arrivals.plot(plot_type='spherical',legend=True, label_arrivals=True,show=False, ax=ax)

# Annotate regions
ax_right.text(0, 0, 'Solid\ninner\ncore',
              horizontalalignment='center', verticalalignment='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
ocr = (model.model.radius_of_planet -
       (model.model.s_mod.v_mod.iocb_depth +
        model.model.s_mod.v_mod.cmb_depth) / 2)

ax_right.text(np.deg2rad(180), ocr, 'Fluid outer core',
              horizontalalignment='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
mr = model.model.radius_of_planet - model.model.s_mod.v_mod.cmb_depth / 2

ax_right.text(np.deg2rad(180), mr, 'Solid mantle',
              horizontalalignment='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
theta = np.linspace(0., 2.*np.pi, endpoint=True)

######### below by kmo, above is from origin code ##########

# model.model.s_mod.v_mod.get_discontinuity_depths()
# output
# array([    0. ,    20. ,    35. ,   210. ,   410. ,   660. ,  2889. ,
#        5153.9,  6371. ])
# reference Taup plot 
# 2889-51539 gray
# 410-660 gray
# 35-210 gray

#inter-core outer-core boundary
iocb=(model.model.radius_of_planet - model.model.s_mod.v_mod.iocb_depth)
#iocb=(model.model.radius_of_planet - model.model.iocb_depth)

# core-mantle boundary 
cmb=(model.model.radius_of_planet - model.model.s_mod.v_mod.cmb_depth )
#cmb=(model.model.radius_of_planet - model.model.cmb_depth )

# moho
moho=(model.model.radius_of_planet - model.model.s_mod.v_mod.moho_depth)

# not sure which discontinuity
notsure=(model.model.radius_of_planet - 210)

# not sure which discontinuity
notsure_2=(model.model.radius_of_planet - 410)

# not sure which discontinuity
notsure_3=(model.model.radius_of_planet - 660)

ax_right.fill_between(theta,moho, color="lightgray")
ax_right.fill_between(theta,notsure, color="white")
ax_right.fill_between(theta,notsure_2, color="lightgray")
ax_right.fill_between(theta,notsure_3, color="white")
ax_right.fill_between(theta,cmb, color="lightgray")
ax_right.fill_between(theta,iocb, color="white")
plt.show()
