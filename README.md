# sgl2020

Data wrapper for SGL2020 aeromagnetic survey.

## Features

- Automatic dataset file download and caching.
- Support multiple ways to select line data, such as selecting all lines, all lines for specific flights, line range, etc.
- Provide flight and sensor descriptions to help understand the structure and content of the dataset.

## Install

```bash
# stable
pip install sgl2020
# nightly
pip install git+https://github.com/dorian-li/sgl2020.git
```

## Usage Cases

### Fetch Data

- Typical usage

  ```python
  from sgl2020 import Sgl2020

  surv_d = (
      Sgl2020()
      .line([1002.02, 1002.20])
      .source(
          [
              "ins_pitch",
              "ins_roll",
              "ins_yaw",
              "mag_1_c",
              "mag_5_uc",
              "flux_b_x",
              "flux_b_y",
              "flux_b_z",
          ]
      )
      .take()
  ) # Dict[line, DataFrame]
  ```

- Select lines

  ```python
  # The following usage can be combined with each other
  # Select all lines of all flight in dataset
  Sgl2020().line(["*.*"])
  # Select all lines in flight 1002
  Sgl2020().line(["1002.*"])
  # Select line 1002.02
  Sgl2020().line(["1002.02"])
  # Or use float
  Sgl2020().line([1002.02])
  # Select more lines
  Sgl2020().line([1002.02, 1002.20])
  # Select line range
  Sgl2020().line(["1002.01-1002.05"])
  ```

- The specific `line` and `source` can be found in `Sgl2020.describe()`

### Description

- Show all source infomation
  ```python
  Sgl2020.describe("sensor")
  ```
- Show infomation of flight `1002`
  ```python
  Sgl2020.describe("1002")
  # or use integer
  Sgl2020.describe(1002)
  ```
- Show all flight infomation
  ```python
  Sgl2020.describe("flight")
  ```

# Thanks

Sincerely thank the [MagNav.jl](https://github.com/MIT-AI-Accelerator/MagNav.jl) team for their publicly available resources.
