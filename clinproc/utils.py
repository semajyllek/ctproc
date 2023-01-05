
import logging

import re
import json
from lxml import etree
from pathlib import Path
from clinproc.regex_patterns import *
from typing import List, Optional, Set, Any


logger = logging.getLogger(__file__)

DONT_ALIAS = {"yo", "girl", "boy", "er", "changes", "patient", "male", "female", "age"}
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



def get_processed_docs(proc_loc):
  """
  proc_loc:    str or path to location of docs in jsonl form
  """
  with open(proc_loc, 'r') as json_file:
    json_list = list(json_file)

  return [json.loads(json_str) for json_str in json_list]

 






# -------------------------------------------------------------------------------------- #
# text processing utils
# -------------------------------------------------------------------------------------- #


def filter_words(text: str, remove_words: Set[str]):
  """
  text:         str of text to be filtered
  remove_words: set of words to remove
  """
  new_contents = [word for word in text.split() if word not in remove_words]
  return ' '.join(new_contents)


def clean_sentences(sent_list: List[str]):
  """
  sent_list:   list of sentence strings
  desc:        removes a bunch of large spaces and newline characters from the text 
  """
  return [re.sub(r"  +", " ", re.sub(r"[\n\r]", "", s)).strip() for s in sent_list]
  

def check_sentences(sents, words_to_remove=REMOVE_WORDS):
  """
  sents:   a list of strings (not tokenized) representing sentences
  desc:    removes sentences that don't contain any actual criteria
  returns: a list of sentences without filler information (not necessarily one criteria per sent however)
  """
  #include_pattern = re.compile(".*(?:(?:(?:[Ee]|[Ii])(?:(?:x|n)(?:clu(?:(?:de)|(?:sion))))|(?:(?:ne)?ligibility))(?: criteria)? (.*)")
  new_sents = []
  for sent in sents:
    crit = ' '.join([w for w in sent.split() if (w.lower().strip('\:') not in words_to_remove)])
    if len(crit) > 2:
      new_sents.append(crit)
  return new_sents




# -------------------------------------------------------------------------------------- #
# age processing utils
# -------------------------------------------------------------------------------------- #


def process_age_field(field_val):
  """
  desc: helper to call concvert_age_to_year.
        extracts unit and value from passed string taken from age field of doc 
  """
  age_match = AGE_PATTERN.match(field_val)
  if age_match is not None:
    age = float(age_match.group('age'))
    units = age_match.group('units')
    return convert_age_to_year(age, units)
  else:
    return None



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
  return age 





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
# ct structuring utils
# -------------------------------------------------------------------------------------- #


def alias_map(field_type):
  """
  field_type: str for directing key names, depending on include, exclude, or topics
  desc:       returns the appropriate field names for the alias creating process

  """
  if field_type == "include":
    crit_field = "include_criteria"
    ent_field = "inc_ents"
    alias_field = "inc_alias_crits"
  elif field_type == "exclude":
    crit_field = "exclude_criteria"
    ent_field = "exc_ents"
    alias_field = "exc_alias_crits"
  else:
    crit_field = "sents"
    ent_field = "ents"
    alias_field = "aliased_sents"
  return crit_field, ent_field, alias_field

  

# -------------------------------------------------------------------------------------- #
# print utils
# -------------------------------------------------------------------------------------- #

def print_crit(inc_elig: List[str], exc_elig: List[str]) -> None:
  print("\n\nINC CRIT")
  print('\n'.join(inc_elig))
  print("\nEXC CRIT")
  print('\n'.join(exc_elig))

