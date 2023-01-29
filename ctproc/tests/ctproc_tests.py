import logging 

import unittest
from pathlib import Path
from ctproc.ctconfig import CTConfig
from ctproc.proc import CTProc, CTDocument, EligCrit
from ctproc.eligibility import process_eligibility_naive


#-------------------------------------------------------------------------------------------#
# 1. "normal" criteria statements with dashes and clear semi-structure
# ------------------------------------------------------------------------------------------#


normal_raw   =  """
                    Inclusion Criteria:
                         -  Patients with HF or IHD who are not currently taking the study medications of
                            interest (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD) and
                            whose primary care physicians are part of the study population
                    Exclusion Criteria:
                        -  Patients who are unable or unwilling to give informed consent,
                        -  previously taken the study medications according to dispensing records
                        -  allergy or intolerance to study medications
                        -  residents of long-term care facilities
                        -  unable to confirm a diagnosis of either HF or IHD
                        -  primary care physician has already contributed 5 patients to the study
                  """

norm_inc_crit = [
  "Patients with HF or IHD who are not currently taking the study medications of interest" \
  + " (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD)" \
  + " and whose primary care physicians are part of the study population"
]


norm_exc_crit = [
  'Patients who are unable or unwilling to give informed consent', 
  'previously taken the study medications according to dispensing records', 
  'allergy or intolerance to study medications', 
  'residents of long-term care facilities', 
  'unable to confirm a diagnosis of either HF or IHD', 
  'primary care physician has already contributed 5 patients to the study'
]






#-------------------------------------------------------------------------------------------#
# 2. raw text contains only inclusion criteria (uses norm_inc_crit above)
# ------------------------------------------------------------------------------------------#

inc_only_raw  =  """
                    Inclusion Criteria:
                         -  Patients with HF or IHD who are not currently taking the study medications of
                            interest (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD) and
                            whose primary care physicians are part of the study population
                  """




#-------------------------------------------------------------------------------------------#
# 3. raw text contains only exclusion criteria (uses norm_exc_crit above)
# ------------------------------------------------------------------------------------------#


exc_only_raw   =  """
                  Exclusion Criteria:
                      -  Patients who are unable or unwilling to give informed consent,
                      -  previously taken the study medications according to dispensing records
                      -  allergy or intolerance to study medications
                      -  residents of long-term care facilities
                      -  unable to confirm a diagnosis of either HF or IHD
                      -  primary care physician has already contributed 5 patients to the study
                """


#---------------------------------------------------------------------------#
# 5. test 5 is on the empty raw text field
# --------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
# 5. spaced with dashes variation (from NCT01414829)
# --------------------------------------------------------------------------#

normal_spaced_raw  =  """
          Inclusion Criteria:

          -  all referred for gastroscopy with clinical or endoscopic signs of peptic disease

        Exclusion Criteria:

          -  coagulation disorders

          -  pregnant women

"""

norm_spaced_inc_crit = [
  'all referred for gastroscopy with clinical or endoscopic signs of peptic disease'
]

norm_spaced_exc_crit = [
  'coagulation disorders',
  'pregnant women'
]



#---------------------------------------------------------------------------#
# 6. spaced with no dashes variation (artificially from NCT01414829)
# --------------------------------------------------------------------------#


normal_no_dash_raw   =  """
                
          Inclusion Criteria:

           all referred for gastroscopy with clinical or endoscopic signs of peptic disease

        Exclusion Criteria:

           coagulation disorders

           pregnant women
""" 


norm_no_dash_inc_crit = [
  'all referred for gastroscopy with clinical or endoscopic signs of peptic disease'
]

norm_no_dash_exc_crit = [
  'coagulation disorders',
  'pregnant women'
]



#-----------------------------------------------------------------------------------------#
# 7. numbered subcriteria variation (slightly modified for tighter testing from NCT01414829)
# - also skips last semantically empty criteria with hacky code
# ----------------------------------------------------------------------------------------#



