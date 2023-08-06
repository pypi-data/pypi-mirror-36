import pytest
import unittest

from vpxhw_db_job_locator.dashboard_url import DashboardUrl


class DashboardUrlTest(unittest.TestCase):

  def setUp(self):
    self.dburl=DashboardUrl()

  @pytest.mark.DashboardUrl
  def test_add_single_job_post_query(self):
    self.dburl.add_single_job('d1f3883fe63b01d4b8ba17c9de26a669adeccda0','libvpx_vp9','ml-cpu6','hevc_conformance_suite.txt', 'fctm_gold_model.json')

    self.assertEqual(self.dburl._jobIds, ['eyJjb21taXQiOiAiZDFmMzg4M2ZlNjNiMDFkNGI4YmExN2M5ZGUyNmE2NjlhZGVjY2RhMCIsICJlbmNvZGVyIjogImxpYnZweF92cDkiLCAidXNlY2FzZSI6ICJtbC1jcHU2IiwgInRlc3Rfc3VpdGUiOiAiaGV2Y19jb25mb3JtYW5jZV9zdWl0ZS50eHQiLCAiRlBHQSI6ICIwIiwgImJ1aWxkX29wdGlvbnMiOiAiZmN0bV9nb2xkX21vZGVsLmpzb24iLCAiaWQiOiAiMWU1YTY0NTY4ZTZmNGZkMGE0MjQ4YmJiZmMzYzM0YzMifQ=='])

  @pytest.mark.DashboardUrl
  def test_query_extracts_test_suite_basename_from_path(self):
    self.dburl.add_single_job('d1f3883fe63b01d4b8ba17c9de26a669adeccda0','libvpx_vp9','ml-cpu6','path/to/hevc_conformance_suite.txt', 'fctm_gold_model.json')

    self.assertEqual(self.dburl._jobIds, ['eyJjb21taXQiOiAiZDFmMzg4M2ZlNjNiMDFkNGI4YmExN2M5ZGUyNmE2NjlhZGVjY2RhMCIsICJlbmNvZGVyIjogImxpYnZweF92cDkiLCAidXNlY2FzZSI6ICJtbC1jcHU2IiwgInRlc3Rfc3VpdGUiOiAiaGV2Y19jb25mb3JtYW5jZV9zdWl0ZS50eHQiLCAiRlBHQSI6ICIwIiwgImJ1aWxkX29wdGlvbnMiOiAiZmN0bV9nb2xkX21vZGVsLmpzb24iLCAiaWQiOiAiMWU1YTY0NTY4ZTZmNGZkMGE0MjQ4YmJiZmMzYzM0YzMifQ=='])

  @pytest.mark.DashboardUrl
  def test_get_dashboard_url(self):
    # self.dburl._encoder='ENCODER'
    self.dburl._jobIds=['job_a', 'job_b']
    # self.dburl._model_name='MODEL_NAME'

    expected_output='''http://go/vpxhw-quality?job=job_a&job=job_b\n\n\n'''

    self.assertEqual(self.dburl.get_dashboard_url(), expected_output)