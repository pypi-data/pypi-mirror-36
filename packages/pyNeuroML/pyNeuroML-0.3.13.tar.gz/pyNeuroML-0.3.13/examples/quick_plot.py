'''
    Example showing use of pynml.generate_plot()
'''
from pyneuroml import pynml
import math
import random
from matplotlib import pyplot as plt

######## Some example data

ts = [t*0.01 for t in range(20000)]

siny = [math.sin(t/10) for t in ts]
cosey = [ math.exp(t/-80)*math.cos(t/5) for t in ts]


########  Generate a plot for this quickly with generate_plot

ax = pynml.generate_plot([ts,ts],                        # Add 2 sets of x values
                         [siny,cosey],                   # Add 2 sets of y values
                         "Some traces",                  # Title
                         xaxis = 'Time (ms)',            # x axis legend
                         yaxis = 'Arbitrary units...',   # y axis legend
                         linewidths = [2,3],             # Thicknesses of each trace
                         show_plot_already=False,        # Show or wait for plt.show()?
                         font_size = 10,                 # Font
                         bottom_left_spines_only = True, # Box or just x & y axes
                         save_figure_to='quick.png')     # Save figure


########   Add another trace
                 
ts_ = [t*0.1 for t in range(2000)]
randy = [ random.random() for t in ts_]
ax.plot(ts_,randy,'.') # Won't be included in saved PNG!


########   Show complete plot

plt.show()

