from .types import LabTest, ReferenceRange

# Built from the reference table in ctproc/lab_extractor.py
# and cross-referenced with lab values that actually appear in ClinicalTrials.gov eligibility criteria.
# Aliases reflect how investigators write criteria (abbreviations, alternate names).

LAB_TESTS: dict[str, LabTest] = {}


def _add(name: str, aliases: list[str], si: ReferenceRange | None, conv: ReferenceRange | None,
         default_unit: str = "", demographics: dict[str, ReferenceRange] | None = None) -> None:
    lt = LabTest(
        name=name, aliases=aliases, si_range=si, conventional_range=conv,
        default_unit=default_unit,
        demographic_ranges=demographics or {},
    )
    LAB_TESTS[name.lower()] = lt
    for a in aliases:
        LAB_TESTS[a.lower()] = lt


# --- Hematology ---

_add("Hemoglobin", ["Hb", "Hgb", "HGB"],
     si=ReferenceRange(120, 180, "g/L"),
     conv=ReferenceRange(12.0, 18.0, "g/dL"),
     default_unit="g/dL",
     demographics={
         "males": ReferenceRange(14.0, 18.0, "g/dL"),
         "females": ReferenceRange(12.0, 16.0, "g/dL"),
         "newborn": ReferenceRange(16.5, 19.5, "g/dL"),
         "children": ReferenceRange(11.2, 16.5, "g/dL"),
     })

_add("Hematocrit", ["Hct", "HCT"],
     si=ReferenceRange(0.37, 0.54, ""),
     conv=ReferenceRange(37, 54, "%"),
     default_unit="%",
     demographics={
         "males": ReferenceRange(40, 54, "%"),
         "females": ReferenceRange(37, 47, "%"),
     })

_add("White blood cells", ["WBC", "Leukocytes", "white blood cell count"],
     si=ReferenceRange(3.5, 12.0, "x10^9/L"),
     conv=ReferenceRange(3500, 12000, "/mm3"),
     default_unit="/mm3")

_add("Absolute neutrophil count", ["ANC", "Neutrophils", "Absolute granulocyte count", "AGC"],
     si=ReferenceRange(3.0, 5.8, "x10^9/L"),
     conv=ReferenceRange(1500, 5800, "/mm3"),
     default_unit="/mm3")

_add("Platelet count", ["Platelets", "Plt", "PLT", "Platelet"],
     si=ReferenceRange(150, 400, "x10^9/L"),
     conv=ReferenceRange(150000, 400000, "/mm3"),
     default_unit="/mm3")

_add("Mean corpuscular volume", ["MCV"],
     si=ReferenceRange(76, 100, "fL"),
     conv=ReferenceRange(76, 100, "fL"),
     default_unit="fL")

_add("Lymphocytes", ["ALC", "Absolute lymphocyte count"],
     si=ReferenceRange(1.5, 3.0, "x10^9/L"),
     conv=ReferenceRange(1500, 3000, "/mm3"),
     default_unit="/mm3")

_add("Reticulocytes", [],
     si=ReferenceRange(25, 75, "x10^9/L"),
     conv=ReferenceRange(25000, 75000, "/mm3"),
     default_unit="/mm3")

_add("Sedimentation rate", ["ESR", "Sed rate"],
     si=ReferenceRange(0, 15, "mm/h"),
     conv=ReferenceRange(0, 15, "mm/h"),
     default_unit="mm/h")

# --- Coagulation ---

_add("Prothrombin time", ["PT"],
     si=ReferenceRange(9, 12, "sec"),
     conv=ReferenceRange(9, 12, "sec"),
     default_unit="sec")

_add("INR", ["International normalized ratio"],
     si=ReferenceRange(0.9, 1.1, ""),
     conv=ReferenceRange(0.9, 1.1, ""),
     default_unit="")

_add("Partial thromboplastin time", ["PTT", "aPTT"],
     si=ReferenceRange(25, 40, "sec"),
     conv=ReferenceRange(25, 40, "sec"),
     default_unit="sec")

# --- Hepatic ---

_add("Bilirubin", ["Total bilirubin", "Bilirubin total", "TBIL"],
     si=ReferenceRange(3, 22, "μmol/L"),
     conv=ReferenceRange(0.2, 1.3, "mg/dL"),
     default_unit="mg/dL")

_add("Direct bilirubin", ["Conjugated bilirubin", "DBIL"],
     si=ReferenceRange(0, 5, "μmol/L"),
     conv=ReferenceRange(0, 0.3, "mg/dL"),
     default_unit="mg/dL")