sub_numbers_raw = """
        Inclusion Criteria:

          -  History of liver steatosis during the preceding 24 months

          -  History of fasting TGs > 200 mg/dL (confirmed at screening).

          -  Liver fat ≥ 10% as determined by the central MRI laboratory.

          -  Subjects on the following medications can be included if these medications are
             medically necessary, cannot be stopped and the investigator feels their dose will
             remain stable for the duration of the double-blind treatment period:

               1. Stable dose of anti-diabetic medications (metformin and/or sulfonylureas) for at
                  least 8 weeks prior to screening.

               2. Stable doses of beta-blockers and thiazide diuretics for at least 8 weeks prior
                  to screening.
 

        Exclusion Criteria:

          -  Treatment with omega-3-acid ethyl esters or omega-3-polyunsaturated fatty acid
             (PUFA)-containing supplements > 200 mg per day within 8 weeks of screening.

          -  Treatment with antiretrovirals, tamoxifen, methotrexate, cyclophosphamide,
             isotretinoin, bile acid binding resins or pharmacologic doses of oral glucocorticoids
             (≥10 mg of prednisone per day or equivalent) within 8 weeks of screening.

        Other protocol defined inclusion/exclusion criteria may apply
      
"""

sub_numbers_inc_crit = [
  'History of liver steatosis during the preceding 24 months',
  'History of fasting TGs > 200 mg/dL (confirmed at screening)',
  'Liver fat ≥ 10% as determined by the central MRI laboratory',
  'Subjects on the following medications can be included if these medications are medically necessary, cannot be stopped and the investigator feels their dose will remain stable for the duration of the double-blind treatment period',
  'Stable dose of anti-diabetic medications (metformin and/or sulfonylureas) for at least 8 weeks prior to screening',
  'Stable doses of beta-blockers and thiazide diuretics for at least 8 weeks prior to screening'
]

sub_numbers_exc_crit = [
  'Treatment with omega-3-acid ethyl esters or omega-3-polyunsaturated fatty acid (PUFA)-containing supplements > 200 mg per day within 8 weeks of screening',
  'Treatment with antiretrovirals, tamoxifen, methotrexate, cyclophosphamide, isotretinoin, bile acid binding resins or pharmacologic doses of oral glucocorticoids (≥10 mg of prednisone per day or equivalent) within 8 weeks of screening'
]






#-----------------------------------------------------------------------------------------#
# 8. all caps headers variation (from NCT00902733)
# ----------------------------------------------------------------------------------------#

headers_raw = """
        DISEASE CHARACTERISTICS:

          -  Diagnosis of pancreatic cancer (all stages)

        PATIENT CHARACTERISTICS:

          -  Admitted to City of Hope National Medical Center

               -  Resides within a 30-mile radius of the medical center

          -  No prior cancer

        PRIOR CONCURRENT THERAPY:

          -  No prior therapy
      
"""

headers_inc_crit = [
  'Diagnosis of pancreatic cancer (all stages)',
  'Admitted to City of Hope National Medical Center',
  'Resides within a 30-mile radius of the medical center',
  'No prior cancer',
  'No prior therapy'
]

headers_exc_crit = []






#-----------------------------------------------------------------------------------------#
# 9. no dash + sub numbering in exclusion criteria (from NCT02352805)
# ----------------------------------------------------------------------------------------#

no_dash_sub_numbers_raw = """
       Inclusion Criteria:

        Need for therapy with extracorporeal circulation / circulatory support due to cardiac
        failure, or lung failure, or renal failure, or a combination of these diseases

        Exclusion Criteria:

          1. History of previously diagnosed hereditary coagulation and/or platelet disorders

          2. Refusal to receive blood transfusion

          3. Participation in other clinical research studies involving evaluation of other
             investigational drugs or devices within 30 days of randomization

          4. Diagnosis of hepatitis B, hepatitis C, and HIV

          5. Age > 85 years
      
"""

no_dash_sub_numbers_inc_crit = [
  'Need for therapy with extracorporeal circulation / circulatory support due to cardiac failure, or lung failure, or renal failure, or a combination of these diseases'
]

no_dash_sub_numbers_exc_crit = [
  'History of previously diagnosed hereditary coagulation and/or platelet disorders',
  'Refusal to receive blood transfusion',
  'Participation in other clinical research studies involving evaluation of other investigational drugs or devices within 30 days of randomization',
  'Diagnosis of hepatitis B, hepatitis C, and HIV',
  'Age > 85 years'   
]





#-------------------------------------------------------------------------------------------#
# 10. individually labelled criteria (from NCT01145885) 
# - note how the word Criteria gets wrongly removed from the words in 'Inclusion Criteria 6' 
# ------------------------------------------------------------------------------------------#


