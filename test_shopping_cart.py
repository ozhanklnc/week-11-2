import unittest
from cart import ShoppingCart


class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_single_item(self):
        self.cart.add_item("apple", 1.50, 3)
        self.assertEqual(self.cart._items["apple"]["price"], 1.50)
        self.assertEqual(self.cart._items["apple"]["quantity"], 3)

    def test_add_item_default_quantity_is_1(self):
        self.cart.add_item("banana", 0.75)
        self.assertEqual(self.cart._items["banana"]["quantity"], 1)

    def test_add_item_price_zero_is_allowed(self):
        self.cart.add_item("freebie", 0.0, 2)
        self.assertEqual(self.cart._items["freebie"]["price"], 0.0)

    def test_add_multiple_different_items(self):
        self.cart.add_item("apple", 1.00)
        self.cart.add_item("milk", 2.00)
        self.assertEqual(len(self.cart._items), 2)

    def test_add_same_item_twice_accumulates_quantity(self):
        self.cart.add_item("apple", 1.00, 3)
        self.cart.add_item("apple", 1.00, 2)
        self.assertEqual(self.cart._items["apple"]["quantity"], 5)


class TestTotal(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_total_single_item(self):
        self.cart.add_item("pen", 2.50, 4)
        self.assertEqual(self.cart.get_total(), 10.00)

    def test_total_multiple_items(self):
        self.cart.add_item("pen", 2.00, 2)
        self.cart.add_item("book", 5.00, 1)
        self.assertEqual(self.cart.get_total(), 9.00)

    def test_total_empty_cart_is_zero(self):
        self.assertEqual(self.cart.get_total(), 0.00)

    def test_total_after_clear(self):
        self.cart.add_item("item", 10.00)
        self.cart.clear()
        self.assertEqual(self.cart.get_total(), 0.00)


class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_remove_existing_item(self):
        self.cart.add_item("apple", 1.00)
        self.cart.remove_item("apple")
        self.assertNotIn("apple", self.cart._items)

    def test_remove_nonexistent_item_raises(self):
        with self.assertRaises(KeyError):
            self.cart.remove_item("ghost")


class TestDiscounts(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_save10_applied_correctly(self):
        self.cart.add_item("item", 100.00)
        self.cart.apply_discount("SAVE10")
        self.assertEqual(self.cart.get_total(), 90.00)

    def test_save20_applied_correctly(self):
        self.cart.add_item("item", 60.00)
        self.cart.apply_discount("SAVE20")
        self.assertEqual(self.cart.get_total(), 48.00)

    def test_flat5_applied_correctly(self):
        self.cart.add_item("item", 40.00)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 35.00)

    def test_flat5_never_goes_negative(self):
        self.cart.add_item("item", 3.00)
        self.cart._discount = {"type": "fixed", "value": 50.0}
        self.assertEqual(self.cart.get_total(), 0.00)


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", 1.00, 0)

    def test_add_item_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", 1.00, -5)

    def test_add_item_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", -1.00)

    def test_invalid_discount_code_raises(self):
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FAKE99")

    def test_discount_below_min_order_raises(self):
        self.cart.add_item("item", 10.00)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FLAT5")

    def test_save20_below_min_order_raises(self):
        self.cart.add_item("item", 40.00)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("SAVE20")


class TestBoundary(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_discount_at_exact_min_order_is_accepted(self):
        self.cart.add_item("item", 30.00)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 25.00)

    def test_discount_one_cent_above_threshold_is_accepted(self):
        self.cart.add_item("item", 30.01)
        self.cart.apply_discount("FLAT5")
        self.assertAlmostEqual(self.cart.get_total(), 25.01, places=2)


class TestGetItemCount(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_count_is_zero(self):
        self.assertEqual(self.cart.get_item_count(), 0)

    def test_single_item_count(self):
        self.cart.add_item("apple", 1.00, 5)
        self.assertEqual(self.cart.get_item_count(), 5)

    def test_multiple_items_count(self):
        self.cart.add_item("apple", 1.00, 3)
        self.cart.add_item("milk", 2.00, 2)
        self.assertEqual(self.cart.get_item_count(), 5)

    def test_count_after_remove(self):
        self.cart.add_item("apple", 1.00, 3)
        self.cart.add_item("milk", 2.00, 2)
        self.cart.remove_item("apple")
        self.assertEqual(self.cart.get_item_count(), 2)

    def test_count_after_clear(self):
        self.cart.add_item("apple", 1.00, 10)
        self.cart.clear()
        self.assertEqual(self.cart.get_item_count(), 0)


if __name__ == "__main__":
    unittest.main()
