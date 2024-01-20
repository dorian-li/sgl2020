from prettytable import PrettyTable
from typing_extensions import Dict, List


class FieldInfo:
    def __init__(self, field: str, units: str, description: str) -> None:
        self.field = field
        self.units = units
        self.description = description


class Note:
    def __init__(self, text: str, sub_notes: List["Note"] = None):
        self.text: str = text
        self.sub_notes: List[Note] = sub_notes if sub_notes is not None else []

    def add_sub_note(self, sub_note: "Note") -> None:
        self.sub_notes.append(sub_note)

    def __str__(self, level: int = 0) -> str:
        result: str = "  " * level + "- " + self.text + "\n"
        for sub_note in self.sub_notes:
            result += sub_note.__str__(level + 1)
        return result


class SensorPosition:
    def __init__(
        self,
        sensor: str,
        description: str,
        x: float,
        y: float,
        z: float,
        flight_number: str = None,
    ) -> None:
        self.sensor = sensor
        self.description = description
        self.x = x
        self.y = y
        self.z = z
        self.flight_number = flight_number


class SensorDescription:
    def __init__(self) -> None:
        self.fields: List[FieldInfo] = []
        self.sensor_positions: List[SensorPosition] = []
        self.field_notes: Dict[str, Note] = {}

    def add_field(self, field: str, units: str, description: str) -> None:
        self.fields.append(FieldInfo(field, units, description))

    def add_sensor_position(
        self,
        sensor: str,
        description: str,
        x: float,
        y: float,
        z: float,
        flight_number: str = None,
    ) -> None:
        self.sensor_positions.append(
            SensorPosition(sensor, description, x, y, z, flight_number)
        )

    def add_field_notes(self, field, note):
        self.field_notes[field] = note

    def describe(self) -> None:
        self.describe_notes()
        field_table = PrettyTable()
        field_table.field_names = ["Field", "Units", "Description"]
        for field in self.fields:
            field_table.add_row([field.field, field.units, field.description])
        print("Field Descriptions:")
        print(field_table)

        # 显示传感器位置信息
        sensor_table = PrettyTable()
        sensor_table.field_names = [
            "Sensor",
            "Description",
            "X",
            "Y",
            "Z",
            "Flight Number",
        ]
        for sensor in self.sensor_positions:
            sensor_table.add_row(
                [
                    sensor.sensor,
                    sensor.description,
                    sensor.x,
                    sensor.y,
                    sensor.z,
                    sensor.flight_number or "Default",
                ]
            )
        print("\nSensor Positions:")
        print(sensor_table)

    def describe_notes(self) -> None:
        print("Notes on Specific Flight Data Fields:")
        for field, note in self.field_notes.items():
            print(note)


# 创建 FlightDataDescription 实例
SENSOR_DESCRIPTIONS = SensorDescription()

