import logging 

import unittest

from ctproc.tests.test_elig import *
from ctproc.tests.test_doc import test_doc
from ctproc.tests.test_topic import test_topic

from ctproc.proc import CTProc
from ctproc.ctconfig import CTConfig
from ctproc.eligibility import process_eligibility_naive





# TODO: uncomment, test_doc_folder_path = Path(__file__).parent.joinpath("ct_test_doc_data.zip").as_posix()
test_doc_folder_path = "/Users/jameskelly/Documents/cp/ctproc/clinicaltrials.gov-16_dec_2015_17.zip"

# test optional support for topic processing
# TODO: uncomment, test_topic_folder_path = Path(__file__).parent.joinpath("ct_test_topic_data.xml").as_posix()
test_topic_folder_path = "/Users/jameskelly/Documents/cp/ctproc/ctproc/tests/ct_topic_test_data.xml"


class DocProcTestCase(unittest.TestCase):

    
    def test_doc_proc_no_nlp(self):
      """
      process a zip file of (possibly) a single document containing the id_ defined in the program
      """
      self.maxDiff = None
      id_ = 'NCT02221141'
     
      cp = CTProc(CTConfig(test_doc_folder_path, max_trials=25, get_only={id_}, disable_tqdm=True))
      id2doc = {res.id : res for res in cp.process_data()}
      id_doc = id2doc[id_] 

      self.assertEqual(test_doc.condition, id_doc.condition)
      self.assertEqual(test_doc.elig_crit.include_criteria, id_doc.elig_crit.include_criteria)
      self.assertEqual(test_doc.elig_crit.exclude_criteria, id_doc.elig_crit.exclude_criteria)



    @unittest.skip("skip for faster tests")
    def test_doc_proc(self):
      """
      process a zip file of a single document containing the id_ defined in the program
      as it uses nlp it will take much longer (about a minute) to do all that extra processing with the spaCy model
      """
      self.maxDiff = None
      id_ = 'NCT02221141'
      config = CTConfig(
        data_path=test_doc_folder_path, 
        max_trials=25, 
        nlp=True, 
        get_only={id_}, 
        expand=True,
        disable_tqdm=True
      )

      cp = CTProc(config)
      id2doc = {res.id : res for res in cp.process_data()}
      id_doc = id2doc[id_]

      self.assertEqual(test_doc.elig_crit.__dict__, id_doc.elig_crit.__dict__)
      self.assertEqual(test_doc.condition, id_doc.condition)
      self.assertEqual(test_doc.inc_ents, id_doc.inc_ents)
      self.assertEqual(test_doc.elig_crit.inc_aliased_crit, id_doc.elig_crit.inc_aliased_crit)
      self.assertEqual(test_doc.elig_crit.exc_aliased_crit, id_doc.elig_crit.exc_aliased_crit)





class TopicProcTestCase(unittest.TestCase):
    
    def test_topic_proc_no_nlp(self):
        topic_config = CTConfig(
            data_path=test_topic_folder_path, 
            is_topic=True,
            disable_tqdm=True
        )
        cp = CTProc(topic_config)
        id2topic = {res.id:res for res in cp.process_data()}
        id_topic = id2topic['1'] 
        self.assertEqual(id_topic.raw_text, test_topic.raw_text)
        self.assertEqual(id_topic.age, test_topic.age)
        self.assertEqual(id_topic.gender, test_topic.gender)



    @unittest.skip("skip for faster tests") 
    def test_topic_proc(self):
        topic_config = CTConfig(
            data_path=test_topic_folder_path, 
            nlp=True,
            is_topic=True,
            disable_tqdm=True
        )

        cp = CTProc(topic_config)
        id2doc = {res.id : res for res in cp.process_data()}
        id_topic = id2doc['1'] 

        self.assertEqual(id_topic.raw_text, test_topic.raw_text)
        self.assertEqual(id_topic.age, test_topic.age)
        self.assertEqual(id_topic.gender, test_topic.gender)





class EligProcTestCase(unittest.TestCase):
    
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
