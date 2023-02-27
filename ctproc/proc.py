# OOP program for processing files of the form ClinicalTrials.2021-04-27.part1/NCT0093xxxx/NCT00934219.xml


import logging

import re
import copy
import json
import spacy
from tqdm import tqdm
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
from negspacy.negation import Negex
from scispacy.linking import EntityLinker 
from typing import Callable, Dict, Generator, List, NamedTuple, Optional, Set, Tuple, Union

from ctproc.doc_checker import DocChecker as dc

from ctproc.ctbase import NLPTools
from ctproc.cttopic import CTTopic
from ctproc.ctconfig import CTConfig
from ctproc.utils import print_crit, filter_words
from ctproc.ctdocument import CTDocument, EligCrit
from ctproc.eligibility import process_eligibility_naive
from ctproc.regex_patterns import EMPTY_PATTERN, TOPIC_ID_PATTERN




logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel('ERROR')



#----------------------------------------------------------------#
# Document Processing API Object
#----------------------------------------------------------------#

class CTProc:
  def __init__(self, ct_config: CTConfig):
    self.config: CTConfig = ct_config
    self.nlp_tools: Optional[NLPTools] = None

    if ct_config.nlp:
      self.add_nlp()
    else:
      nlp_flags = self.check_nlp_configs()
      if len(nlp_flags) > 0:
        logger.warning(f"these config flags are set as True, but will be ignored since nlp is False in self.config: \n{nlp_flags}")


  def check_nlp_configs(self) -> Set[str]:
    # user friendly func to warn about ignored flags if nlp is False in self.config
    # config args: remove_stops, add_ents, move_negations, expand
    config_flags = set()
    if self.config.add_ents:
        config_flags.add('add_ents')
    if self.config.remove_stops:
        config_flags.add('remove_stops')
    if self.config.expand:
        config_flags.add('expand')
    return config_flags


  def add_nlp(self):
    #np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 
    NLP = spacy.load("en_core_sci_md")  # throws runtime error if not installed
    NLP.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    NLP.add_pipe("negex")
    linker = NLP.get_pipe("scispacy_linker")
    STOP_WORDS = NLP.Defaults.stop_words
    self.nlp_tools = NLPTools(NLP=NLP, linker=linker, STOP_WORDS=STOP_WORDS)




  def process_data(self) -> Generator[None, None, Union[CTDocument, CTTopic]]:
    """
    desc:      main method for processing a zipped file of clinical trial XML documents from clinicaltrials.gov
    """
    with open(self.config.write_file, "w") as outfile:
        proc_func = self.get_proc_func()  # will be either proc_doc_data() or proc_topic_data()
        for processed_obj in proc_func():
            del processed_obj.nlp_tools  # remove nlp_tools from object before writing to file 
            json.dump(processed_obj, outfile, default= lambda o: o.__dict__)
            outfile.write("\n")
            yield processed_obj


  def get_proc_func(self) -> Callable:
    if self.config.is_topic:
        return self.process_topic_data
    return self.process_doc_data 



  def process_doc_data(self) -> Generator[None, None, CTDocument]:
    """
    desc:       main method for processing a zipped file of clinical trial XML documents from clinicaltrials.gov
                parameterized by CTConfig by which the ClinProc object (self) was initialized
    returns:    yields processed CTDocment objects, one at a time
    """
    
    with ZipFile(self.config.data_path, 'r') as zip_reader:
        for i, ct_file in enumerate(tqdm(zip_reader.namelist(), disable=self.config.disable_tqdm)):
            
            if not dc.iter_check(i, self.config):
                continue 

            processed_doc = self.build_doc(ct_file, zip_reader) 
            if processed_doc is not None:
                yield processed_doc

     
  def process_topic_data(self) -> Generator[None, None, CTTopic]:
    """
    desc:       main method for processing a single XML file of patient descriptions called "topics" in this sense
                parameterized by CTConfig the by which the ClinProc object (self) was initialized
    returns:    yields processed CTTopic objects, one at a time
    """

    topic_root = ElementTree.parse(self.config.data_path).getroot()
    for topic in topic_root:
        yield self.build_topic(topic.attrib['number'], topic.text)

  def build_doc(self, ct_file: str, zip_reader) -> Optional[CTDocument]:
    doc = self.build_doc_helper(ct_file, zip_reader)
    if doc is None:
        return None
    return self.transform_ct_object(doc)


  def build_doc_helper(self, ct_file: str, zip_reader) -> Optional[CTDocument]:
    if not dc.combined_predoc_check(ct_file, self.config):
        return None
    logger.info(f"ct file being processed: {ct_file}, doc being created")
    result_doc = self.process_ct_doc_file(zip_reader.open(ct_file, 'r'), self.config.id_to_print)
    if not dc.combined_doc_check(result_doc):
        return None
    return result_doc


  def build_topic(self, topic_id: int, topic_text: str) -> Optional[CTTopic]:
    ctop = CTTopic(id=topic_id, raw_text=topic_text, nlp_tools=self.nlp_tools)
    ctop = self.transform_ct_object(ctop)
    ctop.add_age_and_gender_data()        # might depend on added sentences
    return ctop
  

  

  def process_ct_doc_file(self, xml_filereader, id_to_print: Optional[str]):
    """
    xml_filereader:  specific type of object passed from process_data(),
                     used by parsexml library etree.parse() to get tree,
                     allows for easy searching and getting of desired fields 
                     in the document.

    id_to_print:     for debugging processing of a particular CT file, pass the id you wish
                     to have the contents printed for
                      
    desc:            parses xml tree for the set of required fields you see below. 
                     some fields require special treatment. chief among these is
                     'eligibility/criteria/textblock', requiring special 
                     functions to process ths value. 

    returns:         built CTDocument from processed xml data
    
    """
    doc_tree = ElementTree.parse(xml_filereader)
    root = doc_tree.getroot()

    docid = root.find('id_info/nct_id').text
    if docid == id_to_print:
        logger.info(ElementTree.tostring(root, pretty_print=True, encoding='unicode'))

    ct_doc = CTDocument(nct_id=docid, nlp_tools=self.nlp_tools)
    ct_doc.condition = [result.text for result in root.findall('condition')]
    ct_doc.condition_browse =  [result.text for result in root.findall('condition/condition_browse')] 
    ct_doc.intervention_type = [result.text for result in root.findall('intervention/intervention_type')]
    ct_doc.intervention_name = [result.text for result in root.findall('intervention/intervention_name')]
    ct_doc = self.add_eligibility(ct_doc, root)

    if ct_doc.id == id_to_print:
        print_crit(ct_doc.elig_crit.include_criteria, ct_doc.elig_crit.exclude_criteria)
                      
    ct_doc.process_doc_age(root) 

    return ct_doc

  
  
  def add_eligibility(self, ct_doc: CTDocument, xml_root: ElementTree) -> CTDocument:
    field_val = xml_root.find('eligibility/criteria/textblock')
    if field_val is None:
        logger.info("no eligbility criteria exists for this document")
        return ct_doc
    
    field_text = field_val.text
    if EMPTY_PATTERN.fullmatch(field_text):
        logger.info("eligibility criteria is empty")
        return ct_doc

    inc_elig, exc_elig = process_eligibility_naive(field_text)
    ct_doc.elig_crit = EligCrit(field_text) 
    ct_doc.elig_crit.include_criteria = inc_elig
    ct_doc.elig_crit.exclude_criteria = exc_elig
    return ct_doc 


  
  #----------------------------------------------------------------#
  # methods for transforming the documents and/or adding features
  #----------------------------------------------------------------#
  
  def transform_ct_object(self, ct_obj: Union[CTDocument, CTTopic]) -> Union[CTDocument, CTTopic]:    
    if self.config.nlp:
        ct_obj.add_nlp_features(self.config)

    if self.config.concat:
        ct_obj.concatenate_data()

    return ct_obj



  #--------------------------------------------------------------------------------------#
  # methods for reformatting text
  #--------------------------------------------------------------------------------------#

  def save_concat_all(
    self, 
    docs: List[CTDocument], 
    writefile: str, 
    ignore_fields: List[str] =[], 
    grab_only_fields: List[str] =[], 
    lower=False, 
    top_words=None
  ) -> List[CTDocument]:
    """
    docs:               list of dictionary objects containing CT data processed from zipfile
    writefile:          str or path object where dictionaries are written as jsonl (one dict per line)
    ignore_fields:      list of strings representing keys to be ignored when writing
    grab_only_fields:   opposite of ignore_fields, keys to get
    lower:              boolean saying where to call lower() on all string data 
    top_words:          set of words to be removed
    desc:               iterates through doc list, calls conatenate_data() on each doc,
                        creating a new 'contents' field from the concatenated fields
                        with passed args, writes contents selected to writefile, 
                        one dict per line (jsonl)


    """
    new_docs = copy.copy(docs)
    with open(writefile, 'w') as wf:
        for doc in new_docs:
            doc.concatenate_data(ignore_fields=ignore_fields, grab_only_fields=grab_only_fields, lower=lower)
            if top_words is not None:
                doc.contents = filter_words(doc.contents, top_words)

            json.dump(doc._asdict(), wf)
            wf.write('\n')
    return new_docs










