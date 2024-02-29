import numpy as np
import matplotlib.pyplot as plt
import panel as pn
pn.extension('plotly')
import plotly.graph_objs as go

def plot_sine(amp):
    xx = np.linspace(-3.5, 3.5, 100)
    yy = np.linspace(-3.5, 3.5, 100)
    x, y = np.meshgrid(xx, yy)
    z = np.exp(-(x-1)**2-y**2)-(x**3+y**4-x/5)*np.exp(-(x**2+y**2))

    surface = go.Surface(z=z)
    layout = go.Layout(
        title='Plotly 3D Plot',
        autosize=False,
        width=500,
        height=500,
        margin=dict(t=50, b=50, r=50, l=50)
    )
    fig = dict(data=[surface], layout=layout)

    plotly_pane = pn.pane.Plotly(fig)
    return plotly_pane

# Panel Stuff
# pn.extension(sizing_mode="stretch_width")
# month = pn.widgets.IntSlider(start=1, end=12, name='Month')

# def plot_sine(n:int):
#     x=np.linspace(0,1,50)
#     y=n*np.sin(x)
#     fig, ax = plt.subplots()
#     plt.plot(x,y)
#     return fig
    
amp = pn.widgets.IntSlider(start=1, end=12, name='dummy_var')

pn.Column(
        "# Panel Script",
        amp, 
        pn.bind(plot_sine, amp),
        ).servable(target='myplot');
