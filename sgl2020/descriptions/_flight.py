from prettytable import PrettyTable
from typing_extensions import List


class FlightDescription:
    def __init__(
        self,
        flight_number: str,
        date: str,
        doy: str,
        compensations: List[str] = [],
        survey_lines: List[str] = [],
        issues: List["Report"] = [],
    ):
        self.flight_number = flight_number
        self.date = date
        self.doy = doy
        self.compensations = compensations
        self.survey_lines = survey_lines
        self.issues = issues
        self.segments: List["FlightSegment"] = []

    def add_segment(self, segment: "FlightSegment") -> None:
        self.segments.append(segment)

    @property
    def lines(self) -> List[str]:
        return list(set([seg.line_number for seg in self.segments]))

    def describe(self) -> None:
        print(f"Flight {self.flight_number}")
        print(f"Date: {self.date} (Day of Year: {self.doy})")
        print("Compensations:")
        if self.compensations:
            for compensation in self.compensations:
                print(f"  - {compensation}")
        else:
            print("  - No Description")
        print("Survey Lines:")
        if self.survey_lines:
            for line in self.survey_lines:
                print(f"  - {line}")
        else:
            print("  - No Description")
        print("Issues:")
        if self.issues:
            for issue in self.issues:
                issue.describe()
        else:
            print("  - No Description")
        print("\nFlight Segments:")
        segment_table = PrettyTable()
        segment_table.field_names = [
            "Start Time",
            "End Time",
            "Line Number",
            "Description",
        ]
        for segment in self.segments:
            segment_table.add_row(
                [
                    segment.start_time,
                    segment.end_time,
                    segment.line_number,
                    segment.description,
                ]
            )
        print(segment_table)


class FlightSegment:
    def __init__(
        self, start_time: float, end_time: float, line_number: str, description: str
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.line_number = line_number
        self.description = description

    def to_csv(self) -> str:
        return f'{self.start_time},{self.end_time},{self.line_number},"{self.description}"\n'


class Report:
    def __init__(self, description: str, affected_lines: List[str] = None) -> None:
        self.description = description
        self.affected_lines = affected_lines or []

    def describe(self) -> None:
        print(f"  - {self.description}")
        if self.affected_lines:
            print(f"    - Affected Lines: {', '.join(self.affected_lines)}")