indv_label_raw = """
       Inclusion criteria:

          -  Inclusion Criteria 1. Patients with histologically or cytologically confirmed
             diagnosis of advanced, non resectable and / or metastatic solid tumour

          -  Inclusion Criteria 2. Male

          -  Inclusion Criteria 3. Age >=18 and =<70 years

          -  Inclusion Criteria 4. Written informed consent

          -  Inclusion Criteria 5. Eastern Cooperative Oncology Group (ECOG) performance score =<2

          -  Inclusion Criteria 6. Recovery from Common Terminology Criteria for Adverse Events
             (CTCAE) Grade >=2 therapy-related toxicities from previous chemo-, hormone-, immuno-,
             or radiotherapy

        Exclusion criteria:

          -  Exclusion Criteria 1. Serious concomitant non-oncological disease considered by the
             investigator

          -  Exclusion Criteria 2. Active infectious disease

          -  Exclusion Criteria 3. Viral hepatitis, Human Immunodeficiency Virus (HIV) infection

"""

indv_label_inc_crit = [
  'Patients with histologically or cytologically confirmed diagnosis of advanced, non resectable and / or metastatic solid tumour',
  'Male',
  'Age >=18 and =<70 years',
  'Written informed consent',
  'Eastern Cooperative Oncology Group (ECOG) performance score =<2',
  'Recovery from Common Terminology for Adverse Events (CTCAE) Grade >=2 therapy-related toxicities from previous chemo-, hormone-, immuno-, or radiotherapy'
]


indv_label_exc_crit = [
  'Serious concomitant non-oncological disease considered by the investigator',
  'Active infectious disease',
  'Viral hepatitis, Human Immunodeficiency Virus (HIV) infection'
]




#-------------------------------------------------------------------------------------------#
# 11. dash and all caps header like 
# - INCLUSION CRITERIA:
#    ...
# (from NCT00362167) 
# ------------------------------------------------------------------------------------------#


dash_and_header_raw = """
        -  INCLUSION CRITERIA:

        Patients of 4 years of age and older, both genders, and all racial/ethnic groups with
        acute or chronic pain that will help the Branch fulfill its objectives.

        Women of childbearing potential, or who are pregnant or lactating, will only undergo tests
        and procedures, and/or receive medications for which data exists proving minimal risk to
        the fetus. The diagnostic tests will only include medically-indicated radiation exposure.

        Referral is needed from the patients' physician or dentist.

        EXCLUSION CRITERIA:

        Patients with significant cognitive impairment.

        Pregnancy or lactation, if this status precludes proposed diagnostic procedures or
        therapies.

        Patients with serious organ system dysfunction (e.g. heart failure, ischemic heart
        disease).
      
"""


dash_and_header_inc_crit = [
  'Patients of 4 years of age and older, both genders, and all racial/ethnic groups with acute or chronic pain that will help the Branch fulfill its objectives',
  'Women of childbearing potential, or who are pregnant or lactating, will only undergo tests and procedures, and/or receive medications for which data exists proving minimal risk to the fetus. The diagnostic tests will only medically-indicated radiation exposure',
  "Referral is needed from the patients' physician or dentist"
]

dash_and_header_exc_crit = [
  'Patients with significant cognitive impairment',
  'Pregnancy or lactation, if this status precludes proposed diagnostic procedures or therapies',
  'Patients with serious organ system dysfunction (e.g. heart failure, ischemic heart disease)' 
]



#-------------------------------------------------------------------------------------------#
# 12. include statement contains an exclude statement. 
#     this is problematic because the current program removes these words,
#     note the erroneous change:
#     'Exclusion of differential diagnoses' -> 'of differential diagnoses'
#  (from NCT02196155)
# ------------------------------------------------------------------------------------------#

exc_in_inc_raw = """
        Inclusion Criteria:

          -  Exclusion of differential diagnoses

          -  Written informed consent

        Exclusion Criteria

          -  Active differential diagnoses

          -  Neurological diseases affecting the peripheral nervous system
      
"""

exc_in_inc_inc_crit = [
  'of differential diagnoses',
  'Written informed consent'
]

exc_in_inc_exc_crit = [
  'Active differential diagnoses',
  'Neurological diseases affecting the peripheral nervous system'
]


#-------------------------------------------------------------------------------------------#
# 13. numbered criteria with no spaces (from NCT00387855)
# ------------------------------------------------------------------------------------------#

num_no_space_raw = """
        Inclusion Criteria:

          1. Attendance at school participating in study

          2. English speaking youth with parental consent.

        Exclusion Criteria:

        1.Youth who do not speak and read English
      
"""

