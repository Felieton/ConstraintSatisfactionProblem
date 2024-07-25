import sys

import constraint_einstein as ce
import copy


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains  # domain of each variable
        self.constraints = constraints
        self.counter = 0

    def consistent(self, assignment):
        for constraint in self.constraints:
            if not constraint.satisfied(assignment):
                return False

        return True

    def backtracking_search_single(self, assignment, solutions):
        if len(assignment) == len(self.variables):
            return assignment

        chosen_variable = self.next_unassigned_variable(assignment)
        # chosen_variable = self.degree_heuristic(assignment)
        # chosen_variable = self.minimum_remaining_value(assignment, self.domains)

        for value in self.values_from_domain(self.domains, chosen_variable):
        # for value in self.least_constraing_values(self.domains, chosen_variable, assignment,
        #                                          self.get_connected_unassigned_variables(chosen_variable, assignment)):
            local_assignment = assignment.copy()
            local_assignment[chosen_variable] = value
            self.counter += 1
            if self.consistent(local_assignment):
                result = self.backtracking_search_single(local_assignment, solutions)

                if result is not None:
                    return result
        return None

    def backtracking_search(self, assignment, solutions):
        if len(assignment) == len(self.variables):
            solutions.append(assignment)
            return assignment

        chosen_variable = self.next_unassigned_variable(assignment)
        # chosen_variable = self.degree_heuristic(assignment)
        # chosen_variable = self.minimum_remaining_value(assignment, self.domains)

        for value in self.values_from_domain(self.domains, chosen_variable):
        # for value in self.least_constraing_values(self.domains, chosen_variable, assignment,
        #                                          self.get_connected_unassigned_variables(chosen_variable, assignment)):
            local_assignment = assignment.copy()
            local_assignment[chosen_variable] = value
            self.counter += 1
            if self.consistent(local_assignment):
                self.backtracking_search(local_assignment, solutions)

        return solutions

    def get_connected_unassigned_variables(self, variable, assignment):
        variables = []
        for constraint in self.constraints:
            if type(constraint) is ce.ConstraintEinstein:
                if len(constraint.variables[0]) == 2:
                    if variable in constraint.variables[0]:
                        if variable == constraint.variables[0][0]:
                            if constraint.variables[0][1] not in assignment and constraint.variables[0][1]\
                                    not in variables:
                                variables.append(constraint.variables[0][1])
                        elif constraint.variables[0][0] not in assignment and constraint.variables[0][0]\
                                not in variables:
                            variables.append(constraint.variables[0][0])
                elif len(constraint.variables[0]) == 5:
                    if variable in constraint.variables[0]:
                        category_variables = [x for x in constraint.variables[0] if x != variable
                                              and x not in assignment and x not in variables]
                        variables += category_variables

            else:
                if variable == constraint.variables[0]:
                    if constraint.variables[1] not in assignment and constraint.variables[1] not in variables:
                        variables.append(constraint.variables[1])
                elif variable == constraint.variables[1]:
                    if constraint.variables[0] not in assignment and constraint.variables[0] not in variables:
                        variables.append(constraint.variables[0])

        return variables

    def backtracking_forward_check(self, assignment, solutions, domains, var_type, val_type):
        if len(assignment) == len(self.variables):
            solutions.append(assignment)
            return assignment

        if var_type == 'NUV':
            chosen_variable = self.next_unassigned_variable(assignment)
        elif var_type == 'MRV':
            chosen_variable = self.minimum_remaining_value(assignment, domains)
        elif var_type == 'DH':
            chosen_variable = self.degree_heuristic(assignment)

        neighbours = self.get_connected_unassigned_variables(chosen_variable, assignment)
        values = []

        if val_type == 'NVFD':
            values = self.values_from_domain(domains, chosen_variable)
        elif val_type == 'LCV':
            values = self.least_constraing_values(domains, chosen_variable, assignment, neighbours)

        for value in values:
            local_assignment = copy.deepcopy(assignment)
            local_assignment[chosen_variable] = value
            self.counter += 1
            local_domains = copy.deepcopy(domains)

            if self.consistent(local_assignment):
                for neighbour in neighbours:
                    for domain_value in local_domains[neighbour]:
                        if value in local_domains[neighbour]:
                            local_assignment[neighbour] = domain_value
                            if not self.consistent(local_assignment):
                                local_domains[neighbour].remove(domain_value)
                            del local_assignment[neighbour]
                self.backtracking_forward_check(local_assignment, solutions, local_domains, var_type, val_type)

        return solutions

    def backtracking_forward_check_single(self, assignment, solutions, domains, var_type, val_type):
        if len(assignment) == len(self.variables):
            return assignment

        if var_type == 'NUV':
            chosen_variable = self.next_unassigned_variable(assignment)
        elif var_type == 'MRV':
            chosen_variable = self.minimum_remaining_value(assignment, domains)
        elif var_type == 'DH':
            chosen_variable = self.degree_heuristic(assignment)

        neighbours = self.get_connected_unassigned_variables(chosen_variable, assignment)
        values = []

        if val_type == 'NVFD':
            values = self.values_from_domain(domains, chosen_variable)
        elif val_type == 'LCV':
            values = self.least_constraing_values(domains, chosen_variable, assignment, neighbours)

        for value in values:
            local_assignment = copy.deepcopy(assignment)
            local_assignment[chosen_variable] = value
            self.counter += 1
            local_domains = copy.deepcopy(domains)

            if self.consistent(local_assignment):
                for neighbour in neighbours:
                    for domain_value in local_domains[neighbour]:
                        if value in local_domains[neighbour]:
                            local_assignment[neighbour] = domain_value
                            if not self.consistent(local_assignment):
                                local_domains[neighbour].remove(domain_value)
                            del local_assignment[neighbour]
                result = self.backtracking_forward_check_single(local_assignment, solutions, local_domains, var_type, val_type)
                if result is not None:
                    return result

        return None

    def values_from_domain(self, domains, chosen_variable):
        return domains[chosen_variable]

    def least_constraing_values(self, domains, chosen_variable, assignment, neighbours):
        values_list = []
        priority_list = []
        for domain_value in domains[chosen_variable]:
            assignment[chosen_variable] = domain_value
            if self.consistent(assignment):
                values_list.append(domain_value)
                priority_list.append(0)
                for neighbour in neighbours:
                    for neighbour_value in domains[neighbour]:
                        assignment[neighbour] = neighbour_value
                        if self.consistent(assignment):
                            priority_list[-1] += 1
                        del assignment[neighbour]
            del assignment[chosen_variable]

        values_list = [x for _, x in sorted(zip(priority_list, values_list), reverse=True)]
        return values_list

    def next_unassigned_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]
        return first

    def degree_heuristic(self, assignment):
        max_constraint_amount = -1
        unassigned = [v for v in self.variables if v not in assignment]
        variable_to_return = unassigned[0]
        for variable in unassigned:
            constraint_counter = 0
            for constraint in self.constraints:
                if type(constraint) is ce.ConstraintEinstein:
                    if variable in constraint.variables[0]:
                        constraint_counter += 1
                else:
                    if variable in constraint.variables:
                        constraint_counter += 1
            if constraint_counter > max_constraint_amount:
                max_constraint_amount = constraint_counter
                variable_to_return = variable

        return variable_to_return

    def minimum_remaining_value(self, assignment, domains):
        min_domain_size = sys.maxsize
        unassigned = [v for v in self.variables if v not in assignment]
        variable_to_return = unassigned[0]
        for variable in unassigned:
            domain_size = len(domains[variable])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                variable_to_return = variable

        return variable_to_return
