"""
Author: Jani Bizjak
E-mail: janibizjak@gmail.com
Date: 15.04.2020
Updated on: 20.04.2020
Python version: 3.7

Assumptions 1: Solution assumes that given sellers list is ordered by the arrival day of sellers. Otherwise a list
sorting needs to be done first.
Assumption 2: I assume input arguments are valid and therefore don't check for None values, strings instead of integers.

"""

def calculate_purchasing_plan_old(total_days, sellers, starting_bread=10):
    """
    total_days : positive int
    sellers : list of tuple (day, price)
    starting_bread : int, optional
    """
    # Initialize total_days, price of starting bread is 0, the rest should be infinity, since we don't have bread.
    # Each day is saved as a tuple (seller_index, arrival_day, price), it makes it easier to count purchases later.
    cost_of_day = [(0, 0, 0)] * min(starting_bread, 30) + [(-1, 0, float('inf'))] * (
            total_days - min(starting_bread, 30))

    # Buy bread from each seller if his price is lower than current cost of bread for that day.
    for i in range(len(sellers)):
        # Maximum number of bread that can be bought from a seller is 30 or less if we get free bread before.
        for j in range(sellers[i][0], min(sellers[i][0] + 30, total_days)):
            cost_of_day[j] = min([cost_of_day[j], ((i + 1,) + sellers[i])], key=lambda t: t[2])

    # Go through price of bread per day and count how many pieces we buy from each seller.
    purchases = [0] * (len(sellers) + 2)
    for best_seller in cost_of_day:
        purchases[best_seller[0]] += 1

    if purchases[-1] != 0:  # Check if there is any stale bread
        return None

    return purchases[1:-1]  # Value at 0 is starting bread, value at -1 is days with stale bread

def print_matrix(cost_matrix):
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[i])):
            print("%4s " % cost_matrix[i][j], end="|")
        print()


def calculate_purchasing_plan(total_days, sellers, starting_bread=10, best_before_date=30, debug = False):
    """
    total_days : positive int
    sellers : list of tuple (day, price)
    starting_bread : int, optional
    best_before_date : positive int, (how long the bread lasts)
    debug : boolean, (prints cost matrix)
    """
    # create cost_matrix of (sellers+1) x total_days
    cost_matrix = [[0] * starting_bread + [float('inf')] * (total_days - min(starting_bread, best_before_date))]
    for merchant in sellers:
        cost_matrix.append(
            [float('inf')] * (merchant[0]) +  # Add inf before
            [merchant[1]] * min(best_before_date, (total_days - merchant[0])) +  # Add merchant price
            [float('inf')] * (total_days - merchant[0] - min(best_before_date, (total_days - merchant[0]))))  # Add inf after

    if debug:
        print_matrix(cost_matrix)

    current_merchant = len(sellers)
    current_day = total_days - 1
    best_merchant = current_merchant
    merchant_of_the_day = [0] * total_days

    new_merchant = True  # If the merchant changes, we want to go as far up as possible
    while current_day >= starting_bread:
        best_price = cost_matrix[best_merchant][current_day]

        # go up as far as you can
        for best_merchant_index in range(current_merchant, -1, -1):
            tmp = cost_matrix[best_merchant_index][current_day]

            # go up only if price is lower
            if tmp < best_price or (tmp <= best_price and new_merchant):  # Up only if lower price or new merchant
                # print("Better merchant found %3s with price %3s <= %3s" % (best_merchant_index, tmp, best_price))
                best_merchant = best_merchant_index
                best_price = tmp
                new_merchant = True

        merchant_of_the_day[current_day] = best_merchant  # Save from which merchant we buy bread on selected day
        current_day -= 1  # go left one step

        if best_price == float('inf'):
            if debug:
                print("Plan not feasible on day %5s" % current_day)
            return None
        new_merchant = False  # No new merchant for the previous day yet

    #  At this point we have fewest # merchants and lowest price. We need to make another walk from left to right to buy
    #  bread as soon as possible.

    buying_plan = [0] * (len(sellers) + 1)  # +1 is because initial bread is accounted for in the matrix
    current_merchant = 0
    current_day = 0
    while current_day < total_days:
        # If cost of current merchant is the same as cost of the merchant of the day, buy from current, since we buy
        # bread from him earlier (because merchants are sorted by their arrival day)
        if cost_matrix[current_merchant][current_day] > cost_matrix[merchant_of_the_day[current_day]][current_day]:
            current_merchant = merchant_of_the_day[current_day]
        buying_plan[current_merchant] += 1
        current_day += 1

    return buying_plan[1:] # First value shows initial bread.