num_no_space_inc_crit = [
  'Attendance at school participating in study',
  'English speaking youth with parental consent'
]

num_no_space_exc_crit = [
  'Youth who do not speak and read English'
]







#--------------------------------------------------------------------------------------------------#
# test document
#--------------------------------------------------------------------------------------------------#

"""
<clinical_study rank="31715">
  <!-- This xml conforms to an XML Schema at:
    https://clinicaltrials.gov/ct2/html/images/info/public.xsd
 and an XML DTD at:
    https://clinicaltrials.gov/ct2/html/images/info/public.dtd -->
  <required_header>
    <download_date>ClinicalTrials.gov processed this data on December 16, 2015</download_date>
    <link_text>Link to the current ClinicalTrials.gov record.</link_text>
    <url>https://clinicaltrials.gov/show/NCT02221141</url>
  </required_header>
  <id_info>
    <org_study_id>Fabry Disease Cardioscreening</org_study_id>
    <nct_id>NCT02221141</nct_id>
  </id_info>
  <brief_title>Screening of Fabry Disease in Patients With Left Ventricular Hypertrophy Detected in Echocardiography</brief_title>
  <sponsors>
    <lead_sponsor>
      <agency>Laurence Gabriel</agency>
      <agency_class>Other</agency_class>
    </lead_sponsor>
  </sponsors>
  <source>Centre Hospitalier Universitaire Dinant Godinne - UCL Namur</source>
  <oversight_info>
    <authority>Belgium: Federal Agency for Medicines and Health Products, FAMHP</authority>
  </oversight_info>
  <brief_summary>
    <textblock>
      The purpose of this study is to determine the prevalence in Belgium of Fabry disease in
      patients with unexplained hypertrophic cardiomyopathy measured by echocardiography and to
      determine in Fabry patients which was the most frequently initial symptom.

      Actually the early diagnosis is important because a treatment exists that can prevent future
      complications.
    </textblock>
  </brief_summary>
  <overall_status>Recruiting</overall_status>
  <start_date>December 2013</start_date>
  <primary_completion_date type="Anticipated">December 2016</primary_completion_date>
  <phase>N/A</phase>
  <study_type>Observational</study_type>
  <study_design>Observational Model: Cohort</study_design>
  <primary_outcome>
    <measure>Percentage of patients with left ventricular hypertrophy who have Fabry Disease mutation</measure>
    <time_frame>1 day</time_frame>
    <safety_issue>No</safety_issue>
  </primary_outcome>
  <number_of_groups>1</number_of_groups>
  <enrollment type="Anticipated">300</enrollment>
  <condition>Left Ventricular Hypertrophy</condition>
  <eligibility>
    <study_pop>
      <textblock>
        Patients with left ventricular hypertrophy
      </textblock>
    </study_pop>
    <sampling_method>Probability Sample</sampling_method>
    <criteria>
      <textblock>
        Inclusion Criteria:

          -  unexplained left ventricular hypertrophy

        Exclusion Criteria:

          -  isolated septal hypertrophy
      </textblock>
    </criteria>
    <gender>Both</gender>
    <minimum_age>18 Years</minimum_age>
    <maximum_age>N/A</maximum_age>
    <healthy_volunteers>No</healthy_volunteers>
  </eligibility>
  <overall_contact>
    <last_name>Laurence Gabriel</last_name>
    <phone>+32 81 42 21 11</phone>
    <phone_ext>3623</phone_ext>
    <email>laurence.gabriel@uclouvain.be</email>
  </overall_contact>
  <overall_contact_backup>
    <last_name>Karine Jourdan</last_name>
    <phone>+32 81 42 21 11</phone>
    <phone_ext>3610</phone_ext>
    <email>karine.jourdan@uclouvain.be</email>
  </overall_contact_backup>
  <location>
    <facility>
      <name>CHU Dinant-Godinne</name>
      <address>
        <city>Yvoir</city>
        <zip>5530</zip>
        <country>Belgium</country>
      </address>
    </facility>
    <status>Recruiting</status>
    <investigator>
      <last_name>Laurence Gabriel</last_name>
      <role>Principal Investigator</role>
    </investigator>
  </location>
  <location_countries>
    <country>Belgium</country>
  </location_countries>
  <verification_date>July 2015</verification_date>
  <lastchanged_date>July 28, 2015</lastchanged_date>
  <firstreceived_date>August 18, 2014</firstreceived_date>
  <responsible_party>
    <responsible_party_type>Sponsor-Investigator</responsible_party_type>
    <investigator_affiliation>Centre Hospitalier Universitaire Dinant Godinne - UCL Namur</investigator_affiliation>
    <investigator_full_name>Laurence Gabriel</investigator_full_name>
    <investigator_title>Dr Laurence GABRIEL</investigator_title>
  </responsible_party>
  <is_fda_regulated>No</is_fda_regulated>
  <has_expanded_access>No</has_expanded_access>
  <condition_browse>
    <!-- CAUTION:  The following MeSH terms are assigned with an imperfect algorithm  -->
    <mesh_term>Hypertrophy</mesh_term>
    <mesh_term>Hypertrophy, Left Ventricular</mesh_term>
  </condition_browse>
  <!-- Results have not yet been posted for this study                                -->
</clinical_study>

"""