# 添加字段信息
fields_data = [
    ("line", "-", "line number"),
    ("flight", "-", "flight number"),
    ("year", "-", "year"),
    ("doy", "-", "day of year"),
    ("tt", "s", "fiducial seconds past midnight UTC"),
    ("utm_x", "m", "x-coordinate, WGS-84 UTM zone 18N"),
    ("utm_y", "m", "y-coordinate, WGS-84 UTM zone 18N"),
    ("utm_z", "m", "z-coordinate, GPS altitude (WGS-84)"),
    ("msl", "m", "z-coordinate, GPS altitude above EGM2008 Geoid"),
    ("lat", "deg", "latitude, WGS-84"),
    ("lon", "deg", "longitude, WGS-84"),
    ("baro", "m", "barometric altimeter"),
    ("radar", "m", "filtered radar altimeter"),
    ("topo", "m", "radar topography (WGS-84)"),
    ("dem", "m", "digital elevation model from SRTM (WGS-84)"),
    ("drape", "m", "planned survey drape (WGS-84)"),
    ("ins_pitch", "deg", "INS-computed aircraft pitch"),
    ("ins_roll", "deg", "INS-computed aircraft roll"),
    ("ins_yaw", "deg", "INS-computed aircraft yaw"),
    ("diurnal", "nT", "measured diurnal"),
    ("mag_1_c", "nT", "Mag 1: compensated magnetic field"),
    ("mag_1_lag", "nT", "Mag 1: lag-corrected magnetic field"),
    ("mag_1_dc", "nT", "Mag 1: diurnal-corrected magnetic field"),
    ("mag_1_igrf", "nT", "Mag 1: IGRF & diurnal-corrected magnetic field"),
    ("mag_1_uc", "nT", "Mag 1: uncompensated magnetic field"),
    ("mag_2_uc", "nT", "Mag 2: uncompensated magnetic field"),
    ("mag_3_uc", "nT", "Mag 3: uncompensated magnetic field"),
    ("mag_4_uc", "nT", "Mag 4: uncompensated magnetic field"),
    ("mag_5_uc", "nT", "Mag 5: uncompensated magnetic field"),
    ("mag_6_uc", "nT", "Mag 6: uncompensated magnetic field"),
    ("flux_a_x", "nT", "Flux A: fluxgate x-axis"),
    ("flux_a_y", "nT", "Flux A: fluxgate y-axis"),
    ("flux_a_z", "nT", "Flux A: fluxgate z-axis"),
    ("flux_a_t", "nT", "Flux A: fluxgate total"),
    ("flux_b_x", "nT", "Flux B: fluxgate x-axis"),
    ("flux_b_y", "nT", "Flux B: fluxgate y-axis"),
    ("flux_b_z", "nT", "Flux B: fluxgate z-axis"),
    ("flux_b_t", "nT", "Flux B: fluxgate total"),
    ("flux_c_x", "nT", "Flux C: fluxgate x-axis"),
    ("flux_c_y", "nT", "Flux C: fluxgate y-axis"),
    ("flux_c_z", "nT", "Flux C: fluxgate z-axis"),
    ("flux_c_t", "nT", "Flux C: fluxgate total"),
    ("flux_d_x", "nT", "Flux D: fluxgate x-axis"),
    ("flux_d_y", "nT", "Flux D: fluxgate y-axis"),
    ("flux_d_z", "nT", "Flux D: fluxgate z-axis"),
    ("flux_d_t", "nT", "Flux D: fluxgate total"),
    ("ogs_mag", "nT", "OGS survey diurnal-corrected, levelled, magnetic field"),
    ("ogs_alt", "m", "OGS survey, GPS altitude (WGS-84)"),
    ("ins_acc_x", "m/s^2", "INS x-acceleration"),
    ("ins_acc_y", "m/s^2", "INS y-acceleration"),
    ("ins_acc_z", "m/s^2", "INS z-acceleration"),
    ("ins_wander", "rad", "INS-computed wander angle (ccw from north)"),
    ("ins_lat", "rad", "INS-computed latitude"),
    ("ins_lon", "rad", "INS-computed longitude"),
    ("ins_alt", "m", "INS-computed altitude (WGS-84)"),
    ("ins_vn", "m/s", "INS-computed north velocity"),
    ("ins_vw", "m/s", "INS-computed west velocity"),
    ("ins_vu", "m/s", "INS-computed vertical (up) velocity"),
    ("pitch_rate", "deg/s", "avionics-computed pitch rate"),
    ("roll_rate", "deg/s", "avionics-computed roll rate"),
    ("yaw_rate", "deg/s", "avionics-computed yaw rate"),
    ("lgtl_acc", "g", "avionics-computed longitudinal (forward) acceleration"),
    ("ltrl_acc", "g", "avionics-computed lateral (starboard) acceleration"),
    ("nrml_acc", "g", "avionics-computed normal (vertical) acceleration"),
    ("tas", "m/s", "avionics-computed true airspeed"),
    ("pitot_p", "kPa", "avionics-computed pitot pressure"),
    ("static_p", "kPa", "avionics-computed static pressure"),
    ("total_p", "kPa", "avionics-computed total pressure"),
    ("cur_com_1", "A", "current sensor: aircraft radio 1"),
    ("cur_ac_hi", "A", "current sensor: air conditioner fan high"),
    ("cur_ac_lo", "A", "current sensor: air conditioner fan low"),
    ("cur_tank", "A", "current sensor: cabin fuel pump"),
    ("cur_flap", "A", "current sensor: flap motor"),
    ("cur_strb", "A", "current sensor: strobe lights"),
    ("cur_srvo_o", "A", "current sensor: INS outer servo"),
    ("cur_srvo_m", "A", "current sensor: INS middle servo"),
    ("cur_srvo_i", "A", "current sensor: INS inner servo"),
    ("cur_heat", "A", "current sensor: INS heater"),
    ("cur_acpwr", "A", "current sensor: aircraft power"),
    ("cur_outpwr", "A", "current sensor: system output power"),
    ("cur_bat_1", "A", "current sensor: battery 1"),
    ("cur_bat_2", "A", "current sensor: battery 2"),
    ("vol_acpwr", "V", "voltage sensor: aircraft power"),
    ("vol_outpwr", "V", "voltage sensor: system output power"),
    ("vol_bat_1", "V", "voltage sensor: battery 1"),
    ("vol_bat_2", "V", "voltage sensor: battery 2"),
    ("vol_res_p", "V", "voltage sensor: resolver board (+)"),
    ("vol_res_n", "V", "voltage sensor: resolver board (-)"),
    ("vol_back_p", "V", "voltage sensor: backplane (+)"),
    ("vol_back_n", "V", "voltage sensor: backplane (-)"),
    ("vol_gyro_1", "V", "voltage sensor: gyroscope 1"),
    ("vol_gyro_2", "V", "voltage sensor: gyroscope 2"),
    ("vol_acc_p", "V", "voltage sensor: INS accelerometers (+)"),
    ("vol_acc_n", "V", "voltage sensor: INS accelerometers (-)"),
    ("vol_block", "V", "voltage sensor: block"),
    ("vol_back", "V", "voltage sensor: backplane"),
    ("vol_srvo", "V", "voltage sensor: servos"),
    ("vol_cabt", "V", "voltage sensor: cabinet"),
    ("vol_fan", "V", "voltage sensor: cooling fan"),
]

