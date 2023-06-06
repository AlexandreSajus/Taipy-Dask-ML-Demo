import dask
import dask_ml.datasets


def generate_data(centers: int):
    """
    Generates synthetic data for clustering.

    Args:
        - centers (int): number of clusters to generate

    Returns:
        - X (dask.array): array of shape (n_samples, n_features)
    """
    X, _ = dask_ml.datasets.make_blobs(
        n_samples=1000000, chunks=100000, random_state=0, centers=centers
    )
    return X.persist()


def fit(X: dask.array, n_clusters: int):
    """
    Fit a k-means clustering model.

    Args:
        - X (dask.array): array of shape (n_samples, n_features)
        - n_clusters (int): number of clusters to fit

    Returns:
        - km (dask_ml.cluster.KMeans): k-means clustering model
    """
    km = dask_ml.cluster.KMeans(n_clusters=n_clusters)
    km.fit(X)
    return km
