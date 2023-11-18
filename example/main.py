from sgl2020 import SGL2020

surv = SGL2020()
surv_d = (
    surv.line([1002.02]) # 默认所有航线，如果.line()设置了则获取指定航线
    .source(["ins_pitch", "ins_roll", "ins_yaw"]).take(  # 要获取的源（列名）
        include_line=True, reset_index=True
    )  # 可设置是否包含line列、重置dataframe的index、使用cache
)
print(surv_d)  # 返回的是pandas.Dataframe
