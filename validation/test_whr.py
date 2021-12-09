import unittest
from estimations.run_whr import integrate, logistic_likelihood
from whr import whole_history_rating


class TestWHR(unittest.TestCase):
    def test_logistic_no_handicap(self):
        result = logistic_likelihood(0.0)
        expected = whole_history_rating.Base().probability_future_match("alice", "bob", 0.0)[0]

        self.assertAlmostEqual(result, expected)

    def test_logistic_handicap(self):
        result = logistic_likelihood(100.0)
        expected = whole_history_rating.Base().probability_future_match("alice", "bob", 100.0)[0]

        self.assertAlmostEqual(result, expected)

    def test_integrate_standard(self):
        result = integrate(0.0, 1.0, logistic_likelihood)
        expected = 0.5

        self.assertAlmostEqual(result, expected)

    def test_integrate_small_diff(self):
        result = integrate(50.0, 10.0, logistic_likelihood)
        opponent_result = integrate(-50.0, 10.0, logistic_likelihood)
        expected = 0.571405  # resultado calculado con WolframAlpha

        self.assertAlmostEqual(result, expected, places=4)
        self.assertAlmostEqual(result + opponent_result, 1.0)

    def test_integrate_big_diff(self):
        result = integrate(200.0, 10.0, logistic_likelihood)
        opponent_result = integrate(-200.0, 10.0, logistic_likelihood)
        expected = 0.75959  # resultado calculado con WolframAlpha

        self.assertAlmostEqual(result, expected, places=4)
        self.assertAlmostEqual(result + opponent_result, 1.0)


if __name__ == '__main__':
    unittest.main()
