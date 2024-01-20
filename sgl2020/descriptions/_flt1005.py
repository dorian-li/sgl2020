from ._flight import FlightDescription, FlightSegment, Report  # 构造 Flight 1005

FLT1005 = FlightDescription(
    flight_number="1005",
    date="02-Jul-2020",
    doy="184/366",
    compensations=[],  # 未提及补偿动作
    survey_lines=[
        "Perth mini-survey (within Eastern Ontario) flown at 800m, flight 2 of 2"
    ],  # 巡查线描述
    issues=[
        Report("Split into two flights due to weather (low altitude clouds)"),
    ],
)

# 该航班的段落数据
segments_data_1005 = [
    (45788.00, 48085.00, "1005.01", "Takeoff - Transit to Perth Mini-Survey Area"),
    (48085.00, 48666.66, "4011.00", "Perth Survey Line"),
    (48847.12, 49498.52, "4010.00", "Perth Survey Line"),
    (49659.65, 50241.60, "4009.00", "Perth Survey Line"),
    (50482.41, 51080.55, "4008.00", "Perth Survey Line"),
    (51260.85, 51848.30, "4007.00", "Perth Survey Line"),
    (51998.63, 52604.72, "4006.00", "!!!HOLD-OUT TESTING DATA!!!"),
    (52740.76, 53315.22, "4005.00", "!!!HOLD-OUT TESTING DATA!!!"),
    (53471.63, 54063.86, "4004.00", "Perth Survey Line"),
    (54232.63, 54811.78, "4003.00", "Perth Survey Line"),
    (55006.06, 55605.59, "4002.00", "Perth Survey Line"),
    (55605.59, 56710.00, "1005.02", "Transit to base"),
]

for start_time, end_time, line_number, description in segments_data_1005:
    FLT1005.add_segment(FlightSegment(start_time, end_time, line_number, description))
