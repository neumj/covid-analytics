from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool


def plot_total_cases(ts_df ,title='World' ,show_plot=True):
    src = ColumnDataSource(ts_df)
    src.data.keys()
    # title_str = '{}: COVID-19 Cases'.format(title)
    title_str = 'COVID-19 Cases'

    # Create a blank figure with labels
    p = figure(plot_width=425 ,
               plot_height=425,
               title=title_str,
               x_axis_label='Date',
               y_axis_label='Number',
               x_axis_type='datetime')

    # Add glyphs
    p.varea(source=src,
            x='index',
            y1='confirmed',
            y2='active',
            fill_color="aliceblue")
    p.line(source=src,
           x='index',
           y='confirmed',
           color='blue',
           legend_label='Confirmed Cases')
    p.line(source=src,
           x='index',
           y='active',
           color='cornflowerblue',
           legend_label='Active Cases')
    p.line(source=src,
           x='index',
           y='deaths',
           color='darkgray',
           legend_label='Deaths')
    p.circle(source=src,
             x='index',
             y='deaths',
             size=1,
             color='darkgray')
    p.circle(source=src,
             x='index',
             y='confirmed',
             size=1,
             color='blue')
    p.circle(source=src,
             x='index',
             y='active',
             size=1,
             color='cornflowerblue')

    p.legend.location = "top_left"

    hover = HoverTool(tooltips = [('Confirmed', '@confirmed'),
                                  ('Active', '@active'),
                                  ('Deaths', '@deaths')])

    # Add the hover tool to the graph
    p.add_tools(hover)

    if show_plot==True:
        # Set to output the plot in the notebook
        output_notebook()
        # Show the plot
        show(p)

    return p

def plot_percent_change(ts_df ,title='World' ,show_plot=True):
    src = ColumnDataSource(ts_df)
    src.data.keys()
    # title_str = '{}: Percent Change in Confirmed Cases'.format(title)
    title_str = 'Percent Change in Confirmed Cases'

    # Create a blank figure with labels
    p = figure(plot_width=425 ,plot_height=425,
               title=title_str,
               x_axis_label='Date',
               y_axis_label='Percent Change',
               x_axis_type='datetime')

    # Add glyphs
    p.circle(source=src,
             x='index',
             y='percent_change',
             size=2,
             color='blue')
    p.line(source=src,
           x='index',
           y='percent_change',
           color='blue')

    hover = HoverTool(tooltips = [('Percent Change: ', '@percent_change')])

    # Add the hover tool to the graph
    p.add_tools(hover)

    if show_plot==True:
        # Set to output the plot in the notebook
        output_notebook()
        # Show the plot
        show(p)

    return p

def plot_total_change(ts_df ,title='World' ,show_plot=True):
    src = ColumnDataSource(ts_df)
    src.data.keys()
    # title_str = '{}: Change in Confirmed Cases'.format(title)
    title_str = 'Change in Confirmed Cases'

    # Create a blank figure with labels
    p = figure(plot_width=425 ,plot_height=425,
               title=title_str,
               x_axis_label='Date',
               y_axis_label='Number of Cases',
               x_axis_type='datetime')

    p.vbar(source=src,
           x='index',
           top='total_change',
           width=0.5,
           color='blue')
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    if show_plot==True:
        # Set to output the plot in the notebook
        output_notebook()
        # Show the plot
        show(p)

    return p
