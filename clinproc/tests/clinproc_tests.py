
import unittest
from pathlib import Path
from clinproc.proc import ClinProc, CTDocument, EligCrit
from clinproc.ctconfig import CTConfig
from clinproc.eligibility import process_eligibility_naive


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

class EligProcTestCase(unittest.TestCase):

    
    # def test_doc_proc(self):
        
    #     """process an empty criteria block
    #        it would normally be a list of processed documents, hence the indexing
    #     """
    #     self.maxDiff = None
    #     id_ = 'NCT02221141'
    #     cp = ClinProc(CTConfig(test_folder_path, id_to_print=id_, max_trials=25))
    #     id2doc = {res.nct_id : res for res in cp.process_data()}
    #     id_doc = id2doc[id_]

    #     self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
    #     self.assertEqual(test_doc.condition, id_doc.condition)
    #     self.assertEqual(test_doc.inc_ents, id_doc.inc_ents)

    
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
