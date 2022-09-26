# Process tons of files of the form ClinicalTrials.2021-04-27.part1/NCT0093xxxx/NCT00934219.xml, now on local disk


import logging
from utils import *

from ctdocument import CTDocument
from ctconfig import CTConfig

from typing import Dict, Generator, List, NamedTuple, Optional
from eligibility import process_eligibility_naive
from clinproc.regex_patterns import *
from scispacy.linking import EntityLinker
from negspacy.negation import Negex
from move_negs import move_neg, move_negs
from collections import Counter
from ctconfig import CTConfig
from zipfile import ZipFile
from pathlib import Path
from lxml import etree
from tqdm import tqdm
import numpy as np
import spacy
import copy
import json
import os
import re


logger = logging.getLogger(__file__)

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 
nlp = spacy.load("en_core_sci_md") 

nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
nlp.add_pipe("negex")
linker = nlp.get_pipe("scispacy_linker")

STOP_WORDS = nlp.Defaults.stop_words





#----------------------------------------------------------------#
# Document Processing
#----------------------------------------------------------------#

class ClinProc:

  def __init__(self, ct_config:CTConfig):
    self.config = ct_config
    self.nlp = nlp

  def process_data(self) -> Generator[None, None, CTDocument]:
    """
    desc:
    returns:
   
    """

    with ZipFile(self.config.zip_data, 'r') as zip:
      i = 0
      with open(self.config.write_file, "w") as outfile:
        for ct_file in tqdm(zip.namelist()):
          if ct_file.endswith('xml') and (i < self.config.max_trials) and (i > self.config.start):
            if (self.config.get_only is not None) and (Path(ct_file).name[:-4] not in self.config.get_only):
              continue 
            result_doc = self.process_ct_file(zip.open(ct_file, 'r'), self.config.id_to_print)

            if result_doc is not None:
              if self.config.concat:
                result_doc.concatenate_data()
              
              result_doc.make_content_field()

              if self.config.remove_stops:
                result_doc.remove_words(words_to_remove=STOP_WORDS)

              if self.config.add_ents:
                result_doc.entity_expand()

              json.dump(result_doc._asdict(), outfile)
              outfile.write("\n")
              yield result_doc

          i += 1
            
    print(f"Total nunmber of trials documents processed: {i}")






  def process_ct_file(self, xml_filereader, id_to_print=""):
    """
    xml_filereader:  specific type of object passed from process_data(),
                      used by parsexml library etree.parse() to get tree,
                      allows for easy searching and getting of desired fields 
                      in the document.

    id_to_print:     for debugging a particular CT file, pass the id you wish
                      to have the contents printed for
                      
    desc:            parses xml tree for the set of required fields you see below. 
                      some fields require special treatment. chief among these is
                      'eligibility/criteria/textblock', requiring special 
                      functions to process ths value. 

    returns:         processed dict of required fields as new document
    
    """
    doc_tree = etree.parse(xml_filereader)
    root = doc_tree.getroot()

    docid = root.find('id_info/nct_id').text
    if docid == id_to_print:
      print(etree.tostring(root, pretty_print=True, encoding='unicode'))

    ct_doc = CTDocument(ncd_id=docid)
    ct_doc.condition = [result.text for result in root.findall('condition')]
    ct_doc.condition_browse =  [result.text for result in root.findall('condition/condition_browse')] 
    ct_doc.intervention_type = [result.text for result in root.findall('intervention/intervention_type')]
    ct_doc.intervention_name = [result.text for result in root.findall('intervention/intervention_name')]
    ct_doc = self.get_eligibility(ct_doc, root)

    if ct_doc.nct_id == id_to_print:
      print_crit(ct_doc.eligibility_criteria.include_criteria, ct_doc.eligibility_criteria.exclude_criteria)
                      
    ct_doc = get_processed_age(ct_doc, root) 

    # other fields... required_fields[field] = clean_sentences([field_val])[0]
    return ct_doc



  def get_filtered_doc_as_dict(self, ct_doc: CTDocument, writefile: Path) -> Dict[str, str]:
    """
    docs:       dicts containing clinical trial data
    writefile:  location to dump the filtered version to
    desc:       creates smaller, filtered versions of the documents for
                some other types of uses

    """
    filtered = {}
    filtered['nct_id'] = ct_doc.nct_id
    filtered['min_age'] = ct_doc.elig_min_age
    filtered['max_age'] = ct_doc['eligibility/maximum_age']
    filtered['gender'] = doc['eligibility/gender']
    filtered['include_cuis'] = ' '.join([ent['cui']['val'] for ent in ct_doc.inc_ents])
    filtered['exclude_cuis'] = ' '.join([ent['cui']['val'] for ent in ct_doc.exc_ents])
    return filtered
  

  def get_sentences(textblock: str) -> List[str]:
    """
    uses spaCy en_core_sci_md package to do sentence segmentation 
    """
    return [s.text for s in nlp(textblock).sents]


  def get_eligibility(self, ct_doc: CTDocument, xml_root: etree.ElementTree) -> CTDocument:
    field_val = xml_root.find('eligibility/criteria/textblock')
    if field_val is None:
      logger.info("no eligbility criteria exists for this document")
      return ct_doc
    
    field_text = field_val.text
    if EMPTY_PATTERN.fullmatch(field_text):
      logger.info("eligibility criteria is empty")
      return ct_doc

    inc_elig, exc_elig = process_eligibility_naive(field_text)
    ct_doc.elig_crit.include_criteria = inc_elig
    ct_doc.elig_crit.exclude_criteria = exc_elig
    ct_doc.elig_crit.raw_text = field_text
    



