import unittest

from app.topology import ROUTERS, LINKS
from app.routing import standard_rip, ripguard


class TestRoutingComparison(unittest.TestCase):

    def test_six_routers_exist(self):
        self.assertEqual(len(ROUTERS), 6)

    def test_standard_rip_finds_route(self):
        result = standard_rip("R1", "R6")

        self.assertIsNotNone(result["path"])
        self.assertEqual(result["path"][0], "R1")
        self.assertEqual(result["path"][-1], "R6")

    def test_ripguard_finds_route(self):
        result = ripguard("R1", "R6")

        self.assertIsNotNone(result["path"])
        self.assertEqual(result["path"][0], "R1")
        self.assertEqual(result["path"][-1], "R6")

    def test_failure_uses_alternative_path(self):

        failed = {frozenset(("R1", "R4"))}

        result = ripguard(
            "R1",
            "R6",
            failed_links=failed
        )

        self.assertIsNotNone(result["path"])
        self.assertNotIn(
            "R4",
            result["path"][1:2]
        )


if __name__ == "__main__":
    unittest.main()