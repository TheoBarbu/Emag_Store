class TestSuite(unittest.TestCase):

    def test_suite(self):
        tests_to_run = unittest.TestSuite()
        tests_to_run.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(OrderTest),
        ])

        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title="Test Execution Report",
            report_name="Test Results"
        )

        runner.run(tests_to_run)


if __name__ == '__main__':
    unittest.main()
