from typing import NamedTuple, Optional
from pathlib import Path


class CTConfig(NamedTuple):
  """
  zip_data:          str or path ending with .zip containing ct xml files (zipped)
  write_file:        path to write jsonl output
  concat:            bool, whether to concatenate al the grab_only fields into the contents field
  max_trials:        max number to get, useful for debugging and testing!
  start:             useful if your process gets interrupted and you don't want to start at the begining.
  add_ents:          bool, whether to get entitites with spaCY over the include, exclude criteria (once extracted)
  mnegs:             bool, whether to move negations
  expand:            bool, whether to expand terms in eligibility criteria, makes new alias_crits fields if True
  id_to_print:       str, for debugging, prints doc containing the id given  
  get_only:          list of strings, user can select which fields to grab, otherwise all fields grabbed 

  """
  zip_data: Path
  add_nlp: bool = True
  write_file: Path = 'ct_output.txt'
  concat: bool = False
  max_trials: float = 1e7
  start: int = -1
  add_ents: bool = True
  move_negations: bool = True
  expand: bool = True
  remove_stops: bool = True
  id_to_print: Optional[str] = None
  get_only: Optional[bool] = None
  save_data: bool = True

