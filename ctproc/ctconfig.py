from typing import NamedTuple, Optional, Set
from pathlib import Path


class CTConfig(NamedTuple):
  """
  zip_data:          str or path ending with .zip containing ct xml files (zipped)
  id_to_print:       str, for debugging, prints doc containing the id given 
  add_nlp:           bool as to whether to load the en_core_sci_md model and possibly add transformed features,
                     depending on which of the "nlp" args are set,  namely {remove_stops, add_ents, move_negations, expand}
  write_file:        path to write jsonl output
  max_trials:        max number to get, useful for debugging and testing!
  start:             useful if your process gets interrupted and you don't want to start at the begining.
  get_only:          set of strings, user can select which fields to grab, otherwise all fields grabbed 
  skip_ids:          set of strings, user can select which NCT id's to skip

  remove_stops:      bool, whether to use spaCy's set of stop words to filter the criteria strings
  add_ents:          bool, whether to get entitites with spaCY over the include, exclude criteria (once extracted)
  ent_max:           int, how many related aliases to get from the entity search
  move_negations:    bool, whether to move negations from inc to exc criteria or vice versa
  expand:            bool, whether to expand terms in eligibility criteria, makes new alias_crits fields if True
 
  
  concat:             bool, whether to concatenate al the grab_only fields into the contents field
  make_content: 

  """
  zip_data: str
  id_to_print: Optional[str] = None
  add_nlp: bool = False
  write_file: Path = 'ct_output.txt'
  max_trials: float = 1e7
  start: int = -1
  get_only: Optional[Set[str]] = None
  skip_ids: Set[str] = set()

  # nlp configs
  remove_stops: bool = True
  add_ents: bool = True
  max_ents: int = 2
  move_negations: bool = True
  expand: bool = False
  
  concat: bool = False
  save_data: bool = True




