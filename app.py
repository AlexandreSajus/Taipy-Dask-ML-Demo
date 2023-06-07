import taipy as tp
from taipy.gui import Gui, notify
from taipy.config import Config

import dask
import dask_ml.datasets
import dask_ml.cluster
import pandas as pd
import matplotlib.pyplot as plt

from dask.distributed import Client

client = Client(processes=False, threads_per_worker=4, n_workers=1, memory_limit="2GB")

n_clusters = 3
data = dask_ml.datasets.make_blobs(
    n_samples=1000000, chunks=1000000, random_state=0, centers=n_clusters
)
X, _ = data
km = dask_ml.cluster.KMeans(n_clusters=n_clusters)
km.fit(X)
visual_data = pd.DataFrame(
    {"x": X[::1000, 0], "y": X[::1000, 1], "color": km.labels_[::1000]}
)

Config.load("config.toml")

scenario_object = Config.scenarios["scenario"]


def on_button(state):
    notify(state, "info", "Running K-Means")
    scenario = tp.create_scenario(scenario_object)
    scenario.centers.write(state.n_clusters)
    scenario.n_clusters.write(state.n_clusters)
    tp.submit(scenario)
    state.X = scenario.dataset.read()
    state.km = scenario.km.read()
    state.visual_data = pd.DataFrame(
        {
            "x": state.X[::1000, 0],
            "y": state.X[::1000, 1],
            "color": state.km.labels_[::1000],
        }
    )
    notify(state, "success", "Done! (Please Reload the Page))")


page = """
# Scaling K-Means with **Dask**{: .color-secondary} and **Taipy**{: .color-primary}

Number of clusters:

<|{n_clusters}|slider|min=1|max=10|>

<|Run K-Means|button|on_action=on_button|>

<|{visual_data}|chart|mode=markers|x=x|y=y|color=color|>
"""

tp.Core().run()
Gui(page).run()
