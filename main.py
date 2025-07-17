from kripke import *
from LTL import *
from ltl_solver import *

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"

def print_start(test_number):
    print(f"{BLUE} attempting test {test_number} {RESET}")

def print_result(recieved,expected):
    if recieved==expected:
        print(f"{GREEN} test passed {RESET}")
    else:
        print(f"{RED} test failed {RESET}")

def test_1():
    """
    Eventually(p) holds if p reachable.
    """
    print_start(1)
    k = Kripke(3)
    k.vertex[0].add_labels(["q"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels([])

    k.add_edges([(0, 1), (1, 2)])

    formula = Eventually(Prop("p"))
    result = LTL_solver(formula, k, 1)
    print_result(result,True)


def test_2():
    """
    Test Always(p): should fail if one reachable state lacks p.
    """
    print_start(2)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels([])

    k.add_edges([(0, 1), (1, 2)])

    formula = Always(Prop("p"))
    result = LTL_solver(formula, k, 1)
    print_result(result,False)


def test_3():
    """
    Test Until(p, q): p holds until q holds
    """
    print_start(3)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels(["q"])

    k.add_edges([(0, 1), (1, 2)])

    formula = Until(Prop("p"), Prop("q"))
    result = LTL_solver(formula, k, 1)
    print_result(result,True)

def test_4():
    """
    Fail case for Until(p, q): q unreachable
    """
    print_start(4)
    k = Kripke(2)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])

    k.add_edges([(0, 1)])

    formula = Until(Prop("p"), Prop("q"))
    result = LTL_solver(formula, k, 1)
    print_result(result,False)

def test_5():
    """
    Not(Eventually(p)) should be False if p is reachable.
    """
    print_start(5)
    k = Kripke(2)
    k.vertex[0].add_labels(["r"])
    k.vertex[1].add_labels(["p"])
    k.add_edges([(0, 1)])

    formula = Not(Eventually(Prop("p")))
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def test_6():
    """
    Next(p) is True only if next state has p.
    """
    print_start(6)
    k = Kripke(2)
    k.vertex[0].add_labels([])
    k.vertex[1].add_labels(["p"])
    k.add_edges([(0, 1)])

    formula = Next(Prop("p"))
    result = LTL_solver(formula, k, 0)
    print_result(result, True)


def test_7():
    """
    Eventually(p AND q): p and q must be in same state.
    """
    print_start(7)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["q"])
    k.vertex[2].add_labels(["p", "q"])
    k.add_edges([(0, 1), (1, 2)])

    formula = Eventually(And(Prop("p"), Prop("q")))
    result = LTL_solver(formula, k, 0)
    print_result(result, True)


def test_8():
    """
    Or(Eventually(p), Eventually(q)) holds if either is reachable.
    """
    print_start(8)
    k = Kripke(3)
    k.vertex[0].add_labels(["a"])
    k.vertex[1].add_labels(["x"])
    k.vertex[2].add_labels(["q"])
    k.add_edges([(0, 1), (1, 2)])

    formula = Or(Eventually(Prop("p")), Eventually(Prop("q")))
    result = LTL_solver(formula, k, 0)
    print_result(result, True)

def test_9():
    """
    Eventually(p AND q) is False if no state has both.
    """
    print_start(9)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["q"])
    k.vertex[2].add_labels(["r"])
    k.add_edges([(0, 1), (1, 2)])

    formula = Eventually(And(Prop("p"), Prop("q")))
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def test_10():
    """
    Always(p) is False if any reachable state lacks p.
    """
    print_start(10)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels(["q"])  # Breaks Always(p)
    k.add_edges([(0, 1), (1, 2)])

    formula = Always(Prop("p"))
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def test_11():
    """
    p Until q is False if q is never reached.
    """
    print_start(11)
    k = Kripke(4)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels(["p"])
    k.vertex[3].add_labels(["r"])
    k.add_edges([(0, 1), (1, 2), (2, 3)])

    formula = Until(Prop("p"), Prop("q"))
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def test_12():
    """
    Always(p => q) is False if p is true but q is not in any reachable state.
    """
    print_start(12)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels([])  # q is never true
    k.add_edges([(0, 1), (1, 2)])

    formula = Always(Or(Not(Prop("p")), Prop("q")))  # p => q
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def test_13():
    """
    Eventually(Always(p)) is False if there's no suffix where p is always true.
    """
    print_start(13)
    k = Kripke(3)
    k.vertex[0].add_labels(["p"])
    k.vertex[1].add_labels(["p"])
    k.vertex[2].add_labels(["r"])  # breaks Always(p)
    k.add_edges([(0, 1), (1, 2)])

    formula = Eventually(Always(Prop("p")))
    result = LTL_solver(formula, k, 0)
    print_result(result, False)


def main():
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    test_7()
    test_8()
    test_9()
    test_10()
    test_11()
    test_12()
    test_13()
    

if __name__=="__main__":
    main()