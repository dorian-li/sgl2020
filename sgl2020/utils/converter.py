from os import PathLike
from pathlib import Path

import h5py
import pandas as pd
from loguru import logger


def h5_to_df(file: PathLike):
    df = pd.DataFrame()
    with h5py.File(file, "r") as f:
        for component in list(f.keys()):
            if not f[component].shape:
                continue
            df[component] = f[component]
            if df[component].isnull().any():
                logger.warning(f"{Path(file).name}:{component} contains NaN(s)")
    return df