test_elig_crit = EligCrit("\n        Inclusion Criteria:\n\n          -  unexplained left ventricular hypertrophy\n\n        Exclusion Criteria:\n\n          -  isolated septal hypertrophy\n      ")
test_elig_crit.include_criteria = ['unexplained left ventricular hypertrophy']
test_elig_crit.exclude_criteria = ['isolated septal hypertrophy']

test_doc = CTDocument('NCT02221141')
test_doc.condition = ['Left Ventricular Hypertrophy']
test_doc.elig_crit = test_elig_crit
test_doc.elig_gender = 'All'
test_doc.elig_min_age: 18.0
test_doc.inc_filtered = ['unexplained left ventricular hypertrophy']
test_doc.exc_filtered = ['isolated septal hypertrophy']
test_doc.inc_ents = [[{'raw_text': 'unexplained', 'label': 'ENTITY', 'start': 0, 'end': 11, 'cui': {'val': 'C4288071', 'score': 0.9999999403953552}, 'alias_expansion': ['Unexplained'], 'negation': False}, {'raw_text': 'left ventricular hypertrophy', 'label': 'ENTITY', 'start': 12, 'end': 40, 'cui': {'val': 'C0149721', 'score': 1.0}, 'alias_expansion': ['lv hypertrophy', 'Enlarged left ventricle'], 'negation': False}]]
test_doc.exc_ents = [[{'raw_text': 'isolated', 'label': 'ENTITY', 'start': 0, 'end': 8, 'cui': {'val': 'C0205409', 'score': 1.0}, 'alias_expansion': ['Isolated', 'isolated'], 'negation': False}, {'raw_text': 'septal hypertrophy', 'label': 'ENTITY', 'start': 9, 'end': 27, 'cui': {'val': 'C0442887', 'score': 1.0}, 'alias_expansion': ['septal hypertrophy', 'hypertrophy septal'], 'negation': False}]]
test_doc.moved_negs = {
    'include_criteria': ['unexplained left ventricular hypertrophy'], 
    'exclude_criteria': ['isolated septal hypertrophy'], 
    'inc_ents': [[
        {'raw_text': 'unexplained', 'label': 'ENTITY', 'start': 0, 'end': 11, 'cui': {'val': 'C4288071', 'score': 0.9999999403953552}, 'alias_expansion': ['Unexplained'], 'negation': False}, 
        {'raw_text': 'left ventricular hypertrophy', 'label': 'ENTITY', 'start': 12, 'end': 40, 'cui': {'val': 'C0149721', 'score': 1.0}, 'alias_expansion': ['lv hypertrophy', 'Enlarged left ventricle'], 'negation': False}]], 
    'exc_ents': [[
        {'raw_text': 'isolated', 'label': 'ENTITY', 'start': 0, 'end': 8, 'cui': {'val': 'C0205409', 'score': 1.0}, 'alias_expansion': ['Isolated', 'isolated'], 'negation': False}, 
        {'raw_text': 'septal hypertrophy', 'label': 'ENTITY', 'start': 9, 'end': 27, 'cui': {'val': 'C0442887', 'score': 1.0}, 'alias_expansion': ['septal hypertrophy', 'hypertrophy septal'], 'negation': False}]]
}
test_doc.aliased_crits = {
  'inc_alias_crits': ['unexplained lv hypertrophy enlarged left ventricle left ventricular hypertrophy'],
  'exc_alias_crits': []
}





#-----------------------------------------------------------------------------------------------#
# 14. creates a document without nlp and compares eligibility criteria processing and condition
# -----------------------------------------------------------------------------------------------#



