import map_instance_generator as mig
import matplotlib.pyplot as plt
from csp import CSP
from constraint_einstein import ConstraintEinstein
import time


def plot_map_solution(tri, map_variables, results):
    for result in results:
        plt.triplot(map_variables[:, 0], map_variables[:, 1], tri.simplices)
        for point, color in result.items():
            plt.plot(point[0], point[1], 'o', c=color)
        plt.show()


def test_map(var_type, val_type, alg_type, neighbourhood, tri):
    # neighbourhood, tri, random_points = mig.generate_instance(problem_size)
    map_variables = mig.get_variables(neighbourhood)
    map_domains = {}
    for variable in map_variables:
        map_domains[variable] = ["yellow", "red", "green", "black"]
    map_constraints = mig.get_constraints(neighbourhood)
    CSP_map = CSP(map_variables, map_domains, map_constraints)
    if alg_type == 'BT':
        CSP_map_result = CSP_map.backtracking_search_single({}, [])
    elif alg_type == 'FC':
        CSP_map_result = CSP_map.backtracking_forward_check_single({}, [], map_domains, var_type, val_type)
    print(CSP_map.counter)
    # print(CSP_map_result)
    #plot_map_solution(tri, random_points, CSP_map_result)
    return CSP_map.counter


def test_einstein(alg_type):
    country = ["Norwegian", "Danish", "English", "German", "Swedish"]
    colour = ["yellow", "blue", "red", "green", "white"]
    smokes = ["cigar", "light", "no_filter", "pipe", "menthol"]
    drinks = ["water", "tea", "milk", "coffee", "beer"]
    animals = ["cats", "horses", "birds", "fish", "dogs"]
    variables = country + colour + smokes + drinks + animals
    domain = [1, 2, 3, 4, 5]
    einstein_domains = {}

    for i in range(len(variables)):
        einstein_domains[variables[i]] = domain.copy()

    constraints = [
        ConstraintEinstein(lambda a: a == 1, ["Norwegian"]),                      # 1.norweg - 1dom
        ConstraintEinstein(lambda a, b: a == b, ("English", "red")),              # 2.anglik - czerwony dom.
        ConstraintEinstein(lambda a, b: b - a == 1, ("green", "white")),          # 3.zeilony dom bezposrednio po lewej bialego.
        ConstraintEinstein(lambda a, b: a == b, ("Danish", "tea")),               # 4.dunczyk pije herbate.
        ConstraintEinstein(lambda a, b: abs(a - b) == 1, ("light", "cats")),      # 5.palacz light obok hodowcy kotow
        ConstraintEinstein(lambda a, b: a == b, ("yellow", "cigar")),             # 6.mieszkaniec zoltego pali cygara
        ConstraintEinstein(lambda a, b: a == b, ("German", "pipe")),              # 7.niemiec pali fajke
        ConstraintEinstein(lambda a: a == 3, ["milk"]),                           # 8.mieszkeniec srodkowego pije mleko
        ConstraintEinstein(lambda a, b: abs(a - b) == 1, ("light", "water")),     # 9.palacz light ma sasiada co pije wode
        ConstraintEinstein(lambda a, b: a == b, ("no_filter", "birds")),          # 10.palacz bez filtra hoduje ptaki
        ConstraintEinstein(lambda a, b: a == b, ("Swedish", "dogs")),             # 11.szwed hoduje psy
        ConstraintEinstein(lambda a, b: abs(a - b) == 1, ("Norwegian", "blue")),  # 12.norweg mieszka obok niebieskiego
        ConstraintEinstein(lambda a, b: abs(a - b) == 1, ("horses", "yellow")),   # 13.hodowca koni mieszka obok żółtego
        ConstraintEinstein(lambda a, b: a == b, ("menthol", "beer")),             # 14.palacz mentolowych pije piwo.
        ConstraintEinstein(lambda a, b: a == b, ("green", "coffee")),             # 15.w zielonym domu pije się kawę
        ConstraintEinstein(lambda: ConstraintEinstein.all_different_constraint, country),
        ConstraintEinstein(lambda: ConstraintEinstein.all_different_constraint, colour),
        ConstraintEinstein(lambda: ConstraintEinstein.all_different_constraint, smokes),
        ConstraintEinstein(lambda: ConstraintEinstein.all_different_constraint, drinks),
        ConstraintEinstein(lambda: ConstraintEinstein.all_different_constraint, animals),
    ]

    CSP_einstein = CSP(variables, einstein_domains, constraints)
    if alg_type == 'BT':
        CSP_einstein_result = CSP_einstein.backtracking_search_single({}, [])
    elif alg_type == 'FC':
        CSP_einstein_result = CSP_einstein.backtracking_forward_check_single({}, [], einstein_domains, 'NUV', 'NVFD')
    print(CSP_einstein.counter)
    print(CSP_einstein_result)


