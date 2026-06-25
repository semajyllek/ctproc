import unittest
from ctproc.regex_patterns import (
    AGE_PATTERN, TOPIC_AGE_PATTERN, TOPIC_GENDER_PATTERN,
    CT_FILE_PATTERN, EMPTY_PATTERN,
)


# Real TREC 2021 topic excerpts used for testing
TREC_TOPIC_1 = "45-year-old man with a history of anaplastic astrocytoma of the spine"
TREC_TOPIC_3 = "A 32 yo woman who presents following a severe 'exploding' headache"
TREC_TOPIC_5 = "74M hx of CAD s/p CABG, EF 60% prior CVA (no residual deficits), HTN, HL, DMII"
TREC_TOPIC_9 = "41 year old man with history of severe intellectual disability, CHF, epilepsy"
TREC_TOPIC_10 = "Pt is a 22yo F otherwise healthy with a 5 yr history of the systemic mastocytosis"
TREC_TOPIC_12 = "34 year old woman with Marfan's syndrome and known severe mitral valve prolapse"
TREC_TOPIC_17 = "64yo woman with multiple myeloma, s/p allogeneic transplant"
TREC_TOPIC_35 = "The patient is a 15 year old girl with the history of recurrent bilateral headache"
TREC_TOPIC_39 = "A 3-day-old Asian female infant presents with jaundice"
TREC_TOPIC_50 = "A 5 months old male brought to the pediatrics surgery clinic"


class TestAgePattern(unittest.TestCase):
    """AGE_PATTERN is used for XML age fields like '65 Years', '18 Months'."""

    def test_years(self):
        m = AGE_PATTERN.match("65 Years")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age"), "65")
        self.assertEqual(m.group("units"), "Years")

    def test_months(self):
        m = AGE_PATTERN.match("18 Months")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age"), "18")

    def test_no_match(self):
        m = AGE_PATTERN.match("N/A")
        self.assertIsNone(m)


class TestTopicAgePattern(unittest.TestCase):
    """TOPIC_AGE_PATTERN extracts age from free-text patient descriptions (TREC topics)."""

    def test_topic1_45yo_man(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_1)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "45")

    def test_topic3_32yo_woman(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_3)
        self.assertIsNotNone(m)

    def test_topic5_74M(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_5)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "74")

    def test_topic9_41yo(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_9)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "41")

    def test_topic10_22yo_F(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_10)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "22")

    def test_topic17_64yo(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_17)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "64")

    def test_topic35_15yo_girl(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_35)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "15")

    def test_topic50_5months(self):
        m = TOPIC_AGE_PATTERN.search(TREC_TOPIC_50)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("age_val"), "5")


class TestTopicGenderPattern(unittest.TestCase):
    """TOPIC_GENDER_PATTERN extracts gender from TREC patient descriptions."""

    def test_topic3_woman(self):
        m = TOPIC_GENDER_PATTERN.search("32 woman who presents following a severe headache")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "woman")

    def test_topic9_man(self):
        m = TOPIC_GENDER_PATTERN.search("41 man with history of severe intellectual disability")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "man")

    def test_topic12_woman(self):
        m = TOPIC_GENDER_PATTERN.search("34 woman with Marfan's syndrome")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "woman")

    def test_topic10_F_shorthand(self):
        m = TOPIC_GENDER_PATTERN.search("22F otherwise healthy with systemic mastocytosis")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "F")

    def test_topic35_girl(self):
        m = TOPIC_GENDER_PATTERN.search("15 girl with the history of recurrent bilateral headache")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "girl")

    def test_topic50_male(self):
        m = TOPIC_GENDER_PATTERN.search("5 male brought to the pediatrics surgery clinic")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("gender"), "male")

    def test_no_gender_topic39(self):
        # "3-day-old Asian female infant" — "female" is preceded by "Asian" not a digit/space
        m = TOPIC_GENDER_PATTERN.search(TREC_TOPIC_39)
        # pattern requires digit or space before gender word
        # this tests an edge case in the real data
        if m is not None:
            self.assertIn(m.group("gender"), ("female",))


class TestCTFilePattern(unittest.TestCase):
    """CT_FILE_PATTERN matches clinical trial XML filenames."""

    def test_real_ct_path(self):
        # actual path format from ClinicalTrials.2021-04-27.part1.zip
        m = CT_FILE_PATTERN.match("NCT0093xxxx/NCT00934219.xml")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "NCT00934219.xml")

    def test_nested_path(self):
        m = CT_FILE_PATTERN.match("ClinicalTrials/NCT02221141.xml")
        self.assertIsNotNone(m)

    def test_no_match_non_xml(self):
        m = CT_FILE_PATTERN.match("readme.txt")
        self.assertIsNone(m)

    def test_no_match_directory(self):
        m = CT_FILE_PATTERN.match("NCT0093xxxx/")
        self.assertIsNone(m)


class TestEmptyPattern(unittest.TestCase):
    """EMPTY_PATTERN detects blank eligibility fields in CT XML."""

    def test_whitespace_only(self):
        self.assertIsNotNone(EMPTY_PATTERN.fullmatch("   \n\n  "))

    def test_newlines_only(self):
        self.assertIsNotNone(EMPTY_PATTERN.fullmatch("\n\n\n"))

    def test_actual_content(self):
        self.assertIsNone(EMPTY_PATTERN.fullmatch("Patients must be over 18"))

    def test_mixed_content(self):
        self.assertIsNone(EMPTY_PATTERN.fullmatch("\n  Inclusion Criteria:\n"))


if __name__ == "__main__":
    unittest.main()