test_folder_path = Path(__file__).parent.joinpath("ct_test_data.zip").as_posix()
test_folder_path = "/Users/jameskelly/Documents/cp/ctproc/clinicaltrials.gov-16_dec_2015_17.zip"

class EligProcTestCase(unittest.TestCase):

    
    def test_doc_proc_no_nlp(self):
      """process an empty criteria block
          it would normally be a list of processed documents, hence the indexing
      """
      self.maxDiff = None
      id_ = 'NCT02221141'
     
      cp = CTProc(CTConfig(test_folder_path, max_trials=50, get_only={id_}))
      id2doc = {res.nct_id : res for res in cp.process_data()}
      id_doc = id2doc[id_] 

      self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
      self.assertEqual(test_doc.condition, id_doc.condition)




#-------------------------------------------------------------------------------------------#
# 15. creates a document with spaCy model processing and compares entities, 
#     and eligbility info, with test document
# ------------------------------------------------------------------------------------------#


    def test_doc_proc(self):
      """
      process a zip file of a single document containing the id_ defined in the program
      as it uses nlp it will take much longer (about a minute) to do all that extra processing with the spaCy model
      """
      self.maxDiff = None
      id_ = 'NCT02221141'
      config = CTConfig(
        test_folder_path, 
        max_trials=25, 
        add_nlp=True, 
        get_only={id_}, 
        expand=True
      )

      cp = CTProc(config)
      id2doc = {res.nct_id : res for res in cp.process_data()}
      id_doc = id2doc[id_]

      self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
      self.assertEqual(test_doc.condition, id_doc.condition)
      self.assertEqual(test_doc.inc_ents, id_doc.inc_ents)
      self.assertEqual(test_doc.aliased_crits, id_doc.aliased_crits)




    
    
    def test_normal(self):
      """process a criteria blook with include and exclude criteria"""
      self.assertEqual(process_eligibility_naive(normal_raw), (norm_inc_crit, norm_exc_crit))


    def test_inc_only(self):
      """process a critieria block with include only criteria"""
      self.assertEqual(process_eligibility_naive(inc_only_raw), (norm_inc_crit, []))


    def test_exc_only(self):
      """process a critieria block with exclude only criteria"""
      self.assertEqual(process_eligibility_naive(exc_only_raw), ([], norm_exc_crit))


    def test_empty(self):
      """process an empty criteria block"""
      self.assertEqual(process_eligibility_naive(""), ([], []))


    def test_spaced(self):
      """process a well-defined but extra-spaced block"""
      self.assertEqual(process_eligibility_naive(normal_spaced_raw), (norm_spaced_inc_crit, norm_spaced_exc_crit))


    def test_no_dash(self):
      """process a well-defined but extra-spaced block"""
      self.assertEqual(process_eligibility_naive(normal_no_dash_raw), (norm_no_dash_inc_crit, norm_no_dash_exc_crit))

    def test_sub_numbers(self):
      """process a block with numeric subheaders"""
      self.assertEqual(process_eligibility_naive(sub_numbers_raw), (sub_numbers_inc_crit, sub_numbers_exc_crit))

    def test_headers(self):
      """process a block with (assumed) noisy headers"""
      self.assertEqual(process_eligibility_naive(headers_raw), (headers_inc_crit, headers_exc_crit))


    def test_no_dash_sub_numbers(self):
      """process a block with no dashes and subnumbering"""
      self.assertEqual(process_eligibility_naive(no_dash_sub_numbers_raw), (no_dash_sub_numbers_inc_crit, no_dash_sub_numbers_exc_crit))


    def test_individually_labelled(self):
      """process a block with individual labels for each criteria"""
      self.assertEqual(process_eligibility_naive(indv_label_raw), (indv_label_inc_crit, indv_label_exc_crit))


    def test_dash_and_header(self):
      """process a block with dash and header"""
      self.assertEqual(process_eligibility_naive(dash_and_header_raw), (dash_and_header_inc_crit, dash_and_header_exc_crit))

    def test_exc_in_inc(self):
      """process a block with a statement with "excluded?" in it"""
      self.assertEqual(process_eligibility_naive(exc_in_inc_raw), (exc_in_inc_inc_crit, exc_in_inc_exc_crit))

    def test_numbered_no_space(self):
      """process a block with leading number and no spaces between"""
      self.assertEqual(process_eligibility_naive(num_no_space_raw), (num_no_space_inc_crit, num_no_space_exc_crit))








if __name__ == '__main__':
    unittest.main()