def test_map_nodes_time():
    var_types = ['NUV', 'MRV', 'DH']
    x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    NUV_nodes = []
    MRV_nodes = []
    DH_nodes = []
    NUV_time = []
    MRV_time = []
    DH_time = []
    for i in range(3, 31):
        neighbourhood, tri, random_points = mig.generate_instance(i)
        for var_type in var_types:
            start = time.time()
            print(i)
            nodes = test_map(var_type, neighbourhood, tri)
            print(nodes)
            end = time.time()
            print(round((end - start), 2))
            if var_type == 'NUV':
                NUV_nodes.append(nodes)
                NUV_time.append(round((end - start), 2))
            elif var_type == 'MRV':
                MRV_nodes.append(nodes)
                MRV_time.append(round((end - start), 2))
            elif var_type == 'DH':
                DH_nodes.append(nodes)
                DH_time.append(round((end - start), 2))

    print(NUV_nodes)
    print(MRV_nodes)
    print(DH_nodes)
    print(NUV_time)
    print(MRV_time)
    print(DH_time)

    plt.plot(x, NUV_nodes)
    plt.plot(x, MRV_nodes)
    plt.plot(x, DH_nodes)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Amount of nodes visits')
    plt.legend(['Next unassigned variable', 'Minimum remaining value', 'Degree heuristic'])
    plt.show()

    plt.plot(x, NUV_time)
    plt.plot(x, MRV_time)
    plt.plot(x, DH_time)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Time duration')
    plt.legend(['Next unassigned variable', 'Minimum remaining value', 'Degree heuristic'])
    plt.show()


def test_val_type():
    val_types = ['NVFD', 'LCV']
    x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    NVFD_nodes = []
    LCV_nodes = []
    NVFD_time = []
    LCV_time = []

    for i in range(3, 31):
        neighbourhood, tri, random_points = mig.generate_instance(i)
        for val_type in val_types:
            start = time.time()
            print(i)
            nodes = test_map('NUV', val_type, neighbourhood, tri)
            print(nodes)
            end = time.time()
            print(round((end - start), 2))
            if val_type == 'NVFD':
                NVFD_nodes.append(nodes)
                NVFD_time.append(round((end - start), 2))
            elif val_type == 'LCV':
                LCV_nodes.append(nodes)
                LCV_time.append(round((end - start), 2))

    print(NVFD_nodes)
    print(LCV_nodes)
    print(NVFD_time)
    print(LCV_time)

    plt.plot(x, NVFD_nodes)
    plt.plot(x, LCV_nodes)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Amount of nodes visits')
    plt.legend(['Next value from domain', 'Least constraining values'])
    plt.show()

    plt.plot(x, NVFD_time)
    plt.plot(x, LCV_time)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Time duration')
    plt.legend(['Next value from domain', 'Least constraining values'])
    plt.show()


def test_alg():
    alg_types = ['BT', 'FC']
    x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
         , 33, 34, 35, 36, 37, 38, 39, 40]
    BT_nodes = []
    FC_nodes = []
    BT_time = []
    FC_time = []

    for i in range(3, 41):
        neighbourhood, tri, random_points = mig.generate_instance(i)
        for alg_type in alg_types:
            start = time.time()
            print(i)
            nodes = test_map('NUV', 'NVFD', alg_type, neighbourhood, tri)
            print(nodes)
            end = time.time()
            print(round((end - start), 2))
            if alg_type == 'BT':
                BT_nodes.append(nodes)
                BT_time.append(round((end - start), 2))
            elif alg_type == 'FC':
                FC_nodes.append(nodes)
                FC_time.append(round((end - start), 2))

    print(BT_nodes)
    print(FC_nodes)
    print(BT_time)
    print(FC_time)

    plt.plot(x, BT_nodes)
    plt.plot(x, FC_nodes)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Amount of nodes visits')
    plt.legend(['Backtracking', 'Forward checking'])
    plt.show()

    plt.plot(x, BT_time)
    plt.plot(x, FC_time)
    plt.xlabel('Amount of points (problem size)')
    plt.ylabel('Time duration')
    plt.legend(['Backtracking', 'Forward checking'])
    plt.show()


if __name__ == '__main__':
    # start = time.time()
    # test_einstein('FC')
    # end = time.time()
    # print(end - start)
    # test_map_nodes_time()
    # test_val_type()
    # test_alg()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    wells = [25, 20, 40, 40, 40, 60, 60, 80, 100]
    holes = [20, 40, 20, 50, 60, 60, 40, 80, 80]
    scores = [20, 40, 20, 20, 40, 40, 60, 60, 80]
    plt.plot(x, wells)
    plt.plot(x, holes)
    plt.plot(x, scores)
    plt.xlabel('Depth')
    plt.ylabel('% of wins vs depth 3')
    plt.legend(['wells', 'holes', 'scores'])
    plt.show()
