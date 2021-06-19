import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
data = pd.read_excel('产品销售数据表.xlsx')
x = list(data['销售日期'])
y = list(data['销售额(万元)'])
chart = Bar()
chart.add_xaxis(x)
chart.add_yaxis('销售额(万元)', y)
chart.set_global_opts(title_opts = opts.TitleOpts(title = '产品销售额对比图'), datazoom_opts = opts.DataZoomOpts())
chart.render('动态柱形图.html')

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
data = pd.read_excel('产品销售数据表.xlsx')
x = list(data['销售日期'])
y = list(data['销售额(万元)'])
chart = Bar(init_opts = opts.InitOpts(theme = ThemeType.DARK))
chart.add_xaxis(x)
chart.add_yaxis('销售额(万元)', y)
chart.set_global_opts(title_opts = opts.TitleOpts(title = '产品销售额对比图'), datazoom_opts = opts.DataZoomOpts())
chart.render('动态柱形图.html')

