from bokeh.plotting import figure 
from bokeh.transform import cumsum
from bokeh.transform import cumsum
from bokeh.models import LabelSet, ColumnDataSource
from bokeh.palettes import Category20c
from bokeh.embed import components 
import math
from math import pi

def get_chart_component(record):
    graph1 = figure(title="Results",plot_width=300, plot_height=250, x_range=(-1.3, 1.3), y_range=(-4.5, 4.5) )  
    fields = ['Pass','Fail']
    percentages = [record.pass_percentage,record.fail_percentage]
                    # formula for converting percentage into radians  
    radians1 = [math.radians((percent / 100) * 360) for percent in percentages]  
        
    # Generating the start angle values  
    start_angle = [math.radians(0)]  
    prev = start_angle[0]  
    for k in radians1:  
        start_angle.append(k + prev)  
        prev = k + prev  
        
    # generating the end angle values  
    end_angle = start_angle[1:] + [math.radians(0)]  
        
    # initiate the center of the pie chart  
    x = 0  
    y = 0  
        
    # then, we will initiate the radius of the glyphs  
    radius = 1  
        
    # now, generate the color of the wedges  
    color1 = ["green","red"]  
        
    # now, we will plot the graph  
    for k in range(len(fields)):  
        graph1.wedge(x, y, radius,  
                    start_angle = start_angle[k],  
                    end_angle = end_angle[k],  
                    color = color1[k],  
                    legend_label = fields[k]+"-"+str(percentages[k])+"%") 
    graph1.legend.glyph_height = 10#some int
    graph1.legend.glyph_width = 10#some int
    graph1.axis.axis_label = None
    graph1.axis.visible = False
    graph1.grid.grid_line_color = None
    # graph1.legend.visible = False
    script, div = components(graph1)
    bokeh_chart = '%s%s' % (div, script)
    return bokeh_chart