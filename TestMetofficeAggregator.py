from collections import OrderedDict
import unittest
import json
from MetofficeAggregator import MetofficeAggregator


class TestMetofficeAggregatorTestCase(unittest.TestCase):

    def test_main_returns_a_proper_file(self):
        expected = {'country': 'England',
                    'name': 'London Heathrow',
                    'observations':
                        [
                            {
                                'day': '2019-04-23',
                                'temperature': '17.49',
                                'visibility': '24428.57',
                                'wind_direction': 'ENE',
                                'wind_speed': '6.21'
                            },
                            {
                                'day': '2019-04-24',
                                'temperature': '13.02',
                                'visibility': '8827.27',
                                'wind_direction': 'E',
                                'wind_speed': '4.82'
                            }
                        ]
                    }

        with open('metoffice_response_for_testing.json', 'r') as fp:
            raw_data = json.load(fp, object_pairs_hook=OrderedDict)
            MetofficeAggregator.main(raw_data)
            with open('metoffice_report.json', 'r') as report:
                result = json.load(report)
                self.assertEqual(result, expected)

    def test_raises_exception_if_invalid_input(self):
        expected = "invalid input"
        self.assertEqual(MetofficeAggregator.main("dvxvfsdgagv"), expected)
        self.assertEqual(MetofficeAggregator.main(1), expected)
        self.assertEqual(MetofficeAggregator.main(None), expected)

