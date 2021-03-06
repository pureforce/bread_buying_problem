"""
Author: Jani Bizjak
E-mail: janibizjak@gmail.com
Date: 15.04.2020
Updated on: 20.04.2020
Python version: 3.7

Assumptions 1: Solution assumes that given sellers list is ordered by the arrival day of sellers. Otherwise a list
sorting needs to be done first.
Assumption 2: I assume input arguments are valid and therefore don't check for None values, strings instead of integers.

Idea of the solution: There needs to be one piece of bread per day for the duration of experiment. We can represent the
task as grid of dimensions #merchants * #days. We populate the matrix with prices for each merchant on the days that his
bread is available, if a bread from a merchant is not available on a selected day we assign infinite value to it. Each
column thus shows prices of different bread available on that day, if a column only has "inf" values, it means that
solution does not exist. To find a optimal solution we start in the last column. We find the merchant with lowest price,
if multiple merchants have same price on that day we select the one that is up-most. After we have a merchant selected
we go left as far as possible (either to the day when he arrives or another merchant provides bread with lower price).
When we change the merchant we again go up as far as possible and then left, repeating the process until we are in the
top left corner. This gives us solution with lowest price and fewest number of merchants, but the problem is that this
solution favours buying bread as late as possible (since we go from right to left). In order to fix this, we move
through selected merchants from left to right, but now we buy as much bread from the first selected merchant (if the
price is the same). After we are in the bottom right corner again, we have lowest price, with fewest merchants and most
stale bread (strange, villagers, preferring stale over fresh bread :))

The time complexity of the algorithm is O(m * n) + O(m) = O(m * n), where m is # of days and n is # of sellers.

From right to left (assuming bread lasts 3 days)
1. |  5  5  5  i  i  i  i  i  |->|  5  5  5  i  i  i  i  i  |->|  5  5  5  i  i  i  i  i  |->|  x  x  x  i  i  i  i  i |
2. |  i  i  5  5  5  i  i  i  |->|  i  i  5  5  5  i  i  i  |->|  i  i  5  5  5  i  i  i  |->|  i  i  5  5  5  i  i  i |
3. |  i  i  i  4  4  4  i  i  |->|  i  i  i  4  4  4  i  i  |->|  i  i  i  x  x  4  i  i  |->|  i  i  i  x  x  4  i  i |
4. |  i  i  i  i  4  4  4  i  |->|  i  i  i  i  4  4  4  i  |->|  i  i  i  i  4  4  4  i  |->|  i  i  i  i  4  4  4  i |
5. |  i  i  i  i  i  4  4  4  |->|  i  i  i  i  i  x  x  x  |->|  i  i  i  i  i  x  x  x  |->|  i  i  i  i  i  x  x  x |
This gives us solution [3, 0, 2, 0, 3], minimum price and lowest #of merchants but not the stalest of bread.
1. |  y  y  y  i  i  i  i  i  |->|  y  y  y  i  i  i  i  i  |->|  y  y  y  i  i  i  i  i  |
2. |  i  i  -  -  -  i  i  i  |->|  i  i  -  -  -  i  i  i  |->|  i  i  -  -  -  i  i  i  |
3. |  i  i  i  4  4  4  i  i  |->|  i  i  i  y  y  y  i  i  |->|  i  i  i  y  y  y  i  i  |
4. |  i  i  i  i  -  -  -  i  |->|  i  i  i  i  -  -  -  i  |->|  i  i  i  i  -  -  -  i  |
5. |  i  i  i  i  i  4  4  4  |->|  i  i  i  i  i  4  4  4  |->|  i  i  i  i  i  4  y  y  |
This gives us [3, 0, 3, 0, 2], lowest price, lowest # merchants, stalest bread.
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
    print("2",calculate_purchasing_plan(60, [(10, 200), (15, 100), (35, 500), (50, 30)]))  # Example
