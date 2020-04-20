import unittest
from bread_buying_problem import calculate_purchasing_plan


class MyTestCase(unittest.TestCase):
	def test_given_example(self):
		initial_bread = 60
		calendar = [(10, 200), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 30, 5, 10])

	def test_shorter_period(self):
		initial_bread = 30
		calendar = [(10, 200), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 15, 0, 0])

	def test_invalid_last_period(self):
		initial_bread = 90
		calendar = [(10, 200), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, None)

	def test_invalid_start_period(self):
		initial_bread = 60
		calendar = [(11, 200), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, None)

	def test_invalid_third_merchant(self):
		initial_bread = 60
		calendar = [(10, 200), (15, 100), (50, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, None)

	def test_merchant_same_price(self):
		initial_bread = 60
		calendar = [(10, 200), (15, 100), (16, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 30, 1, 4, 10])

	def test_merchant_same_price_same_day(self):
		initial_bread = 60
		calendar = [(10, 200), (15, 100), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 30, 0, 5, 10])

	def test_reverse_order_price(self):
		initial_bread = 60
		calendar = [(10, 200), (15, 150), (15, 100), (35, 500), (50, 30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 0, 30, 5, 10])

	def test_hoard_bread_first(self):
		initial_bread = 60
		calendar = [(10,200),(10,200),(10,200),(11,200),(15,100),(35,500),(50,30)]
		solution = calculate_purchasing_plan(initial_bread, calendar)
		self.assertEqual(solution, [5, 0, 0, 0, 30, 5, 10])

	def test_minimize_num_merchants(self):
		initial_bread = 50
		starting_bread = 5
		calendar = [(5, 100), (10, 100), (15, 100), (45, 50)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread)
		self.assertEqual(solution, [30, 0, 10, 5])

	def test_minimize_num_merchants_2(self):
		initial_bread = 50
		starting_bread = 5
		calendar = [(5, 100), (10, 100), (20, 100), (45, 100)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread)
		self.assertEqual(solution, [30, 0, 15, 0])

	def test_minimize_num_merchants_3(self):
		initial_bread = 50
		starting_bread = 5
		calendar = [(5, 100), (10, 100), (20, 100), (45, 100)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread)
		self.assertEqual(solution, [30, 0, 15, 0])

	def test_hard_problem_1(self):
		initial_bread = 10
		starting_bread = 1
		bread_goes_stale_after = 4
		calendar = [(1, 4), (3, 4), (5, 4), (7, 4)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [4, 2, 0, 3])

	def test_hard_problem_2(self):
		initial_bread = 10
		starting_bread = 0
		bread_goes_stale_after = 4
		calendar = [(0, 4), (3, 4), (6, 4), (6, 4)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [4, 3, 3, 0])

	def test_hard_problem_3(self):
		initial_bread = 7
		starting_bread = 0
		bread_goes_stale_after = 4
		calendar = [(0, 4), (1, 4), (2, 4), (3, 4)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [4, 0, 0, 3])

	def test_hard_problem_4(self):
		initial_bread = 7
		starting_bread = 5
		bread_goes_stale_after = 4
		calendar = [(0, 4), (1, 4), (2, 2), (3, 4)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [0, 0, 1, 1])

	def test_hard_problem_5(self):
		initial_bread = 16
		starting_bread = 3
		bread_goes_stale_after = 4
		calendar = [(2, 5), (4, 3), (6, 1), (10, 20), (10, 15), (12, 4)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [1, 2, 4, 0, 2, 4])

	def test_hard_problem_5(self):
		initial_bread = 13
		starting_bread = 0
		bread_goes_stale_after = 4
		calendar = [(0, 1), (3, 1), (5, 3), (9, 5)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, [4, 3, 2, 4])

	def test_hard_problem_5(self):
		initial_bread = 13
		starting_bread = 0
		bread_goes_stale_after = 4
		calendar = [(0, 1), (3, 1), (5, 3), (10, 5)]
		solution = calculate_purchasing_plan(initial_bread, calendar, starting_bread, bread_goes_stale_after)
		self.assertEqual(solution, None)


if __name__ == '__main__':
	unittest.main()
