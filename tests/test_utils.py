import unittest
from ctproc.utils import (
    clean_sentences, convert_age_to_year, filter_words,
    remove_leading_number, fix_sentence, check_word,
)
from ctproc.skip_crit import SKIP_CRIT


class TestConvertAgeToYear(unittest.TestCase):
    """Age conversion using formats from actual ClinicalTrials.gov XML."""

    def test_years_standard(self):
        self.assertEqual(convert_age_to_year("65", "Years"), 65.0)

    def test_months_pediatric(self):
        # from topic 50: "5 months old male"
        self.assertAlmostEqual(convert_age_to_year("5", "months"), 5 / 12, places=2)

    def test_weeks_neonatal(self):
        # gestational age in weeks
        self.assertAlmostEqual(convert_age_to_year("38", "weeks"), 38 / 52, places=2)

    def test_days_neonatal(self):
        # from topic 39: "3-day-old Asian female infant"
        self.assertAlmostEqual(convert_age_to_year("3", "days"), 3 / 365, places=3)

    def test_none_age(self):
        self.assertIsNone(convert_age_to_year(None, "years"))

    def test_none_units_returns_raw(self):
        # some docs have no unit, just a number
        self.assertEqual(convert_age_to_year("30", None), 30.0)

    def test_6_months(self):
        self.assertAlmostEqual(convert_age_to_year("6", "months"), 0.5)


class TestFilterWords(unittest.TestCase):
    """Filter stop words from real clinical text."""

    def test_removes_stops_from_clinical_text(self):
        # simplified from TREC topic 1 criteria
        result = filter_words("the patient has a history of cancer", {"the", "a", "of", "has"})
        self.assertEqual(result, "patient history cancer")

    def test_empty_remove_set(self):
        result = filter_words("severe lower extremity weakness", set())
        self.assertEqual(result, "severe lower extremity weakness")

    def test_all_removed(self):
        result = filter_words("a the of", {"a", "the", "of"})
        self.assertEqual(result, "")


class TestCheckWord(unittest.TestCase):
    """Test word filtering using patterns from real CT docs."""

    def test_clinical_term_passes(self):
        self.assertTrue(check_word("diabetes"))
        self.assertTrue(check_word("hypertension"))
        self.assertTrue(check_word("carcinoma"))

    def test_all_caps_header_fails(self):
        # from NCT00902733: "DISEASE CHARACTERISTICS:"
        self.assertFalse(check_word("DISEASE"))
        self.assertFalse(check_word("CHARACTERISTICS"))

    def test_criteria_words_fail(self):
        self.assertFalse(check_word("inclusion"))
        self.assertFalse(check_word("exclusion"))
        self.assertFalse(check_word("criteria"))
        self.assertFalse(check_word("include"))
        self.assertFalse(check_word("exclude"))

    def test_short_clinical_abbreviations_pass(self):
        # HIV, MRI, etc are <6 chars, should pass
        self.assertTrue(check_word("HIV"))
        self.assertTrue(check_word("MRI"))
        self.assertTrue(check_word("ECOG"))

    def test_strips_punctuation(self):
        self.assertFalse(check_word("criteria:"))
        self.assertFalse(check_word("exclusion,"))


class TestRemoveLeadingNumber(unittest.TestCase):
    """From real CT docs with numbered criteria."""

    def test_numbered_criterion(self):
        # from NCT02352805: "1. History of previously diagnosed..."
        self.assertEqual(
            remove_leading_number("1. History of previously diagnosed hereditary coagulation"),
            "History of previously diagnosed hereditary coagulation",
        )

    def test_no_number(self):
        self.assertEqual(
            remove_leading_number("Patients with diabetes mellitus"),
            "Patients with diabetes mellitus",
        )

    def test_multi_digit(self):
        # some docs have >9 criteria
        self.assertEqual(remove_leading_number("12. Another criterion"), "Another criterion")


class TestFixSentence(unittest.TestCase):
    """Test sentence cleaning using real CT patterns."""

    def test_removes_criteria_words_from_header(self):
        # from NCT01145885: "Inclusion Criteria 1. Patients with..."
        result = fix_sentence("Inclusion Criteria 1. Patients with confirmed diagnosis")
        self.assertNotIn("Inclusion", result)
        self.assertNotIn("Criteria", result)

    def test_preserves_clinical_text(self):
        result = fix_sentence("Patients with histologically confirmed pancreatic cancer")
        self.assertEqual(result, "Patients with histologically confirmed pancreatic cancer")

    def test_strips_trailing_punctuation(self):
        result = fix_sentence("Eastern Cooperative Oncology Group performance score.,;:")
        self.assertTrue(result.endswith("score"))


class TestCleanSentences(unittest.TestCase):
    """Test using real eligibility criteria patterns."""

    def test_splits_on_dashes(self):
        # standard CT format: "- criterion 1- criterion 2"
        result = clean_sentences(["- Pregnant women- Children under 12"])
        self.assertIn("Pregnant women", result)
        self.assertIn("Children under 12", result)

    def test_removes_skip_crit_filler(self):
        # these are actual filler strings from real CTs
        for skip in SKIP_CRIT:
            result = clean_sentences([skip])
            self.assertEqual(result, [], f"Should have skipped: {skip!r}")

    def test_removes_very_short(self):
        result = clean_sentences(["ab"])
        self.assertEqual(result, [])

    def test_removes_leading_numbers(self):
        # from NCT00387855: "1.Youth who do not speak..."
        result = clean_sentences(["1. English speaking youth with parental consent"])
        self.assertEqual(result, ["English speaking youth with parental consent"])

    def test_preserves_real_criterion(self):
        # real criterion from dataset
        result = clean_sentences(["Patients must be over 18 years of age"])
        self.assertEqual(result, ["Patients must be over 18 years of age"])

    def test_real_ct_criteria_block(self):
        # from NCT01414829 (used in existing test suite)
        sents = [
            "all referred for gastroscopy with clinical or endoscopic signs of peptic disease",
        ]
        result = clean_sentences(sents)
        self.assertEqual(len(result), 1)
        self.assertIn("gastroscopy", result[0])


if __name__ == "__main__":
    unittest.main()
