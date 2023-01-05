# Process tons of files of the form ClinicalTrials.2021-04-27.part1/NCT0093xxxx/NCT00934219.xml, now on local disk


import logging

from typing import Any, Dict, Generator, List, Optional, Set, Tuple
from scispacy.linking import EntityLinker 
from negspacy.negation import Negex
from zipfile import ZipFile
from pathlib import Path
from lxml import etree
from tqdm import tqdm
import spacy
import copy
import json

from clinproc.utils import print_crit, filter_words, DONT_ALIAS
from clinproc.regex_patterns import EMPTY_PATTERN

from clinproc.ctconfig import CTConfig
from clinproc.ctdocument import CTDocument, EligCrit
from clinproc.eligibility import process_eligibility_naive




logger = logging.getLogger(__file__)







#----------------------------------------------------------------#
# Document Processing API Object
#----------------------------------------------------------------#

class ClinProc:

  def __init__(self, ct_config: CTConfig):
    self.config = ct_config
    if ct_config.add_nlp:
      self.add_nlp()


  def add_nlp(self):
    #np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 
    self.NLP = spacy.load("en_core_sci_md") 
    self.NLP.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    self.NLP.add_pipe("negex")
    self.linker = self.NLP.get_pipe("scispacy_linker")
    self.STOP_WORDS = self.NLP.Defaults.stop_words




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
                result_doc = self.filter_crit(result_doc, words_to_remove=self.STOP_WORDS)

              if self.config.add_nlp:
                if self.config.add_ents:
                  result_doc = self.add_entities(result_doc)
                  
                if self.config.move_negations:
                  result_doc, _ = self.move_doc_negs(result_doc)


              if self.config.save_data:
                json.dump(result_doc, outfile, default= lambda o: o.__dict__)
                outfile.write("\n")

              yield result_doc

          i += 1
            
    print(f"Total nunmber of trials documents processed: {i}")




  #----------------------------------------------------------------------------------------------#
  # methods for getting initial data into CTDocument forms according to preferences in CTConfig
  #----------------------------------------------------------------------------------------------#


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

    ct_doc = CTDocument(nct_id=docid)
    ct_doc.condition = [result.text for result in root.findall('condition')]
    ct_doc.condition_browse =  [result.text for result in root.findall('condition/condition_browse')] 
    ct_doc.intervention_type = [result.text for result in root.findall('intervention/intervention_type')]
    ct_doc.intervention_name = [result.text for result in root.findall('intervention/intervention_name')]
    ct_doc = self.get_eligibility(ct_doc, root)

    if ct_doc.nct_id == id_to_print:
      print_crit(ct_doc.eligibility_criteria.include_criteria, ct_doc.eligibility_criteria.exclude_criteria)
                      
    ct_doc.process_doc_age(root) 

    # other fields... required_fields[field] = clean_sentences([field_val])[0]
    return ct_doc

  
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
    ct_doc.elig_crit = EligCrit(field_text) 
    ct_doc.elig_crit.include_criteria = inc_elig
    ct_doc.elig_crit.exclude_criteria = exc_elig
    return ct_doc 



  #----------------------------------------------------------------#
  # Getting CUI expansions (entities)
  #----------------------------------------------------------------#

  def get_ents(self, sent_list: List[str], top_N: int = 2) -> List[Dict[str, str]]:
    """
    sent_list: list of sentence strings
    top_N:     int directing how many aliaseed terms to get
    desc:      uses spaCy pipeline to get entities and link them to terms,
              adds this information, entities lists of the sentences, 
              as a newa_field to the doc
    """
    new_ent_sents = []
    for sent in sent_list:
      nlp_sent = self.NLP(sent)
      new_ents = []
      for ent in nlp_sent.ents:
        for umls_ent in ent._.kb_ents:
          new_ent = {}
          new_ent['raw_text'] = ent.text
          new_ent['label'] = ent.label_
          new_ent['start'] = ent.start_char
          new_ent['end'] = ent.end_char
          new_ent['cui'] = {'val':umls_ent[0], 'score':umls_ent[1]}
          aliases = self.linker.kb.cui_to_entity[umls_ent[0]]._asdict()['aliases']
          new_ent['alias_expansion'] = aliases[:min(len(aliases), top_N)]
          new_ent["negation"] = ent._.negex
          #new_ent['covered_text'] = linker.kb.cui_to_entity[umls_ent[0]]
          new_ents.append(new_ent)
          break   # only get first one
      new_ent_sents.append(new_ents)
      
        
    return new_ent_sents



  def add_entities(self, ct_doc, top_N=2) -> CTDocument:
    """
    desc:    helper function to add the entities got from get_entities() to the doc
    """
    ct_doc.inc_ents = self.get_ents(ct_doc.elig_crit.include_criteria, top_N)
    ct_doc.exc_ents = self.get_ents(ct_doc.elig_crit.exclude_criteria, top_N)
    return ct_doc





  #----------------------------------------------------------------------------------------------#
  # methods for getting representations of eligibility criteria where aliases have been added
  #----------------------------------------------------------------------------------------------#

  def move_aliases(self, ct_doc: CTDocument, field_type: str, dont_alias=DONT_ALIAS):
    """
    doc:            a dict containing clinical trial data
    field_type:     exclude, include, topic are the 3 expected values for this 
    dont_alias:     globally defined set of terms to not be aliased for noticable
                    domain errors, e.g. the term ER, included in many documents,
                    to endoplasmic reticulum

    desc:           uses entities and location from the spaCy pipeline process,
                    with linked UMLS (CUI) terms, and there associated raw text forms
                    it iserts these values into the sentence in the position where
                    the entity is located, preserving the sentence except for the new
                    semantic redundancy. syntactic redundancy is not avoided, as many terms 
                    share value with other aliases, or the portion of the sentence being considered 
                    (entities can span multiple tokens), except in the case where these 
                    (possibly near) identical values are adjacent, in which case the last term of the 
                    inserted material will be dropped before inserting. 
                    This creates longer expanded sentences;

    """

    crit_field, ent_field, alias_field = self.alias_map(field_type)
    crits = self.get_elig_crits(ct_doc.elig_crit, crit_field)
    ents = ct_doc.inc_ents if (ent_field == 'inc_ents') else ct_doc.exc_ents
    for _, (ent_sent, crit) in enumerate(zip(ents, crits)):
      new_crit = crit
      added = 0
      for ent in ent_sent:
        if ent['raw_text'].lower()[:-1] in dont_alias:
          continue

        new_aliases = [a for a in self.get_new_aliases(ent)]
        if len(new_aliases) == 0:
          continue

        begin, end = self.get_ent_begin_and_end(new_crit, ent, added)
        new_aliases = self.handle_right_alias_end(end, new_aliases)
        add_part = ' '.join(new_aliases)   
        if len(add_part) > 0:
          add_part = add_part + ' '     

        add_len = len(add_part)
        new_crit = begin + add_part + end
        added += add_len    

      if field_type == "topic":
        ct_doc.elig_crit._asdict()[alias_field].append(new_crit.strip())
      else:
        ct_doc.alias_crits[alias_field].append(new_crit)

    return ct_doc
    
  def get_elig_crits(self, elig_crit: EligCrit, crit_field: str) -> List[str]:
    if crit_field == 'include_criteria':
      return elig_crit.include_criteria
    return elig_crit.exclude_criteria


  def get_new_aliases(self, ent) -> Generator[None, None, List[str]]:
    for alias in ent['alias_expansion']:
      alias = alias.lower().strip(',.?')
      if alias != ent['raw_text'].lower():
        yield alias


  def get_ent_begin_and_end(self, new_crit: str, ent, added: int) -> Tuple[str, str]:
    begin = new_crit[:ent['start'] + added]
    if not begin.endswith(' ') and (len(begin) > 0):
      begin += ' '
    end = new_crit[ent['start'] + added:]
    return begin, end
    

  def handle_right_alias_end(self, end: str, new_aliases: List[str]) -> List[str]:
    if len(end) > 0:
      last_alias_word = new_aliases[-1].split()[-1]
      if (end.split()[0] == last_alias_word) or (end.split()[0][:-1] == last_alias_word):
        last_alias = new_aliases[-1].split()
        if len(last_alias) > 1:
          new_aliases[-1] = ' '.join(last_alias[:-1])
        
        else:
          new_aliases = new_aliases[:-1]
    return new_aliases




  #--------------------------------------------------------------------
  # methods for moving negations
  #--------------------------------------------------------------------


  def move_all_negs(self, docs: List[CTDocument], inc_or_exc="inc", end_counts=None) -> Tuple[int, int]:
    total_changes = 0
    total_docs_changed = 0
    for doc in docs:       
      _, count = self.move_negs(doc, inc_or_exc=inc_or_exc, end_counts=end_counts)
      if count > 0:
        total_changes += count
        total_docs_changed += 1
        
    return total_docs_changed, total_changes



  def move_doc_negs(self, ct_doc: CTDocument, inc_or_exc="inc", end_counts=None) -> Tuple[CTDocument, int]:
    new_crits = []
    new_ent_sents = []
    changes = 0

    if ct_doc.moved_negations is None:
      ct_doc.moved_negs = {"include_criteria":ct_doc.elig_crit.include_criteria,
                        "exclude_criteria":ct_doc.elig_crit.exclude_criteria, 
                        "inc_ents":ct_doc.inc_ents, "exc_ents":ct_doc.exc_ents}

    # allow moving negation from inc to exc or vice versa
    crit_field, ent_field, other_crit_field, other_ent_field = self.get_neg_fields(inc_or_exc)
    

    # this loops got verbose because I had to keep track of both the positions in the criteria string and
    # the entities list in order to build the representations desired
    crits = self.get_elig_crits(ct_doc.elig_crit, crit_field)
    ents = ct_doc.inc_ents if (ent_field == 'inc_ents') else ct_doc.exc_ents
    for crit, ent_sent in zip(crits, ents):
      i = 0
      neg_found = False
      #split_crit = crit.split()
      while i < len(ent_sent):
        ent = ent_sent[i]
        ent_start = i
        if ent['negation']:
          neg_found = True
          
          text_start, text_end, ent_end = self.get_neg_text_begin_end(ent, ent_sent)

          # stuff for the beginning and end of remaming string and corresponding ent lists
          end_part = crit[text_end:]
          start_part = crit[:text_start]
          ent_start_part = ent_sent[:ent_start]
          ent_end_part = ent_sent[ent_end:]
          new_crit = ""
          new_ent_sent = []
          other_ent = []
          
          other_crit = crit[text_start:text_end]

          good_end = self.get_good_neg_end(start_part, ent_start_part)
          if good_end is not None:
            other_crit = good_end + ' ' + other_crit # could be severe, significant, etc. 
          other_ent = ent_sent[ent_start:ent_end]
      
          if len(end_part.strip().split()) > 2:
            new_crit += end_part
            new_ent_sent += ent_end_part

          if len(other_ent) > 1:
            ct_doc.moved_negs[other_ent_field].append(other_ent)
            ct_doc.moved_negs[other_crit_field].append(other_crit)
        

        i += 1

      
      if neg_found:
        changes += 1
        if len(new_crit.split()) > 2:
          new_crits.append(new_crit)
          new_ent_sents.append(new_ent_sent)
      else:
        new_crits.append(crit)
        new_ent_sents.append(ent_sent)

  
    
    ct_doc.moved_negs[crit_field] = new_crits
    ct_doc.moved_negs[ent_field] = new_ent_sents
    return ct_doc, changes
    
  
  def get_neg_fields(self, inc_or_exc: str) -> Tuple[str, str, str, str]:
    # allows moving negation from inc to exc or vice versa
    if inc_or_exc == 'inc':
      crit_field = "include_criteria"
      ent_field = "inc_ents"
      other_crit_field = "exclude_criteria"
      other_ent_field = "exc_ents"
    else:
      crit_field = "exclude_criteria"
      ent_field = "exc_ents"
      other_crit_field = "include_criteria"
      other_ent_field = "inc_ents"
    
    return crit_field, ent_field, other_crit_field, other_ent_field


  def get_neg_text_begin_end(self, ent, ent_sent) -> Tuple[int, int, int]:
    text_start = ent['start']                      # find the place in the criteria string where the negated entitiy raw string starts
    while (i < len(ent_sent) - 1) and ent_sent[i+1]['negation']: # get all of the text and relative ents associated with that negated span
      i += 1
    
    text_end = ent_sent[i]['end']
    ent_end = i + 1
    return text_start, text_end, ent_end



  def get_good_and_bad_neg_end(self, start_part: str, ent_start_part: str, end_counts: int) -> Optional[str]:
    bad_end_exists = True
    if (len(start_part.strip().split()) > 3) and not self.check_if_bad_end(start_part, end_counts):
      new_crit += start_part
      new_ent_sent += ent_start_part
      bad_end_exists = False
      
    if not bad_end_exists:
      good_end = self.get_good_end(start_part)
    else:
      good_end = None
    
    return good_end



  def check_if_bad_end(self, sent, end_counts=None) -> bool:
    bad_ends = ["be", "have", "to", "with", "for", "of", "no", "not", "other", "been"]
    last_word = sent.split()[-1]
    if end_counts is not None:
      end_counts[last_word] += 1
    for be in bad_ends:
      if last_word == be:
        return True
    return False



  def get_good_end(self, sent) -> str:
    #good_ends = ["severe", "significant", "current", "prior", "previous"]
    last_word = sent.strip().split()[-1]
    return last_word
    #for ge in good_ends:
    #  if last_word == ge:
    #    return last_word
    #return None




  #--------------------------------------------------------------------
  # methods for reformatting text
  #--------------------------------------------------------------------

  def get_sentences(self, textblock: str) -> List[str]:
    """
    uses spaCy en_core_sci_md package to do sentence segmentation 
    """
    return [s.text for s in self.NLP(textblock).sents]


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
    filtered['gender'] = ct_doc['eligibility/gender']
    filtered['include_cuis'] = ' '.join([ent['cui']['val'] for ent in ct_doc.inc_ents])
    filtered['exclude_cuis'] = ' '.join([ent['cui']['val'] for ent in ct_doc.exc_ents])
    return filtered


  def filter_crit(self, ct_doc: CTDocument, words_to_remove: Set[str]) -> CTDocument:
    """
    desc:    helper function to add versions of the criteria without stopwords to the doc
    """
    ct_doc.inc_filtered = [filter_words(sent, words_to_remove) for sent in ct_doc.elig_crit.include_criteria]
    ct_doc.exc_filtered = [filter_words(sent, words_to_remove) for sent in ct_doc.elig_crit.exclude_criteria]
    return ct_doc


  def concat_all(
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
        doc.concatenate_data(ignore_fields=ignore_fields, grab_only_fields=grab_only_fields, lower=lower)
        if top_words is not None:
          doc.contents = filter_words(doc.contents, top_words)
        json.dump(doc._asdict(), wf)
        wf.write('\n')
    return new_docs













if __name__ == "__main__":
    data = '/Users/jameskelly/Documents/cp/clinproc/clinproc/tests/CT_test_folder.zip'
    cp = ClinProc(CTConfig(data))
    docs = [doc for doc in cp.process_data()]
    print(docs[0])