def move_aliases(doc, field_type, dont_alias=DONT_ALIAS):
  """
  doc:            a dict containing clinical trial data
  field_type:     exclude, include, topic are the 3 expected values for this 
  dont_alias:     globally defined set of terms to not be aliased for notocable
                  domain errors, e.g. the term ER, included in many documents,
                  to endoplasmic reticulum

  desc:           uses entities and location from the spaCy pipeline process,
                  with linked UMLS (CUI) terms, and there associated raw text forms
                  it iserts these values into the sentence in the position where
                  the entitiy is located, preserving the sentence except for the new
                  semantic redundancy. syntactic redundancy is not avoided, as many terms 
                  share value with other aliases, or the portion of the sentence being considered 
                  (entities can sopan multiple tokens), except in the case where these 
                  (possibly near) identical values are adjacent, in which case the last term of the 
                  inserted material will be droped before inserting. 
                  This creates longer expanded sentences;

  """

  crit_field, ent_field, alias_field = alias_map(field_type)
  doc = make_alias_doc_field(doc, field_type, alias_field)
  crits = doc['eligibility/criteria/textblock'][crit_field] if (field_type != "topic") else doc[crit_field]
  ents = doc[ent_field]
  for i, (ent_sent, crit) in enumerate(zip(ents, crits)):
    new_crit = crit
    added = 0
    for ent in ent_sent:
      if (ent['raw_text'].lower()) in dont_alias or  (ent['raw_text'].lower()[:-1] in dont_alias):
        continue

      new_aliases = []
      for alias in ent['alias_expansion']:
        alias = alias.lower().strip(',.?')
        if alias != ent['raw_text'].lower():
          new_aliases.append(alias)
      
      begin = new_crit[:ent['start'] + added]
      if not begin.endswith(' ') and (len(begin) > 0):
        begin += ' '
      end = new_crit[ent['start'] + added:]

      if len(new_aliases) == 0:
        continue

      last_alias_word = new_aliases[-1].split()[-1]
      if len(end) > 0:
        if (end.split()[0] == last_alias_word) or (end.split()[0][:-1] == last_alias_word):
          last_alias = new_aliases[-1].split()
          if len(last_alias) > 1:
            new_aliases[-1] = ' '.join(last_alias[:-1])
          
          else:
            new_aliases = new_aliases[:-1]

      add_part = ' '.join(new_aliases)   
      if len(add_part) > 0:
        add_part = add_part + ' '     

      add_len = len(add_part)
      new_crit = begin + add_part + end
      
      added += add_len    

    if field_type == "topic":
      doc[alias_field].append(new_crit.strip())
    else:
      doc["alias_crits"][alias_field].append(new_crit)








def concat_all(docs, writefile, ignore_fields=[], grab_only_fields=[], lower=False, top_words=None):
  """
  docs:               list of dictionary objects containing CT data processed from zipfile
  writefile:          str or path object where dictionaries are written as jsonl (one dict per line)
  ignore_fields:      list of strings representing keys to be ignoredwhen writing
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
      concat_doc = concatenate_data(doc, ignore_fields=ignore_fields, grab_only_fields=grab_only_fields, lower=lower)
      doc['contents'] = concat_doc['contents']
      if top_words is not None:
        doc['contents'] = remove_top_words(doc['contents'], top_words)
      json.dump(doc, wf)
      wf.write('\n')
  return new_docs







if __name__ == "__main__":
    data = '/home/mrkellyjam/ct_prep_pkg/tests/CT_test_folder.zip'
    doc = process_data(data, "output")
    print(doc)