_add("AST", ["SGOT", "Aspartate aminotransferase", "Aspartate transaminase"],
     si=ReferenceRange(7, 40, "IU/L"),
     conv=ReferenceRange(7, 40, "U/L"),
     default_unit="U/L")

_add("ALT", ["SGPT", "Alanine aminotransferase", "Alanine transaminase"],
     si=ReferenceRange(5, 35, "IU/L"),
     conv=ReferenceRange(5, 35, "U/L"),
     default_unit="U/L")

_add("Alkaline phosphatase", ["Alk phos", "ALP", "Alk P"],
     si=ReferenceRange(40, 160, "IU/L"),
     conv=ReferenceRange(40, 160, "U/L"),
     default_unit="U/L")

_add("Albumin", ["Alb"],
     si=ReferenceRange(35, 55, "g/L"),
     conv=ReferenceRange(3.5, 5.5, "g/dL"),
     default_unit="g/dL")

_add("Lactate dehydrogenase", ["LDH"],
     si=ReferenceRange(45, 90, "IU/L"),
     conv=ReferenceRange(45, 90, "U/L"),
     default_unit="U/L")

_add("Total protein", ["Protein"],
     si=ReferenceRange(60, 80, "g/L"),
     conv=ReferenceRange(6.0, 8.0, "g/dL"),
     default_unit="g/dL")

_add("Amylase", [],
     si=ReferenceRange(25, 125, "IU/L"),
     conv=ReferenceRange(25, 125, "U/L"),
     default_unit="U/L")

# --- Renal ---

_add("Creatinine", ["Cr", "SCr", "Serum creatinine"],
     si=ReferenceRange(50, 110, "μmol/L"),
     conv=ReferenceRange(0.6, 1.2, "mg/dL"),
     default_unit="mg/dL")

_add("Creatinine clearance", ["CrCl", "CCr"],
     si=None, conv=None,
     default_unit="mL/min")

_add("BUN", ["Urea nitrogen", "Blood urea nitrogen"],
     si=None,
     conv=ReferenceRange(8, 23, "mg/dL"),
     default_unit="mg/dL")

_add("eGFR", ["GFR", "Estimated glomerular filtration rate", "Glomerular filtration rate"],
     si=None, conv=None,
     default_unit="mL/min")

# --- Electrolytes ---

_add("Sodium", ["Na"],
     si=ReferenceRange(135, 145, "mmol/L"),
     conv=ReferenceRange(135, 145, "mEq/L"),
     default_unit="mEq/L")

_add("Potassium", ["K"],
     si=ReferenceRange(3.5, 5.1, "mmol/L"),
     conv=ReferenceRange(3.5, 5.1, "mEq/L"),
     default_unit="mEq/L")

_add("Calcium", ["Ca"],
     si=ReferenceRange(2.10, 2.50, "mmol/L"),
     conv=ReferenceRange(8.4, 10.6, "mg/dL"),
     default_unit="mg/dL")

_add("Phosphate", ["Phosphorus", "Phos"],
     si=ReferenceRange(1.0, 1.5, "mmol/L"),
     conv=ReferenceRange(3.0, 4.5, "mg/dL"),
     default_unit="mg/dL")

_add("Magnesium", ["Mg"],
     si=ReferenceRange(0.65, 1.05, "mmol/L"),
     conv=ReferenceRange(1.3, 2.1, "mg/dL"),
     default_unit="mg/dL")

_add("Chloride", ["Cl"],
     si=ReferenceRange(96, 106, "mmol/L"),
     conv=ReferenceRange(96, 106, "mEq/L"),
     default_unit="mEq/L")

_add("Bicarbonate", ["HCO3", "CO2"],
     si=ReferenceRange(23, 29, "mmol/L"),
     conv=ReferenceRange(23, 29, "mEq/L"),
     default_unit="mEq/L")

# --- Metabolic ---

_add("Glucose", ["Glc", "FBS", "Fasting blood sugar", "Fasting glucose", "Blood glucose"],
     si=ReferenceRange(3.9, 6.1, "mmol/L"),
     conv=ReferenceRange(70, 110, "mg/dL"),
     default_unit="mg/dL")

_add("Hemoglobin A1c", ["HbA1c", "A1c", "HgbA1c", "Glycosylated hemoglobin", "Glycated hemoglobin"],
     si=None, conv=None,
     default_unit="%")

