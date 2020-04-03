from covidanalytics import etl as ce
from covidanalytics import analytics as ca
from covidanalytics import plots as cp
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components
from jinja2 import Template
import datetime

template = Template(
    '''<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" type="text/css" href="../css/stylesheet.css" media="screen"/>
                <title> {{ title }} </title>
                <style>
                </style>                
                {{ resources_cc }}
                {{ script_cc }}
                {{ resources_pc }}
                {{ script_pc }}
                {{ resources_tc }}
                {{ script_tc }}
            </head>
            <body class="body">
                <div class="grid-container">
                    <div class="grid-infog">
                        <img src="../images/{{ png }}" height={{ iheight }} width={{ iwidth }} class="gpx" />
                        <p><u>{{ hdr }}</u></p>
                        <p>{{ cases }}</p>
                        <p>{{rate}}</p>                        
                        <p>{{ deaths }}</p>
                    </div>           
                    <div class="embed-wrapper">
                        {{ div_cc }}
                    </div>            
                    <div class="embed-wrapper">
                        {{ div_tc }}
                    </div>
                    <div class="embed-wrapper">
                        {{ div_pc }}
                    </div>
                </div>
                <div class="footer">
                    <p>Data sourced from <a href="https://github.com/CSSEGISandData">Johns Hopkins</a>.</p>
                    <p>Last updated {{ update }}.</p>
                </div>

             </body>
        </html>
        ''')


def gen_covid_html(param_dict):
    filenames = ce.dates_to_filenames(param_dict['start_date'], param_dict['end_date'])
    recs = []
    for f in filenames:
        try:
            f_path = param_dict['reports_path'] + f
            covid = ce.covid_csv_to_df(f_path)
            if 'state' in param_dict.keys():
                daily = ce.covid_province_state(covid, param_dict['state'])
            if 'country' in param_dict.keys():
                daily = ce.covid_country_region(covid, param_dict['country'])
            if 'query' in param_dict.keys():
                daily = ce.covid_query(covid, param_dict['query'])
            recs.append(daily)
        except:
            print(f)
    covid_ts = ca.covid_dict_to_timeseries_df(recs, param_dict['start_date'], param_dict['end_date'])
    cc = cp.plot_total_cases(covid_ts, param_dict['title'], show_plot=False)
    pc = cp.plot_percent_change(covid_ts, param_dict['title'], show_plot=False)
    tc = cp.plot_total_change(covid_ts, param_dict['title'], show_plot=False)

    # bokeh html embed components
    script_cc, div_cc = components(cc)
    resources_cc = CDN.render()
    script_pc, div_pc = components(pc)
    resources_pc = CDN.render()
    script_tc, div_tc = components(tc)
    resources_tc = CDN.render()
    cases = "{:,}".format(int(covid_ts['confirmed'].max())) + " cases."
    deaths = "{:,}".format(int(covid_ts['deaths'].max())) + " deaths."
    if covid_ts.shape[0] >= 14:
        rate = "{:,}".format(int(covid_ts['7day_fit_m'][-1])) + " cases per day."
    else:
        rate = "{:,}".format(int(covid_ts['total_change'][-1])) + " cases per day."
    hdr = param_dict['title']
    png = param_dict['html']['img']
    if param_dict['html']['img_shape'] == 'tall':
        iheight = 240
        iwidth = 140
    elif param_dict['html']['img_shape'] == 'wide':
        iheight = 200
        iwidth = 275
    elif param_dict['html']['img_shape'] == 'square':
        iheight = 200
        iwidth = 200

    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # render everything together
    html = template.render(title=param_dict['title'],
                           resources_cc=resources_cc,
                           script_cc=script_cc,
                           div_cc=div_cc,
                           resources_pc=resources_pc,
                           script_pc=script_pc,
                           div_pc=div_pc,
                           resources_tc=resources_tc,
                           script_tc=script_tc,
                           div_tc=div_tc,
                           cases=cases,
                           deaths=deaths,
                           hdr=hdr,
                           png=png,
                           iheight=iheight,
                           iwidth=iwidth,
                           update=update,
                           rate=rate
                           )
    # write
    with open(param_dict['html']['dir'], 'w') as f:
        f.write(html)
