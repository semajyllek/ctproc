


from proc import process_eligibility_naive, process_data
import unittest
import os

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
        'Patients who are unable or unwilling to give informed consent,', 
        'previously taken the study medications according to dispensing records', 
        'allergy or intolerance to study medications', 
        'residents of long-term care facilities', 
        'unable to confirm a diagnosis of either HF or IHD', 
        'primary care physician has already contributed 5 patients to the study'
        ]


test_doc = {
        'id': 'NCT00000202', 
        'brief_title': 'Buprenorphine Maintenance for Opioid Addicts - 1', 
        'eligibility/criteria/textblock': {
                    'raw_text': '\n        Please contact site for information.\n      ', 
                    'include_criteria': ['Please contact site for information.'], 
                    'exclude_criteria': []
        }, 
        'eligibility/gender': 'Both', 
        'eligibility/minimum_age': 18.0, 
        'eligibility/maximum_age': 65.0, 
        'detailed_description/textblock': None, 
        'condition': ['Opioid-Related Disorders'], 
        'condition/condition_browse': [], 
        'intervention/intervention_type': ['Drug'], 
        'intervention/intervention_name': ['Buprenorphine'], 
        'intervention_browse/mesh_term': 'Buprenorphine', 
        'contents': 'The purpose of this study is to evaluate the efficacy of buprenorphine and desipramine in treatment of opiate and cocaine dependence.', 
        'inc_no_stop': ['contact site information.'], 
        'exc_no_stop': [], 
        'inc_ents': [[
            {
                'raw_text': 'contact site', 'label': 'ENTITY', 'start': 7, 'end': 19, 'cui': {'val': 'C2752541', 'score': 1.0}, 
                'alias_expansion': [], 'negation': False
            }, 
            {
                'raw_text': 'information', 'label': 'ENTITY', 'start': 24, 'end': 35, 'cui': {'val': 'C0870705', 'score': 0.9999998807907104}, 
                'alias_expansion': ['information'], 'negation': False
            }
        ]], 
        'exc_ents': [], 
        'moved_negs': {
            'include_criteria': ['Please contact site for information.'], 
            'exclude_criteria': [], 
            'inc_ents': [[
            {
            'raw_text': 'contact site', 'label': 'ENTITY', 'start': 7, 'end': 19, 'cui': {'val': 'C2752541', 'score': 1.0}, 
            'alias_expansion': [], 'negation': False
            }, 
            {
            'raw_text': 'information', 'label': 'ENTITY', 'start': 24, 'end': 35, 'cui': {'val': 'C0870705', 'score': 0.9999998807907104}, 
            'alias_expansion': ['information'], 'negation': False
            }
            ]], 
            'exc_ents': []
        }, 
        'alias_crits': {
            'inc_alias_crits': ['Please contact site for information.'], 
            'exc_alias_crits': []
        }
        }



test_folder_path = "tests/CT_test_folder.zip"
test_write_path = "tests/ct_output"

class EligProcTestCase(unittest.TestCase):

    
    def test_proc_doc(self):
        """process an empty criteria block
           it would normally be a list of processed documents, hence the indexing
        """
        self.assertEqual(test_doc, process_data(test_folder_path, test_write_path)[0])
        os.remove(test_write_path) 
    
    
    def test_normal(self):
        """process a criteria blook with include and exclude criteria"""
        self.assertEqual(process_eligibility_naive(normal_crit), (inc_norm, exc_norm))


    def test_inc_only(self):
        """process a critieria block with include only criteria"""
        self.assertEqual(process_eligibility_naive(inc_only_crit), (inc_norm, []))


    def test_exc_only(self):
        """process a critieria block with include only criteria"""
        self.assertEqual(process_eligibility_naive(exc_only_crit), ([], exc_norm))


    def test_empty(self):
        """process an empty criteria block"""
        self.assertEqual(process_eligibility_naive(""), ([], []))












if __name__ == '__main__':
    unittest.main()
