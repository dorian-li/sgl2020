from ._flight import FlightDescription, FlightSegment, Report

# 构造 Flight 1003
FLT1003 = FlightDescription(
    flight_number="1003",
    date="29-Jun-2020",
    doy="181/366",
    compensations=[],  # 未提及补偿动作
    survey_lines=["Eastern Ontario & Renfrew free-fly at 400m & 800m"],  # 巡查线描述
    issues=[
        Report(
            "Mag 2 periodically dropped signal at ~180 degree headings during pitch/roll maneuvers",
            affected_lines=["1003.01"],
        ),
    ],
)

# 该航班的段落数据
segments_data_1003 = [
    (49820.00, 50713.00, "1003.01", "Takeoff - Eastern Ontario Free-Fly"),
    (50713.00, 54497.00, "1003.02", "Eastern Ontario Free-Fly 400m"),
    (54497.00, 54639.00, "1003.03", "Climb to 800m"),
    (54639.00, 59475.00, "1003.04", "Eastern Ontario Free-Fly 800m"),
    (59475.00, 59926.00, "1003.05", "Transit at 800m"),
    (59926.00, 60105.00, "1003.06", "Descend to 400m"),
    (60105.00, 60243.00, "1003.07", "Transit to Renfrew Free-Fly"),
    (60243.00, 64586.00, "1003.08", "Renfrew Free-Fly 400m"),
    (64586.00, 64763.00, "1003.09", "Climb to 800m"),
    (64763.00, 69252.00, "1003.10", "!!!HOLD-OUT TESTING DATA!!!"),
    (69252.00, 70311.00, "1003.11", "Transit to base"),
]

for start_time, end_time, line_number, description in segments_data_1003:
    FLT1003.add_segment(FlightSegment(start_time, end_time, line_number, description))
