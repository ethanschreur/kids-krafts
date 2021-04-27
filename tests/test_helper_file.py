from unittest import TestCase
import app.helper as helper

class HelperFileTestCase(TestCase):
    def test_get_prev_month(self):
        self.assertEqual(helper.get_prev_month(1), 12)
        self.assertEqual(helper.get_prev_month(2), 1)

    def test_get_next_month(self):
        self.assertEqual(helper.get_next_month(12), 1)
        self.assertEqual(helper.get_next_month(1), 2)

    def test_get_prev_year(self):
        self.assertEqual(helper.get_prev_year(1, 21), (20))
        self.assertEqual(helper.get_prev_year(2, 21), (21))

    def test_get_next_year(self):
        self.assertEqual(helper.get_next_year(12, 21), 22)
        self.assertEqual(helper.get_next_year(1, 21), 21)

    def test_get_two_weeks_options(self):
        self.assertEqual(helper.get_two_weeks_options(4, 21), [{'months': [3, 4], 'range': [[28, 29, 30, 31, 0, 0, 0], [4, 5, 6, 7, 8, 9, 10]], 'years': [21, 21]}, {'months': [4, 5], 'range': [[25, 26, 27, 28, 29, 30, 0], [2, 3, 4, 5, 6, 7, 8]], 'years': [21, 21]}])
        self.assertEqual(helper.get_two_weeks_options(3, 21), [{'months': [2, 3], 'range': [[21, 22, 23, 24, 25, 26, 27], [0, 1, 2, 3, 4, 5, 6]], 'years': [21, 21]}, {'months': [3, 4], 'range': [[28, 29, 30, 31, 0, 0, 0], [4, 5, 6, 7, 8, 9, 10]], 'years': [21, 21]}])
        self.assertEqual(helper.get_two_weeks_options(5, 21), [{'months': [4, 5], 'range': [[25, 26, 27, 28, 29, 30, 0], [2, 3, 4, 5, 6, 7, 8]], 'years': [21, 21]}, {'months': [5, 6], 'range': [[23, 24, 25, 26, 27, 28, 29], [0, 0, 1, 2, 3, 4, 5]], 'years': [21, 21]}])

    def test_whichOption(self):
        two_weeks_options = helper.get_two_weeks_options(4, 21)
        self.assertEqual(helper.whichOption(2, two_weeks_options), 'first')
        self.assertEqual(helper.whichOption(11, two_weeks_options), 'second')

    def test_get_last_week(self):
        two_weeks_options = helper.get_two_weeks_options(4, 21)
        self.assertEqual(helper.get_last_week('first', two_weeks_options), [28, 29, 30, 31, 0, 0, 0])
        self.assertEqual(helper.get_last_week('second', two_weeks_options), [25, 26, 27, 28, 29, 30, 0])

    def test_get_first_week(self):
        two_weeks_options = helper.get_two_weeks_options(4, 21)
        self.assertEqual(helper.get_first_week('first', two_weeks_options), [4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(helper.get_first_week('second', two_weeks_options), [2, 3, 4, 5, 6, 7, 8])

    def test_get_total_month_days(self):
        two_weeks_options = helper.get_two_weeks_options(4, 21)
        self.assertEqual(helper.get_total_month_days('first', two_weeks_options), 31)
        self.assertEqual(helper.get_total_month_days('second', two_weeks_options), 30)

    def test_get_new_last_week(self):
        two_weeks_options = helper.get_two_weeks_options(4, 21)
        last_week = helper.get_last_week('second', two_weeks_options)
        self.assertEqual(helper.get_new_last_week(last_week, 'second', two_weeks_options), [25, 26, 27, 28, 29, 30, 1])
        two_weeks_options = helper.get_two_weeks_options(1, 15)
        self.assertEqual(helper.get_new_last_week([24, 25, 26, 27, 28, 29, 30], 'second', two_weeks_options), [24, 25, 26, 27, 28, 29, 30])

    def test_get_new_first_week(self):
        two_weeks_options = helper.get_two_weeks_options(3, 21)
        first_week = helper.get_first_week('first', two_weeks_options)
        self.assertEqual(helper.get_new_first_week(first_week, 'first', two_weeks_options), [28, 1, 2, 3, 4, 5, 6])

    def test_get_first_month(self):
        self.assertEqual(helper.get_first_month('first', 'March', 'April'), 'March')
        self.assertEqual(helper.get_first_month('second', 'March', 'April'), 'April')

    def test_get_second_month(self):
        self.assertEqual(helper.get_second_month('first', 'April', 'May'), 'April')
        self.assertEqual(helper.get_second_month('second', 'April', 'May'), 'May')

    def test_get_month_header(self):
        prev_month = "March"
        curr_month = "April"
        next_month = "May"
        last_week = [25, 26, 27, 28, 29, 30, 0]
        first_week = [2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(helper.get_month_header('first', prev_month, curr_month, next_month, last_week, first_week), "March 25 - April 8")
        self.assertEqual(helper.get_month_header('second', prev_month, curr_month, next_month, last_week, first_week), "April 25 - May 8") 
