import unittest

from app.topology import LINKS
from app.routing import link_cost, ripguard


class TestRIPGuardMetrics(unittest.TestCase):

    def test_link_cost_is_positive(self):

        for link in LINKS:
            self.assertGreater(link_cost(link), 0)

    def test_selected_path_has_valid_endpoints(self):

        result = ripguard("R1", "R6")

        self.assertEqual(result["path"][0], "R1")
        self.assertEqual(result["path"][-1], "R6")

    def test_path_cost_matches_selected_path(self):

        result = ripguard("R1", "R6")

        expected_cost = 0

        for a, b in zip(
            result["path"],
            result["path"][1:]
        ):
            link = next(
                link for link in LINKS
                if {link["source"], link["target"]} == {a, b}
            )

            expected_cost += link_cost(link)

        self.assertAlmostEqual(
            result["path_cost"],
            round(expected_cost, 3),
            places=3
        )


if __name__ == "__main__":
    unittest.main()