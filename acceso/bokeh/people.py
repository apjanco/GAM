import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import os
import sys
sys.path.append('/srv/GAM/archivo/')
from settings_secret import DATABASES
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.layouts import column
from bokeh.models import HoverTool, Slider, Dropdown, Select, TableColumn, DataTable, FactorRange, Toggle, Button, Div, RangeTool, ColumnDataSource
from bokeh.layouts import row
from bokeh.models.callbacks import CustomJS
from bokeh.client import push_session
from bokeh.models.widgets import TextInput, RangeSlider
try:
	conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], host=DATABASES['default']['HOST'], database=DATABASES['default']['NAME'])
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)

c = conn.cursor()


df = pd.read_sql(
		"""
		SELECT *
		FROM gam_app_caso
		""", con=conn)
#print(Persona[Persona['edad_en_al_momento'] == 21])
pd.set_option('display.max_rows', 20)
#print(Persona.dtypes)
#print(Persona[Persona['edad_en_el_momento'] != ''])
#print(Persona.columns)

'''`
for key,value in df.items():
	df[key] = list(value)
source = ColumnDataSource(data=df)
'''

df = df[df['fecha_desaparicion'] != '']
dates = np.array(df['fecha_desaparicion'], dtype=np.datetime64)
dates = np.unique(dates)
print(dates)
counts = []
for i in dates:
	counts.append(df[df['fecha_desaparicion'] == str(i)]['fecha_desaparicion'].count())


source = ColumnDataSource(data=dict(date=dates, close=counts))

p = figure(plot_height=300, plot_width=800, tools="", toolbar_location=None, x_axis_type="datetime", x_axis_location="above", background_fill_color="#efefef", x_range=(dates[150], dates[250]))

p.line('date', 'close', source=source)
p.yaxis.axis_label = "Number of people missing"
range_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="Stuff")
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=130, plot_width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool
#show(column(p))
curdoc().add_root(column(p, select))
