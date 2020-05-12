
__author__ = "Antonia Mey"
__email_ = "antonia.mey@ed.ac.uk"


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
    r'Liner regresion fit of data points extrapolating to cross x and y axis at 0.'

    # Fit data
    fit = linregress(v, G)
    # find maximum x
    x_max = -fit[1]/fit[0]

    # create new extrapolated data point array
    new_v = np.linspace(0,x_max, 20)
    new_G = fit[0]*new_v+fit[1]

    #return all relevant data points
    return new_v, new_G, x_max

def data_input():
    r'Widget to interact with for data'
    form_item_layout = Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )

    form_items = [
        Box([Label(value=r'Vibrational intervals  $\Delta$ G in cm$^{-1}$'),
             Textarea()], layout=form_item_layout),
        Box([Label(value='Vibrational quantum numbers v+1/2'),
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

    # Basic plot with labels
    plt.plot(v,G, marker='o')
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\Delta G(v+1/2)\,[cm^{-1}]$')
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

    # Basic plot with lables that also plots the fit
    plt.plot(v,G, marker='o')
    plt.plot(new_v,new_G,'--')
    plt.xlim(0,x_max)
    plt.ylim(0,max(new_G))
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\Delta G(v+1/2)\,[cm^{-1}]$')
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

    # Compute the area under the curve
    a = 0.5*x_max*max(new_G)
    Area = r'Area = $\frac{1}{2}$vG = %.2f cm$^{-1}$' %(a)
    pos_x = 0.8*x_max
    pos_y = 0.8*max(new_G)

    # Plot with shaded area and computed size of area
    plt.plot(v,G, marker='o')
    plt.plot(new_v,new_G,'--', color = 'orange')
    plt.fill_between(new_v, new_G, alpha=0.2, color = 'orange')
    plt.xlim(0,x_max)
    plt.ylim(0,max(new_G))
    plt.text(pos_x,pos_y,Area, bbox=dict(edgecolor='black', alpha=0.1), fontsize=15)
    plt.xlabel(r'v+$\frac{1}{2}$')
    plt.ylabel(r'$\Delta G(v+1/2)\,[cm^{-1}]$')
    sbn.despine()

def compute_dissociation_energy(form = None, transition_wave_number=None, vib_quantum_number=None, ):

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

