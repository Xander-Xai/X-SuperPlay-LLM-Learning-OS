"""Unit tests for the deterministic synthetic tool boundary, no external deps."""
import unittest

from gateway import (
    AccessDenied,
    EvidenceMismatch,
    InvalidCall,
    execute,
    synthetic_example,
    verify_final,
)


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.trace = []

    def inv(self, role="guest", product="A"):
        return execute(role, {"name": "query_inventory", "arguments": {"product_id": product}}, self.trace)

    def docs(self, role="guest", product="A"):
        return execute(role, {"name": "search_docs", "arguments": {"product_id": product}}, self.trace)

    def test_public_product_and_evidence(self):
        self.assertTrue(verify_final(
            "guest", "A", {"product_id": "A", "stock": 12, "citation_id": "doc-A"},
            [self.inv(), self.docs()],
        ))

    def test_unauthorized_product_fails_before_tool(self):
        with self.assertRaises(AccessDenied):
            self.inv("guest", "B")
        self.assertEqual(self.trace[-1]["status"], "error")

    def test_staff_can_read_staff_only_product(self):
        self.assertEqual(self.inv("staff", "B")["stock"], 3)
        self.assertEqual(self.docs("staff", "B")[0]["id"], "doc-B")

    def test_unknown_tool_not_executed(self):
        with self.assertRaises(InvalidCall):
            execute("guest", {"name": "delete_database", "arguments": {"product_id": "A"}}, self.trace)

    def test_extra_arguments_are_rejected(self):
        with self.assertRaises(InvalidCall):
            execute("guest", {"name": "query_inventory",
                              "arguments": {"product_id": "A", "role": "staff"}}, self.trace)

    def test_invalid_product_is_rejected(self):
        with self.assertRaises(InvalidCall):
            self.inv("guest", "MISSING")

    def test_fabricated_stock_rejected(self):
        with self.assertRaises(EvidenceMismatch):
            verify_final("guest", "A",
                         {"product_id": "A", "stock": 999, "citation_id": "doc-A"},
                         [self.inv(), self.docs()])

    def test_fabricated_citation_rejected(self):
        with self.assertRaises(EvidenceMismatch):
            verify_final("guest", "A",
                         {"product_id": "A", "stock": 12, "citation_id": "doc-UNKNOWN"},
                         [self.inv(), self.docs()])

    def test_role_cannot_be_model_supplied(self):
        with self.assertRaises(InvalidCall):
            execute("guest", {"name": "query_inventory",
                              "arguments": {"product_id": "B"}, "role": "staff"}, self.trace)

    def test_trace_does_not_include_inventory_or_claims(self):
        self.inv()
        self.docs()
        self.assertEqual({*self.trace[0]}, {"tool", "status", "duration_ms"})
        self.assertNotIn("stock", repr(self.trace))
        self.assertNotIn("适合基础保湿", repr(self.trace))

    def test_synthetic_example_is_clearly_labeled(self):
        x = synthetic_example()
        self.assertEqual(x["mode"], "SYNTHETIC_NO_MODEL")
        self.assertTrue(x["verified"])


if __name__ == "__main__":
    unittest.main()