for field, units, description in fields_data:
    SENSOR_DESCRIPTIONS.add_field(field, units, description)

# 添加传感器位置信息
sensor_positions_data = [
    ("Mag 1", "Tail stinger", -12.01, 0, 1.37, "Flt1002-1007"),
    ("Mag 2", "Front cabin, aft of cockpit", -0.60, -0.36, 0, "Flt1002-1007"),
    ("Mag 3", "Mid cabin, near INS", -1.28, -0.36, 0, "Flt1002-1007"),
    ("Mag 4", "Rear cabin, floor", -3.53, 0, 0, "Flt1002-1007"),
    ("Mag 5", "Rear cabin, ceiling", -3.79, 0, 1.20, "Flt1002-1007"),
    ("Flux A", "Mid cabin, near fuel tank", -3.27, -0.60, 0, "Flt1002-1007"),
    ("Flux B", "Tail, base of stinger", -8.92, 0, 0.96, "Flt1002-1007"),
    ("Flux C", "Rear cabin, port", -4.06, 0.42, 0, "Flt1002-1007"),
    ("Flux D", "Rear cabin, starboard", -4.06, -0.42, 0, "Flt1002-1007"),
    # Modified orientation for Flt1008 & Flt1009
    ("Mag 1", "tail stinger", -12.01, 0, 1.37, "Flt1008-1009"),
    ("Mag 2", "port diamond vertex, rear floor", -3.77, 0.60, 0.10, "Flt1008-1009"),
    ("Mag 3", "forward diamond vertex, rear floor", -3.17, 0, 0.11, "Flt1008-1009"),
    ("Mag 4", "starboard diamond vertex, rear floor", -3.77, -0.60, 0.12, "Flt1008"),
    ("Mag 4", "starboard diamond vertex, rear floor", -3.77, -0.35, 0.12, "Flt1009"),
    ("Mag 5", "aft diamond vertex, rear floor", -4.37, 0, 0.10, "Flt1008-1009"),
    ("Mag 6", "center of diamond, rear floor", -3.77, 0, 0.19, "Flt1008-1009"),
    ("Flux A", "front cabin, near battery", -0.73, -0.60, 0, "Flt1008-1009"),
    ("Flux B", "tail at base of stinger", -8.92, 0, 0.96, "Flt1008-1009"),
    ("Flux C", "mid cabin starboard side", -1.56, -0.55, 0, "Flt1008-1009"),
    ("Flux D", "mid-rear cabin, near fuel tank", -2.35, -0.55, 0, "Flt1008-1009"),
]

