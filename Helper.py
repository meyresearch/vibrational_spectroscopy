
import matplotlib.pyplot as plt
from scipy.stats import linregress
import scipy.constants as con
import numpy as np
import seaborn as sbn
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider

form = None

def populate_form():
    form_item_layout = Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )

    form_items = [
        Box([Label(value='Vibrations'),
             Textarea()], layout=form_item_layout),
        Box([Label(value='levels'),
             Textarea()], layout=form_item_layout)
    ]

    form = Box(form_items, layout=Layout(
        display='flex',
        flex_flow='column',
        border='solid 2px',
        align_items='stretch',
        width='50%'
    ))
    return form

def plot_birge_sponer(transition_wave_number, vib_quantum_number):
    r""" Plots a birge sponer plot
    Parameters:
    -----------
    transition_wave_number : string array
        Array conting transition wave numbers
    vib_quantum_number : string array
        corresponding vibrational quantum numbers

    Returns:
    --------
    matplotlib plot
    """
    G = []
    v = []
    for i in transition_wave_number.split(','):
        G.append(float(i.strip()))

    for V in vib_quantum_number.split(','):
        v.append(float(V.strip()))
    G.sort(reverse=True)
    print(G)
    G=np.array(G)
    v = np.array(v)
    # make sure arrays are sorted properly
    v= np.sort(v)

    plt.plot(v,G)
    sbn.despine()

def plot_extrapolated_birge_sponer(transition_wave_number, vib_quantum_number, shaded = True):
    r""" Plots a birge sponer plot
    Parameters:
    -----------
    transition_wave_number : string array
        Array conting transition wave numbers
    vib_quantum_number : string array
        corresponding vibrational quantum numbers

    Returns:
    --------
    matplotlib plot
    """
    G = []
    v = []
    for i in transition_wave_number.split(','):
        G.append(float(i.strip()))

    for V in vib_quantum_number.split(','):
        v.append(float(V.strip()))
    G.sort(reverse=True)
    print(G)
    G=np.array(G)
    v = np.array(v)
    # make sure arrays are sorted properly
    v= np.sort(v)

    fit = linregress(v, G)
    x_max = -fit[1]/fit[0]
    new_v = np.linspace(0,x_max, 20)
    new_G = fit[0]*new_v+fit[1]



    plt.plot(v,G)
    plt.plot(new_v,new_G,'--')
    sbn.despine()

def compute_area_under_graph(transition_wave_number, vib_quantum_number, shaded = True):
    r""" Plots a birge sponer plot
    Parameters:
    -----------
    transition_wave_number : string array
        Array conting transition wave numbers
    vib_quantum_number : string array
        corresponding vibrational quantum numbers

    Returns:
    --------
    matplotlib plot
    """
    G = []
    v = []
    for i in transition_wave_number.split(','):
        G.append(float(i.strip()))

    for V in vib_quantum_number.split(','):
        v.append(float(V.strip()))
    G.sort(reverse=True)
    print(G)
    G=np.array(G)
    v = np.array(v)
    # make sure arrays are sorted properly
    v= np.sort(v)

    fit = linregress(v, G)
    x_max = -fit[1]/fit[0]
    new_v = np.linspace(0,x_max, 20)
    new_G = fit[0]*new_v+fit[1]

    a = 0.5*x_max*max(new_G)
    Area = r'Area = $\frac{1}{2}$*v*G = %.3f cm$^{-1}$' %(a)
    pos_x = 0.8*x_max
    pos_y = 0.8*max(new_G)



    plt.plot(v,G)
    plt.plot(new_v,new_G,'--', color = 'orange')
    plt.fill_between(new_v, new_G, alpha=0.2, color = 'orange')
    plt.xlim(0,x_max)
    plt.ylim(0,max(new_G))
    plt.text(pos_x,pos_y,Area, bbox=dict(edgecolor='black', alpha=0.5), fontsize=15)
    sbn.despine()
