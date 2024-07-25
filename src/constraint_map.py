from constraint import Constraint
from typing import Dict


class ConstraintMap(Constraint[tuple, tuple]):
    def __init__(self, point1, point2) -> None:
        super().__init__([point1, point2])
        self.point1 = point1
        self.point2 = point2

    def satisfied(self, assignment: Dict[tuple, str]) -> bool:
        if self.point1 not in assignment or self.point2 not in assignment:
            return True

        return assignment[self.point1] != assignment[self.point2]
