
import logging

import re
import json
from lxml import etree
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from ctproc.regex_patterns import EMPTY_PATTERN
from ctproc.skip_crit import SKIP_CRIT


logger = logging.getLogger(__file__)

REMOVE_WORDS = ["criteria", "include", "exclude", "inclusion", "exclusion", "eligibility"]


# -------------------------------------------------------------------------------------- #
# I/O utils
# -------------------------------------------------------------------------------------- #

def save_docs_jsonl(docs: List[Any], writefile: Path) -> None:
  """
  desc:    iteratively writes contents of docs as jsonl to writefile 
  """
  with open(writefile, "w") as outfile:
    for doc in docs:
      json.dump(doc, outfile)
      outfile.write("\n")



def get_processed_data(proc_loc, get_only: Optional[Set[str]] = None) -> List[Dict[str, str]]:
  """
  proc_loc:    str or path to location of docs in jsonl form
  """
  with open(proc_loc, 'r') as json_file:
    json_list = list(json_file)

  doc_list = [json.loads(json_str) for json_str in json_list]
  if get_only is not None:
    return filter_processed_data(doc_list, get_only=get_only)
  return doc_list



def filter_processed_data(docs: List[Dict[str, str]], get_only: Set[str]) -> List[Dict[str, str]]:
  """
  docs:    list of processed docs
  get_only: set of nct_id strings to filter docs by
  """
  return [doc for doc in docs if doc['id'] in get_only]



# -------------------------------------------------------------------------------------- #
# text processing utils
# -------------------------------------------------------------------------------------- #


def filter_words(text: str, remove_words: Set[str]):
  """
  text:         str of text to be filtered
  remove_words: set of words to remove
  """
  return ' '.join([word for word in text.split() if word not in remove_words])




def check_word(word: str, words_to_remove: Set[str] = REMOVE_WORDS) -> bool:
  w = word.strip(":-,") 

  # ex. DISEASE
  if re.match(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]+(?: [A-Z]+)?', w):
    return False

  if w.lower() in words_to_remove:
    return False

  return True

  

def fix_sentence(sent: str) -> str:
  """
  sents:   a list of strings (not tokenized) representing sentences
  desc:    removes sentences that don't contain any actual criteria
  returns: a list of sentences without filler information (not necessarily one criteria per sent however)
  """
  #include_pattern = re.compile(".*(?:(?:(?:[Ee]|[Ii])(?:(?:x|n)(?:clu(?:(?:de)|(?:sion))))|(?:(?:ne)?ligibility))(?: criteria)? (.*)")
  return ' '.join([w for w in sent.split() if check_word(w)]).strip('.,;:')
 

def remove_leading_number(s: str) -> str:
  m = re.match(r'\d+. *(?P<crit>.*)', s)
  if m is not None:
    s = m['crit']
  return s


def clean_sentences(sent_list: List[str]):
  """
  sent_list:   list of sentence strings
  desc:        removes a bunch of large spaces and newline characters from the text 
  """
  new_sents = []
  for sent in sent_list:
    for s in re.split(r"- ", sent):
      s = fix_sentence(s)
      s = remove_leading_number(s)
      if len(s) > 2 and s not in SKIP_CRIT:
        new_sents.append(s)

  return new_sents
  


# -------------------------------------------------------------------------------------- #
# age processing utils
# -------------------------------------------------------------------------------------- #

def convert_age_to_year(age, units):
  """
  age:  string result for the age extracted
  unit: string being either years or months (or some variation of those 2)
  desc: converts string to float, months to years if unit is month
  """
  if age is not None:
    age = float(age)
    if units is not None:
      if 'm' in units.lower():
        age /= 12.
      elif 'w' in units.lower():
        age /= 52.
      elif 'd' in units.lower():
        age /= 365. 
  return round(age, 3) 





# -------------------------------------------------------------------------------------- #
# ct processing utils
# -------------------------------------------------------------------------------------- #


def get_str_or_none(field: str, xml_root: etree.ElementTree) -> Optional[str]:
    field_val = xml_root.find(field)
    if field_val is None:
      logger.info("missing field: {field}")
      return None

    field_text = field_val.text
    if EMPTY_PATTERN.fullmatch(field_text):
      return None

    return clean_sentences([field_text])




def data_to_str(data, contents_ignore_fields, grab_only_fields):
  """
  desc:   recursively converts all data to a single concatenated string
          only works for strings, lists and dicts
  """
  c = ""
  if type(data) == list:
    for d in data:
      c += " " + data_to_str(d, contents_ignore_fields, grab_only_fields)
  elif type(data) == dict:
    for f, v in data.items():
      if len(grab_only_fields) != 0:
        if f in grab_only_fields:
          c += " " + data_to_str(v, contents_ignore_fields, grab_only_fields)
      elif f not in contents_ignore_fields:
        c += " " + data_to_str(v, contents_ignore_fields, grab_only_fields)
  elif (type(data) == float) or (type(data) == int):
    c += " " + str(data) 
  elif type(data) == str:
    c += " " + data
  return c



# -------------------------------------------------------------------------------------- #
# print utils
# -------------------------------------------------------------------------------------- #

def print_crit(inc_elig: List[str], exc_elig: List[str]) -> None:
  print("\n\nINC CRIT")
  print('\n'.join(inc_elig))
  print("\nEXC CRIT")
  print('\n'.join(exc_elig))

