import pandas as pd
import pooch
from deinterf import TollesLawsonCompensator
from loguru import logger

from .data_resource import Resource
from .utils.converter import h5_to_df


class SGL2020:
    def __init__(self):
        self._resource = Resource

    def _load_data(self):
        if not self.cache:
            self.remove_cache()

        if self._check_legacy_exists():
            self.data = self._load_legacy_data()
            self._set_all_line()
            return
        self.data = self._reload_data()
        self._cache_data()
        self._set_all_line()

    def _set_all_line(self):
        if not hasattr(self, "_line"):
            self._line = self.data["line"].drop_duplicates().to_list()

    @property
    def cache_src(self):
        return pooch.os_cache("sgl2020") / "sgl2020.pkl"

    def remove_cache(self):
        self.cache_src.unlink(missing_ok=True)

    def _cache_data(self):
        self.data.to_pickle(self.cache_src)

    def _load_legacy_data(self) -> pd.DataFrame:
        return pd.read_pickle(self.cache_src)

    def _check_legacy_exists(self):
        return self.cache_src.exists()

    def _load_raw(self):
        logger.info("loading raw...")
        flight_ds = pd.DataFrame()
        for d_file in self._resource.registry_files:
            file = self._resource.fetch(d_file)
            flight_d = h5_to_df(file)
            flight_ds = pd.concat([flight_ds, flight_d])
        flight_ds.reset_index(drop=True, inplace=True)
        return flight_ds

    def _add_tl_corr(self, data):
        logger.info("adding tl corr...")
        grouped = data.groupby("line")

        for op_sensor in [3, 4, 5]:
            compor = TollesLawsonCompensator()
            cali_d = grouped.get_group(1002.02)
            compor.fit(
                cali_d["flux_d_x"],
                cali_d["flux_d_y"],
                cali_d["flux_d_z"],
                cali_d[f"mag_{op_sensor}_uc"],
            )
            for line, line_d in grouped:
                comped, _ = compor.apply(
                    line_d["flux_d_x"],
                    line_d["flux_d_y"],
                    line_d["flux_d_z"],
                    line_d[f"mag_{op_sensor}_uc"],
                )
                data.loc[line_d.index, f"mag_{op_sensor}_tl_corr"] = comped
        return data

    def _reload_data(self):
        logger.info("start loading data...")
        data = self._load_raw()
        # data = self._add_tl_feat(data)
        # data = self._add_tl_coef(data)
        data = self._add_tl_corr(data)
        # data = self._add_igrf(data)
        # data = self._add_fom_bpf(data)
        logger.info("done")
        return data

    def line(self, line: float | list[float]):
        if isinstance(line, float):
            line = [line]
        self._line = line
        return self

    def source(self, source: str | list[str]):
        if isinstance(source, str):
            source = [source]
        self._source = source
        return self

    def take(self, include_line=False, reset_index=False, cache=True):
        self.cache = cache
        self._load_data()

        if include_line:
            self._source.append("line")
        taken = self.data[self.data["line"].isin(self._line)][self._source]
        if reset_index:
            taken.reset_index(drop=True, inplace=True)
        return taken
