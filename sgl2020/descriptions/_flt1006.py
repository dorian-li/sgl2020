from ._flight import FlightDescription, FlightSegment, Report

# 构造 Flight 1006
FLT1006 = FlightDescription(
    flight_number="1006",
    date="06-Jul-2020",
    doy="188/366",
    compensations=[
        "Compensation maneuvers in FOM at 10,000ft (3048m), 13,000ft (3962m), 17,000ft (5181m)",
        "Compensation maneuvers in Eastern Ontario at 400m",
    ],  # 补偿动作的描述
    survey_lines="",  # 未提及巡查线
    issues=[
        Report(
            "Mag 2 periodically dropped signal at ~180 degree headings during pitch/roll maneuvers",
            affected_lines=[
                "1006.02",
                "1006.03",
                "1006.04",
                "1006.06",
                "1006.07",
                "1006.08",
            ],
        ),
        Report(
            "Limited pilot comments written during flight due to challenging maneuvers"
        ),
    ],
)

# 该航班的段落数据
segments_data_1006 = [
    (46100.00, 47222.00, "1006.01", "Takeoff - Compensation area"),
    (47222.00, 48213.00, "1006.02", "!!!HOLD-OUT TESTING DATA!!!"),
    (48213.00, 49000.00, "1006.03", "Climb to 17,000ft"),
    (49000.00, 53286.00, "1006.04", "Compensation maneuvers at 17,000ft"),
    (53286.00, 53855.00, "1006.05", "Descent to 10,000ft"),
    (53855.00, 54510.00, "1006.06", "Compensation maneuvers at 10,000ft"),
    (54510.00, 55770.00, "1006.07", "Transit/Descent to Eastern Ontario"),
    (
        55770.00,
        56609.00,
        "1006.08",
        "Compensation maneuvers in Eastern Ontario at 400m",
    ),
    (56609.00, 57922.00, "1006.09", "Transit to base"),
]

for start_time, end_time, line_number, description in segments_data_1006:
    FLT1006.add_segment(FlightSegment(start_time, end_time, line_number, description))
