from analysis import tweets
from analysis import hashtags
from analysis import links
from pprint import pprint
import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('tjmrees', 'c1va4v3ghr')

# pprint(tweets.statistics())
# pprint(hashtags.statistics())
# pprint(links.statistics())

A = tweets.statistics()

pprint(A)

joi = (A["joi"] / A["all"]) * 100
ooi = (A["ooi"] / A["all"]) * 100
ext = (A["ext"] / A["all"]) * 100

# plot pie chart
labels = ["JOI", "OOI", "EXT"]
values = [joi, ooi, ext]

trace = go.Pie(labels=labels, values=values)
py.plot([trace])
