from dataclasses import dataclass
from typing import List


@dataclass
class AccessRecord:
    user: str
    role: str
    department: str
    active: bool = True


class AccessService:
    def __init__(self):
        self.records: List[AccessRecord] = []

    def add(self, user: str, role: str, department: str, active: bool = True) -> AccessRecord:
        record = AccessRecord(user, role, department, active)
        self.records.append(record)
        return record

    def by_department(self, department: str) -> List[AccessRecord]:
        return [r for r in self.records if r.department == department and r.active]

    def to_table_rows(self) -> List[dict]:
        return [
            {"user": r.user, "role": r.role, "department": r.department, "active": str(r.active).lower()}
            for r in self.records
        ]
