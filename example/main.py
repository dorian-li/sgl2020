from sgl2020 import Sgl2020

surv_d = (
    Sgl2020()
    .line([1005.01])  # 默认所有航线，如果.line()设置了则获取指定航线
    .source(  # 要获取的源（列名），详见SGL2020.describe()
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
    .take()  # 可设置是否包含line列、重置dataframe的index、使用cache
)
print(surv_d)  # 返回的是pandas.Dataframe, shape (n_samples, n_sources)

Sgl2020.describe("1005")
