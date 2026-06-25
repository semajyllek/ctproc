import unittest
from pathlib import Path
from ctproc.ctconfig import CTConfig


class TestCTConfig(unittest.TestCase):

    def test_minimal_creation(self):
        cfg = CTConfig(data_path=Path("test.zip"))
        self.assertEqual(cfg.data_path, Path("test.zip"))

    def test_defaults(self):
        cfg = CTConfig(data_path="test.zip")
        self.assertFalse(cfg.nlp)
        self.assertEqual(cfg.max_trials, 1e7)
        self.assertEqual(cfg.start, -1)
        self.assertIsNone(cfg.get_only)
        self.assertEqual(cfg.skip_ids, set())
        self.assertFalse(cfg.remove_stops)
        self.assertTrue(cfg.add_ents)
        self.assertEqual(cfg.max_aliases, 2)
        self.assertFalse(cfg.expand)
        self.assertFalse(cfg.concat)
        self.assertFalse(cfg.is_topic)
        self.assertEqual(cfg.trec_or_kz, "trec")

    def test_nlp_config(self):
        cfg = CTConfig(data_path="test.zip", nlp=True, expand=True, remove_stops=True)
        self.assertTrue(cfg.nlp)
        self.assertTrue(cfg.expand)
        self.assertTrue(cfg.remove_stops)

    def test_topic_config(self):
        cfg = CTConfig(data_path="topics.xml", is_topic=True, trec_or_kz="kz")
        self.assertTrue(cfg.is_topic)
        self.assertEqual(cfg.trec_or_kz, "kz")

    def test_get_only_filter(self):
        ids = {"NCT001", "NCT002"}
        cfg = CTConfig(data_path="test.zip", get_only=ids)
        self.assertEqual(cfg.get_only, ids)

    def test_skip_ids(self):
        cfg = CTConfig(data_path="test.zip", skip_ids={"NCT00154479"})
        self.assertIn("NCT00154479", cfg.skip_ids)

    def test_is_namedtuple(self):
        cfg = CTConfig(data_path="test.zip")
        self.assertIsInstance(cfg, tuple)
        self.assertTrue(hasattr(cfg, '_fields'))
        self.assertIn('data_path', cfg._fields)


if __name__ == "__main__":
    unittest.main()
