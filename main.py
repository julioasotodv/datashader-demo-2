import os

import panel as pn
import numpy as np
import pandas as pd
import hvplot.pandas
import holoviews as hv
from bokeh.io import curdoc
from matplotlib.cm import YlGnBu_r
import geoviews as gv
import cartopy
import datashader
import colorcet as cc

hv.extension("bokeh")

# Data:
datos_airbnb = pd.read_parquet(os.path.join("datos_airbnb", "airbnb_listings.parquet"), 
                           engine="fastparquet"
                          )

# Charts:

tiles_carto_oscuras = gv.tile_sources.CartoDark

scatter_airbnb = datos_airbnb.hvplot(kind="scatter",
                                     x="long_mercator",
                                     y="lat_mercator",
                                     c="precio diario",
                                     size=5,
                                     clabel="$/día",
                                     alpha=0.3,
                                     cmap=YlGnBu_r,
                                     colorbar=True,
                                     logz=True
                                    )

from holoviews.operation.datashader import rasterize, shade, datashade

scatter_rasterizado_matplotlib = rasterize(scatter_airbnb, 
                                           aggregator=datashader.reductions.mean("precio diario"),
                                           x_sampling=10,
                                           y_sampling=10
                                           )

scatter_rasterizado_matplotlib.opts(colorbar=True,
                                    clabel="$/día",
                                    cmap=YlGnBu_r,
                                    tools=["hover"],
                                    logz=True,
                                    colorbar_opts={"bar_line_width": 0.0},
                                    title="Paleta matplotlib"
                                   )


scatter_rasterizado_colorcet = rasterize(scatter_airbnb, 
                                         aggregator=datashader.reductions.mean("precio diario"),
                                         x_sampling=10,
                                         y_sampling=10
                                         )

scatter_rasterizado_colorcet.opts(colorbar=True,
                                  clabel="$/día",
                                  cmap=cc.bgy,     # Paleta de colorcet
                                  tools=["hover"],
                                  logz=True,
                                  colorbar_opts={"bar_line_width": 0.0,
                                                 "major_tick_line_color": "white"},
                                  title="Paleta colorcet"
                                 )


# Y volvemos a pintar junto con el mapa. Vamos
# a pintarlos uno encima del otro, para ver mejor las diferencias:

tiles_carto_oscuras = gv.tile_sources.CartoDark

antes = (tiles_carto_oscuras * scatter_rasterizado_matplotlib.opts(width=700, height=500))
despues = (tiles_carto_oscuras * scatter_rasterizado_colorcet.opts(width=700, height=500))

doc = hv.renderer("bokeh").server_doc((antes + despues).cols(2))

curdoc().title = "Ejemplo Datashader 2"

