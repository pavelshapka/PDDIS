import unittest
import allure
from app import app


@allure.feature('Тест калькулятора')
class Test_calculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = app.Calculator()
    
    def test_add(self) -> None:
        self.assertEqual(self.calculator.add(5., 7.), 12.)

    def test_sub(self) -> None:
        self.assertEqual(self.calculator.sub(5., 7.), -2.)

    def test_mul(self) -> None:
        self.assertEqual(self.calculator.mul(5., 7.), 35.)

if __name__ == "__main__":
    unittest.main()