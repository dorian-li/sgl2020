from sgl2020 import SGL2020

surv = SGL2020()
surv_d = (
    surv.line([1002.02])
    .source(["ins_pitch", "ins_roll", "ins_yaw"])
    .take(include_line=True, reset_index=True, cache=False)
)
print(surv_d)
