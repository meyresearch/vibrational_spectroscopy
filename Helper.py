
import matplotlib.pyplot as plt
from scipy.stats import linregress
import scipy.constants as con
import numpy as np
import seaborn as sbn
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
sbn.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

form = None

def _extract_data(transition_wave_number, vib_quantum_number):
    r""" Plots a birge sponer plot
    Parameters:
    -----------
    transition_wave_number : string array
        Array conting transition wave numbers
    vib_quantum_number : string array
        corresponding vibrational quantum numbers
    """
    G = []
    v = []
    for i in transition_wave_number.split(','):
        G.append(float(i.strip()))

    for V in vib_quantum_number.split(','):
        v.append(float(V.strip()))
    G.sort(reverse=True)
    G=np.array(G)
    v = np.array(v)
    # make sure arrays are sorted properly
    v = np.sort(v)
    return v,G

def _fit(v,G):
    fit = linregress(v, G)
    x_max = -fit[1]/fit[0]
    new_v = np.linspace(0,x_max, 20)
    new_G = fit[0]*new_v+fit[1]
    return new_v, new_G, x_max

def data_input():
    form_item_layout = Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )

    form_items = [
        Box([Label(value='Vibrational Transition wave numbers G'),
             Textarea()], layout=form_item_layout),
        Box([Label(value='vibrational quantum numbers v+0.5'),
             Textarea()], layout=form_item_layout)
    ]

    form = Box(form_items, layout=Layout(
        display='flex',
        flex_flow='column',
        border='solid 2px',
        align_items='stretch',
        width='60%'
    ))
    return form

def plot_birge_sponer(form = None, transition_wave_number=None, vib_quantum_number=None):
    if transition_wave_number is None or vib_quantum_number is None:
        if form is None:
            print('Please populate form')
        else:
            transition_wave_number = form.children[0].children[1].value
            vib_quantum_number = form.children[1].children[1].value
    v,G = _extract_data(transition_wave_number, vib_quantum_number)

    plt.plot(v,G, marker='o')
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\tilde{\nu}\,[cm^{-1}]$')
    sbn.despine()

def plot_extrapolated_birge_sponer(form = None, transition_wave_number=None, vib_quantum_number=None, shaded = True):
    if transition_wave_number is None or vib_quantum_number is None:
        if form is None:
            print('Please populate form')
        else:
            transition_wave_number = form.children[0].children[1].value
            vib_quantum_number = form.children[1].children[1].value
    v,G = _extract_data(transition_wave_number, vib_quantum_number)

    new_v, new_G, x_max = _fit(v,G)

    plt.plot(v,G, marker='o')
    plt.plot(new_v,new_G,'--')
    plt.xlim(0,x_max)
    plt.ylim(0,max(new_G))
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\tilde{\nu}\,[cm^{-1}]$')
    sbn.despine()

def compute_area_under_graph(form = None, transition_wave_number=None, vib_quantum_number=None, shaded = True):
    if transition_wave_number is None or vib_quantum_number is None:
        if form is None:
            print('Please populate form')
        else:
            transition_wave_number = form.children[0].children[1].value
            vib_quantum_number = form.children[1].children[1].value
    v,G = _extract_data(transition_wave_number, vib_quantum_number)

    new_v, new_G, x_max = _fit(v,G)

    a = 0.5*x_max*max(new_G)
    Area = r'Area = $\frac{1}{2}$vG = %.2f cm$^{-1}$' %(a)
    pos_x = 0.8*x_max
    pos_y = 0.8*max(new_G)

    plt.plot(v,G, marker='o')
    plt.plot(new_v,new_G,'--', color = 'orange')
    plt.fill_between(new_v, new_G, alpha=0.2, color = 'orange')
    plt.xlim(0,x_max)
    plt.ylim(0,max(new_G))
    plt.text(pos_x,pos_y,Area, bbox=dict(edgecolor='black', alpha=0.5), fontsize=15)
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\tilde{\nu}\,[cm^{-1}]$')
    sbn.despine()

def compute_disosication_energy(form = None, transition_wave_number=None, vib_quantum_number=None, ):

    if transition_wave_number is None or vib_quantum_number is None:
        if form is None:
            print('Please populate form')
        else:
            transition_wave_number = form.children[0].children[1].value
            vib_quantum_number = form.children[1].children[1].value
    v,G = _extract_data(transition_wave_number, vib_quantum_number)

    new_v, new_G, x_max = _fit(v,G)
    a = 0.5*x_max*max(new_G)
    energy = (con.c*(a)*con.h*con.Avogadro*100)/1000
    print("The dissociation energy is: %.2f kJ/mol" % energy)
    #return energy

