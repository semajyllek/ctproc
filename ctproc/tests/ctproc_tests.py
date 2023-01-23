
import unittest
from pathlib import Path
from ctproc.ctconfig import CTConfig
from ctproc.proc import CTProc, CTDocument, EligCrit
from ctproc.eligibility import process_eligibility_naive


normal_crit   =  """
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



inc_only_crit   =  """
                    Inclusion Criteria:
                         -  Patients with HF or IHD who are not currently taking the study medications of
                            interest (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD) and
                            whose primary care physicians are part of the study population
                  """


exc_only_crit   =  """
                    Exclusion Criteria:
                        -  Patients who are unable or unwilling to give informed consent,
                        -  previously taken the study medications according to dispensing records
                        -  allergy or intolerance to study medications
                        -  residents of long-term care facilities
                        -  unable to confirm a diagnosis of either HF or IHD
                        -  primary care physician has already contributed 5 patients to the study
                  """




inc_norm = [
        "Patients with HF or IHD who are not currently taking the study medications of interest" \
        + " (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD)" \
        + " and whose primary care physicians are part of the study population"
        ]


exc_norm = [
        'Patients who are unable or unwilling to give informed consent', 
        'previously taken the study medications according to dispensing records', 
        'allergy or intolerance to study medications', 
        'residents of long-term care facilities', 
        'unable to confirm a diagnosis of either HF or IHD', 
        'primary care physician has already contributed 5 patients to the study'
        ]


# test document
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



test_folder_path = Path(__file__).parent.joinpath("ct_test_data.zip").as_posix()
#test_folder_path = "/Users/jameskelly/Documents/cp/clinproc/clinicaltrials.gov-16_dec_2015_17.zip"

class EligProcTestCase(unittest.TestCase):

    
    def test_doc_proc_no_nlp(self):
        
        """process an empty criteria block
           it would normally be a list of processed documents, hence the indexing
        """
        self.maxDiff = None
        id_ = 'NCT02221141'
        cp = CTProc(CTConfig(test_folder_path, max_trials=25))
        id2doc = {res.nct_id : res for res in cp.process_data()}
        id_doc = id2doc[id_] 
  
        self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
        self.assertEqual(test_doc.condition, id_doc.condition)



    def test_doc_proc(self):
        
        """process an empty criteria block
           it would normally be a list of processed documents, hence the indexing
        """
        self.maxDiff = None
        id_ = 'NCT02221141'
        cp = CTProc(CTConfig(test_folder_path, max_trials=25, add_nlp=True))
        id2doc = {res.nct_id : res for res in cp.process_data()}
        id_doc = id2doc[id_]

        self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
        self.assertEqual(test_doc.condition, id_doc.condition)
        self.assertEqual(test_doc.inc_ents, id_doc.inc_ents)

    
    def test_normal(self):
        """process a criteria blook with include and exclude criteria"""
        self.assertEqual(process_eligibility_naive(normal_crit), (inc_norm, exc_norm))


    def test_inc_only(self):
        """process a critieria block with include only criteria"""
        self.assertEqual(process_eligibility_naive(inc_only_crit), (inc_norm, []))


    def test_exc_only(self):
        """process a critieria block with exclude only criteria"""
        self.assertEqual(process_eligibility_naive(exc_only_crit), ([], exc_norm))


    def test_empty(self):
        """process an empty criteria block"""
        self.assertEqual(process_eligibility_naive(""), ([], []))












if __name__ == '__main__':
    unittest.main()