if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='cli for clinproc process_data api')
    parser.add_argument('--data_path', help='pathlike to a zipped folder containing XML CT trial data')
    parser.add_argument('--write_file', help='pathlike to write location for jsonl file created, one processed trial per line')



    parser.add_argument('--concat', action='store_true',
                        help='Boolean, whether to concatenate all fields into a single content field (in addition to other parsed fields), default=False')

    parser.add_argument('--max_trials', type=int, default=1e7,
                        help='Integer for max number of files to process, default=1e7')


    parser.add_argument('--start_index', type=int, default=-1,
                        help='Integer specifying which index (minus 1) to start at. Useful for debugging or stopped processes, default=-1')


    parser.add_argument('--add_ents', action='store_false',
                        help='Boolean, whether to add a field for representing criterias as entities, default=True')


    parser.add_argument('--expand', action='store_false',
                        help='Boolean, whether to add a field for representing criterias as expansions of entity-related text values, default=True')



    parser.add_argument('--remove_stops', action='store_false',
                        help='Boolean, whether to add a field for representing criterias without stopwords, default=True')


    parser.add_argument('--id_to_print', default="",
                        help='String, an ID like NCT81001 supplied by user for printing a single processed clinical trial, debug info. default="')


    parser.add_argument('--get_only', default=None, nargs='+', 
                        help="List of strings, user supplied list of NCTID's to process, useful for debugging, default=None")



    args = parser.parse_args()

    ct_data = '/Users/jameskelly/Documents/cp/ctproc/ctproc/tests/CT_test_folder.zip'

    ct_config = CTConfig(
      data_path=args.data_path, 
      write_file=args.write_file, 
      concat=args.concat, 
      max_trials=args.max_trials, 
      start=args.start_index, 
      add_ents=args.add_ents, 
      expand=args.expand,
      remove_stops=args.remove_stops,
      id_to_print=args.id_to_print, 
      get_only=args.get_only
    )

    cp = CTProc(ct_config)
    for d in cp.process_data():
      print(d.__dict__)
      break




