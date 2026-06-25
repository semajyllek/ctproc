"""
Tests using real clinical text from ClinicalTrials.gov eligibility criteria
and TREC 2021 patient descriptions.

ctproc.lab extracts lab values (analyte + value + unit) from any clinical text.
It skips comparator words as noise — comparator interpretation is ctproc's job.
"""
import unittest
from ctproc.lab import extract_lab_values


class TestLabReportFormat(unittest.TestCase):
    """Lab report style: "Analyte: value unit" — from TREC patient descriptions."""

    def test_a1c(self):
        # TREC topic 29: "A1c: 11.3%"
        vals = extract_lab_values("A1c: 11.3%")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Hemoglobin A1c")
        self.assertEqual(vals[0].value, 11.3)

    def test_creatinine(self):
        # TREC topic 29: "Creatinine: 0.9 mg/dL"
        vals = extract_lab_values("Creatinine: 0.9 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Creatinine")
        self.assertEqual(vals[0].value, 0.9)
        self.assertEqual(vals[0].unit, "mg/dL")

    def test_tsh(self):
        # TREC topic 30: "TSH: 2.35 mU/L"
        vals = extract_lab_values("TSH: 2.35 mU/L")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "TSH")
        self.assertEqual(vals[0].value, 2.35)

    def test_psa(self):
        # TREC topic 24: "PSA level: 3.2 ng/mL"
        vals = extract_lab_values("PSA level: 3.2 ng/mL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "PSA")
        self.assertEqual(vals[0].value, 3.2)

    def test_vitamin_d(self):
        # TREC topic 53: "Vit D: 14ng/ml"
        vals = extract_lab_values("Vit D: 14ng/ml")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Vitamin D")
        self.assertEqual(vals[0].value, 14.0)

    def test_hemoglobin(self):
        # TREC topic 45: "Hgb: 8 g/dl"
        vals = extract_lab_values("Hgb: 8 g/dl")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Hemoglobin")
        self.assertEqual(vals[0].value, 8.0)

    def test_direct_bilirubin(self):
        # TREC topic 32: "direct bilirubin: 2.4 mg/dL"
        vals = extract_lab_values("direct bilirubin: 2.4 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Direct bilirubin")
        self.assertEqual(vals[0].value, 2.4)

    def test_ldh(self):
        # TREC topic 32: "LDH: 881 IU/L"
        vals = extract_lab_values("LDH: 881 IU/L")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Lactate dehydrogenase")
        self.assertEqual(vals[0].value, 881.0)

    def test_ldh_with_full_name_and_abbreviation(self):
        # TREC topic 32: "lactate dehydrogenase (LDH): 881 IU/L"
        vals = extract_lab_values("lactate dehydrogenase (LDH): 881 IU/L")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 881.0)

    def test_creatinine_high_value(self):
        # TREC topic 32: "Creatinine: 3.6 mg/dL"
        vals = extract_lab_values("Creatinine: 3.6 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 3.6)


class TestEligibilityCriteriaFormat(unittest.TestCase):
    """
    Eligibility criteria style: "Analyte at least/greater than value unit"
    ctproc.lab extracts the value, skipping the comparator words.
    ctproc would separately parse the comparator meaning.
    """

    def test_hemoglobin_at_least(self):
        vals = extract_lab_values("Hemoglobin at least 9 g/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Hemoglobin")
        self.assertEqual(vals[0].value, 9.0)
        self.assertEqual(vals[0].unit, "g/dL")

    def test_hemoglobin_greater_than(self):
        vals = extract_lab_values("Hemoglobin greater than 10 g/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 10.0)

    def test_hemoglobin_gte_symbol(self):
        vals = extract_lab_values("Hemoglobin >= 10 g/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 10.0)

    def test_hgb_abbreviation(self):
        vals = extract_lab_values("Hgb at least 10 g/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Hemoglobin")

    def test_wbc_with_comma(self):
        # "WBC at least 3,500/mm3"
        vals = extract_lab_values("WBC at least 3,500/mm3")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "White blood cells")
        self.assertEqual(vals[0].value, 3500.0)

    def test_platelet_count_at_least(self):
        # "Platelet count at least 100,000/mm3"
        vals = extract_lab_values("Platelet count at least 100,000/mm3")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Platelet count")
        self.assertEqual(vals[0].value, 100000.0)

    def test_platelets_greater_than(self):
        vals = extract_lab_values("Platelets greater than 100,000")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 100000.0)

    def test_anc_at_least(self):
        vals = extract_lab_values("Absolute neutrophil count at least 1,500/mm3")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Absolute neutrophil count")
        self.assertEqual(vals[0].value, 1500.0)

    def test_anc_abbreviation(self):
        vals = extract_lab_values("ANC at least 1,500")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Absolute neutrophil count")

    def test_hematocrit_greater_than(self):
        vals = extract_lab_values("Hematocrit greater than 30%")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 30.0)

    def test_bilirubin_less_than(self):
        vals = extract_lab_values("Bilirubin less than 1.5 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Bilirubin")
        self.assertEqual(vals[0].value, 1.5)

    def test_bilirubin_no_greater_than(self):
        vals = extract_lab_values("Bilirubin no greater than 1.0 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 1.0)

    def test_creatinine_less_than(self):
        vals = extract_lab_values("Creatinine less than 1.5 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 1.5)

    def test_creatinine_no_greater_than(self):
        vals = extract_lab_values("Creatinine no greater than 1.5 mg/dL")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 1.5)

    def test_creatinine_clearance(self):
        vals = extract_lab_values("Creatinine clearance greater than 70 mL/min")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Creatinine clearance")
        self.assertEqual(vals[0].value, 70.0)

    def test_bun_less_than(self):
        vals = extract_lab_values("BUN less than 40")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "BUN")
        self.assertEqual(vals[0].value, 40.0)


