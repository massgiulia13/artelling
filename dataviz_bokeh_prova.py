#IMPORTANTE: si dovrebbe pulire il file json o csv con le birthplaces e gli autori, farci una df carina, ed UNIRLA alla df su periods e collections
#SOLO DOPO SI PUO' FARE QUESTA PRIMA DATAVIZ. 

import csv
from collections import defaultdict
import numpy as np
final_data = {} # final data


with open("IL NUOVO CSV") as csvfile: #è il csv creato dalla query corretta, ma manca birthplace
    periodLabel = []
    birthplace_label = []  #faccio 2 liste di valori presi dalle nostre query
    #ci serve tutto questo per correlare i birthplace degli autori con i periodi delle collezioni!
    rows = csv.reader(csvfile, delimiter=',')
    next(rows) # skip the header
    for row in rows:
        if row[1] not in nameHistorian:
            periodLabel.append(row[1]) # create the list of unique periods
        if row[2] not in nameColl :
            birthplace_label.append(row[2]) # create the list of unique birthplaces
            
    print(periodLabel)
    print(birthplace_label)  #fai le colonne, x e y con i periodi e le birthplace
    birthplace_label.sort()
    period_birthplace_zeros_matrix = np.array(np.zeros(( len(periodLabel), len(birthplace_label) ))) # rows, columns
    
    for i, period in enumerate(periodLabel): # loop over periods and their index position  
        for j, birthplace_label in enumerate(birthplace_label):
            with open(r"IL NUOVO CSV") as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                for row in rows:
                    if row[2] == birthplace_label and row[1] == periodLabel:
                        period_birthplace_zeros_matrix[j][i] = int(period_birthplace_zeros_matrix[j][i])+1
    
    periods_years_zeros_matrix
    
# put everything together
final_data["periodLabel"] = data_periods
for i, birthplace_label in enumerate(birthplace_label):
    data[birthplace_label] = list(period_birthplace_zeros_matrix[i])
print(final_data)

from bokeh.io import output_file, show
from bokeh.plotting import figure
import random

output_file("period_birthplaces_correlation.html")

number_of_colors = 10 # pick random colors for the years
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

p = figure(x_range=data_periods, plot_height=650, title="Periods counting by year",
           toolbar_location=None, tools="hover", tooltips="$name: @$name")

p.vbar_stack(years, x='periods', width=0.8, color=color, source=data,
             legend_label=years)

p.y_range.start = 0
p.x_range.range_padding = 0.2
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "vertical"
p.xaxis.major_label_orientation = "vertical"
show(p)

#questa funzione dovrebbe creare un barplot con x = periodi e y = birthplace degli autori di collezioni su tali periodi. però dobbiamo creare altri dataset, crearne uno unendo le due query