if __name__ == "__main__":
    print("1",calculate_purchasing_plan_old(60, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Example
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Example
    print("1",calculate_purchasing_plan_old(30, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Shorter period
    print("2",calculate_purchasing_plan(30, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Shorter period
    print("1",calculate_purchasing_plan_old(90, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid last period
    print("2",calculate_purchasing_plan(90, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid last period
    print("1",calculate_purchasing_plan_old(60, [(11, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid start
    print("2",calculate_purchasing_plan(60, [(11, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid start
    print("1",calculate_purchasing_plan_old(60, [(10, 200), (15, 100), (50, 500), (50, 30)]))  # Invalid 3rd
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (50, 500), (50, 30)]))  # Invalid 3rd
    print("1",calculate_purchasing_plan_old(60, [(10, 200), (15, 100), (16, 100), (35, 500), (50, 30)]))  # Same price
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (16, 100), (35, 500), (50, 30)]))  # Same price
    print("1",calculate_purchasing_plan_old(60, [(10, 200), (15, 100), (15, 100), (35, 500), (50, 30)]))  # Same price same day
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (15, 100), (35, 500), (50, 30)]))  # Same price same day
    print("1",calculate_purchasing_plan_old(60, [(10, 200), (15, 150), (15, 100), (35, 500), (50, 30)]))  # Reverse order price
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 150), (15, 100), (35, 500), (50, 30)]))  # Reverse order price
    print("1",calculate_purchasing_plan_old(60, [(10,200),(10,200),(10,200),(11,200),(15,100),(35,500),(50,30)]))
    print("2",calculate_purchasing_plan(60, [(10,200),(10,200),(10,200),(11,200),(15,100),(35,500),(50,30)]))
    print("1",calculate_purchasing_plan_old(60, [(10,200), (10,200), (10,200), (11,200), (15,100), (35,500), (50,30)]))
    print("2",calculate_purchasing_plan(60, [(10,200), (10,200), (10,200), (11,200), (15,100), (35,500), (50,30)]))
    print()
    print("1",calculate_purchasing_plan(50, [(5, 100), (10, 100), (15, 100), (45, 50)], 5))
    print("2",calculate_purchasing_plan_old(50, [(5, 100), (10, 100), (15, 100), (45, 50)], 5))
    print("1",calculate_purchasing_plan(50, [(5, 100), (10, 100), (20, 100), (45, 100)], 5))
    print("2",calculate_purchasing_plan_old(50, [(5, 100), (10, 100), (20, 100), (45, 100)], 5))
    print("1",calculate_purchasing_plan(50, [(5, 100), (10, 100), (15, 100), (40, 50)], 5))
    print("2",calculate_purchasing_plan_old(50, [(5, 100), (10, 100), (15, 100), (40, 50)], 5))
    print()
    print(calculate_purchasing_plan(10, [(1, 4), (3, 4), (5, 4), (7, 4)], 1, 4, True), "[4, 2, 0, 3]")
    print(calculate_purchasing_plan(10, [(0, 4), (3, 4), (6, 4), (6, 4)], 0, 4, True), "[4, 3, 3, 0]")
    print(calculate_purchasing_plan(7, [(0, 4), (1, 4), (2, 4), (3, 4)], 0, 4, True), "[4, 0, 0, 3]")
    print(calculate_purchasing_plan(7, [(0, 4), (1, 4), (2, 2), (3, 4)], 5, 4, True), "[0, 0, 1, 1]")
    print(calculate_purchasing_plan(16, [(2, 5), (4, 3), (6, 1), (10, 20), (10, 15), (12, 4)], 3, 4, True), "[1, 2, 4, 0, 2, 4]")
    print(calculate_purchasing_plan(13, [(0, 1), (3, 1), (5, 3), (9, 5)], 0, 4, True), "[4, 3, 2, 4]")
    print(calculate_purchasing_plan(13, [(0, 1), (3, 1), (5, 3), (10, 5)], 0, 4, True), "None")