class TestULNPattern(unittest.TestCase):
    """'X times upper limit of normal' — common in hepatic criteria."""

    def test_ast_uln(self):
        vals = extract_lab_values("AST less than 2 times ULN")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "AST")
        self.assertEqual(vals[0].value, 2.0)
        self.assertEqual(vals[0].unit, "x ULN")

    def test_sgot_uln(self):
        vals = extract_lab_values("SGOT no greater than 2.5 times upper limit of normal")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "AST")
        self.assertEqual(vals[0].value, 2.5)
        self.assertEqual(vals[0].unit, "x ULN")

    def test_alt_uln(self):
        vals = extract_lab_values("ALT less than 2 times ULN")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "ALT")

    def test_sgpt_uln(self):
        vals = extract_lab_values("SGPT less than 2.5 times upper limit of normal")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "ALT")

    def test_alkaline_phosphatase_uln(self):
        vals = extract_lab_values("Alkaline phosphatase less than 2 times ULN")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].analyte, "Alkaline phosphatase")

    def test_bilirubin_uln(self):
        vals = extract_lab_values("Bilirubin less than 1.5 times upper limit of normal")
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].value, 1.5)
        self.assertEqual(vals[0].unit, "x ULN")


class TestMultipleValues(unittest.TestCase):
    """Extract multiple lab values from a single text block."""

    def test_hematologic_block(self):
        text = (
            "WBC at least 3,500/mm3 "
            "Platelet count at least 100,000/mm3 "
            "Hemoglobin at least 9 g/dL"
        )
        vals = extract_lab_values(text)
        analytes = {v.analyte for v in vals}
        self.assertIn("White blood cells", analytes)
        self.assertIn("Platelet count", analytes)
        self.assertIn("Hemoglobin", analytes)

    def test_hepatic_renal_block(self):
        text = "Bilirubin less than 1.5 mg/dL Creatinine less than 1.5 mg/dL"
        vals = extract_lab_values(text)
        self.assertEqual(len(vals), 2)
        analytes = {v.analyte for v in vals}
        self.assertIn("Bilirubin", analytes)
        self.assertIn("Creatinine", analytes)

    def test_trec_topic_lab_panel(self):
        # from TREC topic 29 lab results section
        text = "A1c: 11.3% Creatinine: 0.9 mg/dL AST: 17 U/L ALT: 14 U/L"
        vals = extract_lab_values(text)
        analytes = {v.analyte for v in vals}
        self.assertIn("Hemoglobin A1c", analytes)
        self.assertIn("Creatinine", analytes)
        self.assertIn("AST", analytes)
        self.assertIn("ALT", analytes)

    def test_trec_topic_32_panel(self):
        # from TREC topic 32
        text = "Hemoglobin: 9.7 g/dL Platelet: 110,000 /cu.mm Creatinine: 3.6 mg/dL"
        vals = extract_lab_values(text)
        self.assertGreaterEqual(len(vals), 2)
        analytes = {v.analyte for v in vals}
        self.assertIn("Hemoglobin", analytes)
        self.assertIn("Creatinine", analytes)


