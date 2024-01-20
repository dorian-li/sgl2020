import re

import numpy as np
import pooch
from h5py import File, is_hdf5
from pandas import DataFrame, Series
from typing_extensions import Dict, List, Literal, Self, Union

from sgl2020.descriptions import FLIGHT_DESCRIPTIONS, SENSOR_DESCRIPTIONS


class DataWarehouse:
    def __init__(self) -> None:
        self.resource = pooch.create(
            path=pooch.os_cache("sgl2020"),
            base_url="doi:10.5281/zenodo.4271803/",
            registry={
                "Flt1002_train.h5": "md5:d42e6579719e31d17115c9b8ed3e4471",
                "Flt1003_train.h5": "md5:bc0e819bebb8bc9d4814cdbce0fb911a",
                "Flt1004_train.h5": "md5:a17c1678407c02f260d7250b4e6c3a15",
                "Flt1005_train.h5": "md5:0065e0a270db7f53544ba8df247e1c12",
                "Flt1006_train.h5": "md5:fb798e26d515673deae2e1b349b9e215",
                "Flt1007_train.h5": "md5:ad29d8bb5ab8a3c97ac02b8f83b41b01",
            },
        )
        self.file_handles: Dict[str, File] = {}

    def get_file_handle(self, flight: str) -> File:
        dataset_filename = f"Flt{flight}_train.h5"
        if flight not in self.file_handles:
            dataset_filepath = self.resource.fetch(dataset_filename, progressbar=True)
            if not is_hdf5(dataset_filepath):
                raise ValueError(
                    f"{dataset_filepath} is not a valid HDF5 file or does not exist."
                )
            self.file_handles[flight] = File(dataset_filepath, "r")
        return self.file_handles[flight]

    def close(self) -> None:
        for handle in self.file_handles.values():
            handle.close()


class Sgl2020:
    def __init__(self, reset_index=False) -> None:
        self.data_warehouse = DataWarehouse()
        self.lines_seleted: List[str] = None
        self.sources_requested: List[str] = None
        self.reset_index = reset_index
        # TODO: 处理空数据，如不存在的航线、数据集内没有对应数据等
        # self.without_empty_data = False
        # TODO: 排除取出数据的时间段，如航线说明带有“HOLD-OUT”字样的
        # self.without_holdout_period = False

    def __del__(self) -> None:
        self.data_warehouse.close()

    def line(self, selected: List[Union[float, str]]) -> Self:
        lines_seleted = self._parse_lines_selected(selected)
        # self._validate_lines(lines_seleted)
        self.lines_seleted = lines_seleted
        return self

    def source(self, sources: List[str]) -> Self:
        # self._validate_sources(sources)
        self.sources_requested = sources
        return self

    def take(self) -> Dict[str, DataFrame]:
        if self.lines_seleted is None or self.sources_requested is None:
            raise ValueError("Please specify lines and sources first.")

        data = {
            line_id: self._fetch_line_data(line_id) for line_id in self.lines_seleted
        }
        return data

    FltString = Literal["1002", "1003", "1004", "1005", "1006", "1007"]
    FltInt = Literal[1002, 1003, 1004, 1005, 1006, 1007]

    @staticmethod
    def describe(
        mode: Union[Literal["flight", "sensor"], FltString, FltInt] = "sensor"
    ) -> None:
        # validate
        if mode not in ["flight", "sensor"] and str(mode) not in FLIGHT_DESCRIPTIONS:
            raise ValueError(
                f"Invalid mode: {mode}, should be one of 'flight', 'sensor' or flight id."
            )

        if mode == "flight":
            print("Flight descriptions:")
            for flight_id in FLIGHT_DESCRIPTIONS:
                FLIGHT_DESCRIPTIONS[flight_id].describe()
        elif mode == "sensor":
            SENSOR_DESCRIPTIONS.describe()
        else:  # mode is flight id
            FLIGHT_DESCRIPTIONS[str(mode)].describe()

    def _parse_lines_selected(self, selected: List[Union[float, str]]) -> List[str]:
        # 支持“*.*”选择所有航线
        # 支持“1002.*”选择1002航班的所有航线，根据数据文件,可能有非1002开头的航线
        # 支持“1002.01”这样的航线号
        # 支持1002.01这样的航线号
        # 支持“1002.01-1002.02”这样的航线号
        pattern = r"^(\d{4}\.\d{2}|\d{4}\.\*|\d{4}\.\d{2}\-\d{4}\.\d{2}|\*\.\*)$"

        ret: List[str] = []
        for line in selected:
            if isinstance(line, float):
                line = f"{line:.2f}"
            if not re.match(pattern, line):
                raise ValueError(f"Invalid line: {line}")

            if line == "*.*":
                for flight in FLIGHT_DESCRIPTIONS:
                    ret.extend(self._expand_line(flight))
            elif "*" in line:
                # 1002.* => [1002.01, 1002.02, ...]
                ret.extend(self._expand_line(self._parse_flight_from_line(line)))
            elif "-" in line:
                ret.extend(self._expand_line_range(line))
            else:
                ret.append(line)
        return list(set(ret))

    def _expand_line(self, flight: str) -> List[str]:
        lines_expanded = [
            seg.line_number for seg in FLIGHT_DESCRIPTIONS[flight].segments
        ]
        lines_expanded = list(set(lines_expanded))
        return lines_expanded

    def _expand_line_range(self, line: str) -> List[str]:
        # 1002.02-1002.05 => [1002.02, 1002.03, 1002.04, 1002.05]
        start, end = line.split("-")
        start_flight = self._parse_flight_from_line(start)
        end_flight = self._parse_flight_from_line(end)

        if start_flight != end_flight:
            raise ValueError(f"Only support line range in the same flight: {line}")

        start_line = int(start.split(".")[1])
        end_line = int(end.split(".")[1])

        lines_expanded = [
            f"{start_flight}.{line:02d}" for line in range(start_line, end_line + 1)
        ]
        return lines_expanded

    def _parse_flight_from_line(self, line: str) -> str:
        def find_flight(line: str):
            for id, flight in FLIGHT_DESCRIPTIONS.items():
                if line in flight.lines:
                    return flight.flight_number

        flight = line.split(".")[0].strip()
        if flight not in FLIGHT_DESCRIPTIONS:
            flight = find_flight(line)
        return flight

    def _fetch_line_data(self, line_id: str) -> DataFrame:
        flight_id = self._parse_flight_from_line(line_id)
        file_handle = self.data_warehouse.get_file_handle(flight_id)
        return self._read_data(file_handle, line_id)

    def _read_data(self, file_handle: File, line_id: str) -> DataFrame:
        lines = [f"{line:.2f}" for line in file_handle["line"][:]]
        mask = np.array(lines) == line_id

        index = np.where(mask)[0] if not self.reset_index else None

        line_data = {
            source: Series(file_handle[f"/{source}"][:][mask], index=index)
            for source in self.sources_requested
        }

        return DataFrame(line_data)
