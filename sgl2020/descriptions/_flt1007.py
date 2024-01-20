from sgl2020.descriptions._flight import FlightDescription, FlightSegment, Report

# 构造 Flight 1007
FLT1007 = FlightDescription(
    flight_number="1007",
    date="07-Jul-2020",
    doy="189/366",
    compensations=[],  # 未提及补偿动作
    survey_lines=[
        "Free-fly in Perth mini-survey at 800m",
        "Free-fly in Eastern Ontario & Renfrew at 400m",
    ],  # 巡查线描述
    issues=[],  # 未提及具体问题
)

# 该航班的段落数据
segments_data_1007 = [
    (47070.00, 48024.00, "1007.01", "Transit to Perth Mini-Survey Area"),
    (48024.00, 51880.00, "1007.02", "Free-Fly at 800m within Perth Mini-Survey Area"),
    (51880.00, 52050.00, "1007.03", "Descent/Transit to 400m Eastern Ontario Free-Fly"),
    (52050.00, 57330.00, "1007.04", "!!!HOLD-OUT TESTING DATA!!!"),
    (57330.00, 57770.00, "1007.05", "Transit to Renfrew Free-Fly"),
    (57770.00, 63010.00, "1007.06", "Free-Fly at 400m within Renfrew Area"),
    (63010.00, 63800.00, "1007.07", "Transit to base"),
]

for start_time, end_time, line_number, description in segments_data_1007:
    FLT1007.add_segment(FlightSegment(start_time, end_time, line_number, description))
