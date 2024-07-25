from constraint import Constraint
from typing import Dict


class ConstraintEinstein(Constraint[tuple, tuple]):
    def __init__(self, func, values):
        super().__init__([values])
        self.func = func
        self.values = values

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if len(self.values) > 2:
            return self.all_different_constraint(assignment, self.values)

        in_assignment = []

        for value in self.values:
            if value in assignment:
                in_assignment.append(assignment[value])
            else:
                return True

        if len(in_assignment) == len(self.values):
            return self.func(*in_assignment)

    @staticmethod
    def all_different_constraint(assignment, values):
        values_in_assignment = []
        for value in values:
            if value in assignment:
                values_in_assignment.append(assignment[value])

        return len(values_in_assignment) == len(set(values_in_assignment))
