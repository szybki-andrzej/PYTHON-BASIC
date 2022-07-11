import unittest
from stock_info import ceo_year_born_data, week_change_data, holds_data


class TestStockInfo(unittest.TestCase):
    def test_ceo_year_born_data(self):
        ceo_year_born_tab = ceo_year_born_data()
        for record in ceo_year_born_tab:
            if record[1] == 'AMD':
                self.assertEqual(record[0], 'Advanced Micro Devices, Inc.')
                self.assertEqual(record[2], 'United States')
                self.assertEqual(record[3], '15,500')
                self.assertEqual(record[4], 'Dr. Lisa T. Su Ph.D.')
                self.assertEqual(record[5], '1970')

            if record[1] == 'NVDA':
                self.assertEqual(record[0], 'NVIDIA Corporation')
                self.assertEqual(record[2], 'United States')
                self.assertEqual(record[3], '22,473')
                self.assertEqual(record[4], 'Mr. Jen-Hsun  Huang')
                self.assertEqual(record[5], '1963')

    def test_week_change_data(self):
        week_change_tab = week_change_data()
        for record in week_change_tab:
            if record[1] == 'META':
                self.assertEqual(record[0], 'Meta Platforms, Inc.')
                self.assertEqual(record[2], -51.61)
                self.assertEqual(record[3], '43.89B')

            if record[1] == 'TSLA':
                self.assertEqual(record[0], 'Tesla, Inc.')
                self.assertEqual(record[2], 9.71)
                self.assertEqual(record[3], '18.01B')

    def test_holds_data(self):
        holds_tab = holds_data()
        for record in holds_tab:
            if record[1] == 'AMZN':
                self.assertEqual(record[0], 'Amazon.com, Inc.')
                self.assertEqual(record[2], '29,143,882')
                self.assertEqual(record[3], 'Mar 30, 2022')
                self.assertEqual(record[4], '5.73%')
                self.assertEqual(record[5], 95007598125)

            if record[1] == 'F':
                self.assertEqual(record[0], 'Ford Motor Company')
                self.assertEqual(record[2], '272,690,686')
                self.assertEqual(record[3], 'Mar 30, 2022')
                self.assertEqual(record[4], '6.91%')
                self.assertEqual(record[5], 3168665740)


if __name__ == '__main__':
    unittest.main()