for sensor_data in sensor_positions_data:
    if len(sensor_data) == 5:  # 如果数据中只有5个值，则添加一个默认的 flight_number
        sensor_data = sensor_data + (" ",)
    sensor, description, x, y, z, flight_number = sensor_data
    SENSOR_DESCRIPTIONS.add_sensor_position(sensor, description, x, y, z, flight_number)


dataset_overview_note = Note(
    "Dataset Overview",
    [
        Note("HDF5 data fields for 2020 SGL flight data."),
        Note("Data sampled at 10Hz."),
        Note(
            "Includes magnetic sensors, inertial navigation system, avionics, and electrical currents and voltages."
        ),
        Note("(WGS-84) is altitude above WGS-84 ellipsoid."),
    ],
)

# 构建 Note 对象并添加到 data_description 实例
radar_note = Note(
    "radar",
    [
        Note(
            "unavailable at some times due to flown altitude exceeding instrument range"
        )
    ],
)

ins_pitch_roll_yaw_note = Note(
    "ins_pitch, ins_roll, ins_yaw",
    [
        Note(
            "convention: yaw clockwise from north, then pitch up, then roll to starboard"
        )
    ],
)

ogs_mag_alt_note = Note(
    "ogs_mag & ogs_alt",
    [
        Note("included for reference only"),
        Note("sampled from original Ontario Geological Survey flown in 2013"),
        Note(
            "unavailable at some times due to flown position not over original OGS survey"
        ),
    ],
)

ins_acc_xyz_note = Note(
    "ins_acc_x, ins_acc_y, ins_acc_z",
    [
        Note("AIRGrav (airborne gravimeter) system (http://www.sgl.com/Gravity.html)"),
        Note("3-axis gimballed INS, run in local-level, wander-angle mechanization"),
        Note("corrected for temperature, misalignment, and scale factor"),
        Note(
            "digitizers used for accelerometers are sigma-delta type and require low-pass filtering to increase resolution"
        ),
        Note("ins_acc_x: nominally horizontal, ccw from north by ins_wander [rad]"),
        Note("ins_acc_y: nominally horizontal, 90 [deg] ccw from ins_acc_x"),
        Note(
            "ins_acc_z: nominally vertical (up), includes gravity term (~navigation frame)"
        ),
    ],
)

ins_alt_note = Note(
    "ins_alt",
    [Note("combined GPS/inertial altitude computed in real time, contains lag error")],
)

lgtl_ltrl_nrml_acc_note = Note(
    "lgtl_acc, ltrl_acc, nrml_acc",
    [
        Note(
            "Garmin avionics module 010-0G600-00 (https://www.garmin.com/en-US/p/6427)"
        ),
        Note("nrml_acc does not include gravity term (body frame)"),
    ],
)

# 将 Note 对象添加到 data_description 实例
SENSOR_DESCRIPTIONS.add_field_notes("dataset_overview", dataset_overview_note)
SENSOR_DESCRIPTIONS.add_field_notes("radar", radar_note)
SENSOR_DESCRIPTIONS.add_field_notes(
    "ins_pitch, ins_roll, ins_yaw", ins_pitch_roll_yaw_note
)
SENSOR_DESCRIPTIONS.add_field_notes("ogs_mag & ogs_alt", ogs_mag_alt_note)
SENSOR_DESCRIPTIONS.add_field_notes("ins_acc_x, ins_acc_y, ins_acc_z", ins_acc_xyz_note)
SENSOR_DESCRIPTIONS.add_field_notes("ins_alt", ins_alt_note)
SENSOR_DESCRIPTIONS.add_field_notes(
    "lgtl_acc, ltrl_acc, nrml_acc", lgtl_ltrl_nrml_acc_note
)