class TestReferenceRanges(unittest.TestCase):

    def test_known_labs_exist(self):
        from ctproc.lab import get_lab_test
        for name in ["Hemoglobin", "Creatinine", "Platelet count", "AST", "ALT",
                      "Bilirubin", "WBC", "BUN", "ANC", "INR"]:
            self.assertIsNotNone(get_lab_test(name), f"Missing: {name}")

    def test_aliases_resolve(self):
        from ctproc.lab import get_lab_test
        for alias, expected in [("Hgb", "Hemoglobin"), ("SGOT", "AST"), ("SGPT", "ALT"),
                                 ("Plt", "Platelet count"), ("Na", "Sodium"), ("K", "Potassium"),
                                 ("Cr", "Creatinine"), ("HbA1c", "Hemoglobin A1c")]:
            lt = get_lab_test(alias)
            self.assertIsNotNone(lt, f"Alias not found: {alias}")
            self.assertEqual(lt.name, expected)

    def test_all_lab_names_count(self):
        from ctproc.lab import get_all_lab_names
        names = get_all_lab_names()
        self.assertGreater(len(names), 40)

    def test_hemoglobin_demographics(self):
        from ctproc.lab import get_lab_test
        hgb = get_lab_test("Hemoglobin")
        self.assertIn("males", hgb.demographic_ranges)
        self.assertIn("females", hgb.demographic_ranges)
        self.assertEqual(hgb.demographic_ranges["males"].high, 18.0)
        self.assertEqual(hgb.demographic_ranges["females"].low, 12.0)


class TestPositionTracking(unittest.TestCase):
    """Verify start/end positions point to the right span."""

    def test_position_in_simple_text(self):
        text = "Patient Hemoglobin: 9.2 g/dL today"
        vals = extract_lab_values(text)
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0].start, 8)  # "Hemoglobin" starts at index 8
        self.assertGreater(vals[0].end, vals[0].start)

    def test_raw_text_contains_analyte(self):
        vals = extract_lab_values("Creatinine: 1.5 mg/dL")
        self.assertIn("Creatinine", vals[0].raw_text)


class TestEdgeCases(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(extract_lab_values(""), [])

    def test_no_lab_values(self):
        self.assertEqual(extract_lab_values("Patient must be over 18 years of age"), [])

    def test_analyte_without_value(self):
        vals = extract_lab_values("History of elevated Creatinine")
        self.assertEqual(len(vals), 0)

    def test_analyte_in_word_not_matched(self):
        # "AST" should not match inside "at leAST" or similar
        vals = extract_lab_values("at least 5 years since prior radiotherapy")
        self.assertEqual(len(vals), 0)


if __name__ == "__main__":
    unittest.main()
