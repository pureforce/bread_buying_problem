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

def calculate_purchasing_plan(total_days, sellers, starting_bread=10):
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


if __name__ == "__main__":
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Example
    print("2",calculate_purchasing_plan(30, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Shorter period
    print("2",calculate_purchasing_plan(90, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid last period
    print("2",calculate_purchasing_plan(60, [(11, 200), (15, 100), (35, 500), (50, 30)]))  # Invalid start