_add("Cholesterol", ["Total cholesterol"],
     si=ReferenceRange(None, 5.2, "mmol/L"),
     conv=ReferenceRange(None, 200, "mg/dL"),
     default_unit="mg/dL")

_add("LDL", ["LDL cholesterol", "LDL-C", "Low density lipoprotein"],
     si=ReferenceRange(None, 3.4, "mmol/L"),
     conv=ReferenceRange(None, 130, "mg/dL"),
     default_unit="mg/dL")

_add("HDL", ["HDL cholesterol", "HDL-C", "High density lipoprotein"],
     si=ReferenceRange(0.91, None, "mmol/L"),
     conv=ReferenceRange(35, None, "mg/dL"),
     default_unit="mg/dL")

_add("Triglycerides", ["TG", "Trigs"],
     si=ReferenceRange(0.45, 1.71, "mmol/L"),
     conv=ReferenceRange(40, 150, "mg/dL"),
     default_unit="mg/dL")

_add("Uric acid", [],
     si=ReferenceRange(120, 420, "μmol/L"),
     conv=ReferenceRange(2.0, 7.0, "mg/dL"),
     default_unit="mg/dL")

# --- Blood gas ---

_add("pO2", ["PaO2", "Arterial pO2"],
     si=ReferenceRange(80, 100, "mmHg"),
     conv=ReferenceRange(80, 100, "mmHg"),
     default_unit="mmHg")

_add("pCO2", ["PaCO2", "Arterial pCO2"],
     si=ReferenceRange(35, 45, "mmHg"),
     conv=ReferenceRange(35, 45, "mmHg"),
     default_unit="mmHg")

_add("O2 saturation", ["SpO2", "SaO2", "O2 sat", "Oxygen saturation"],
     si=ReferenceRange(94, 99, "%"),
     conv=ReferenceRange(94, 99, "%"),
     default_unit="%")

_add("pH", ["Arterial pH"],
     si=ReferenceRange(7.35, 7.45, ""),
     conv=ReferenceRange(7.35, 7.45, ""),
     default_unit="")

# --- Endocrine ---

_add("TSH", ["Thyroid stimulating hormone"],
     si=ReferenceRange(0.4, 4.8, "mIU/L"),
     conv=ReferenceRange(0.4, 4.8, "mIU/L"),
     default_unit="mIU/L")

_add("Free T4", ["FT4", "Thyroxine free"],
     si=ReferenceRange(13, 27, "pmol/L"),
     conv=ReferenceRange(1.0, 2.1, "ng/dL"),
     default_unit="ng/dL")

_add("PSA", ["Prostate specific antigen"],
     si=ReferenceRange(0, 4.0, "μg/L"),
     conv=ReferenceRange(0, 4.0, "ng/mL"),
     default_unit="ng/mL")

# --- Iron ---

_add("Ferritin", [],
     si=ReferenceRange(20, 200, "μg/L"),
     conv=ReferenceRange(20, 200, "ng/mL"),
     default_unit="ng/mL")

_add("Iron", ["Serum iron", "Fe"],
     si=ReferenceRange(5, 31, "μmol/L"),
     conv=ReferenceRange(28, 175, "μg/dL"),
     default_unit="μg/dL")

_add("TIBC", ["Total iron binding capacity", "Iron binding capacity"],
     si=ReferenceRange(45, 73, "μmol/L"),
     conv=ReferenceRange(250, 410, "μg/dL"),
     default_unit="μg/dL")

# --- Other common in CT eligibility ---

_add("CRP", ["C-reactive protein"],
     si=None, conv=None,
     default_unit="mg/L")

_add("IGF-1", ["Insulin-like growth factor 1", "IGF1"],
     si=None, conv=None,
     default_unit="ng/mL")

_add("Vitamin D", ["25-OH Vitamin D", "Vit D", "25-hydroxyvitamin D"],
     si=None, conv=None,
     default_unit="ng/mL")

_add("PTH", ["Parathyroid hormone"],
     si=ReferenceRange(1.4, 6.8, "pmol/L"),
     conv=ReferenceRange(13.2, 64.1, "pg/mL"),
     default_unit="pg/mL")


def get_lab_test(name: str) -> LabTest | None:
    return LAB_TESTS.get(name.lower())


def get_all_lab_names() -> list[str]:
    seen = set()
    result = []
    for lt in LAB_TESTS.values():
        if lt.name not in seen:
            seen.add(lt.name)
            result.append(lt.name)
    return result
