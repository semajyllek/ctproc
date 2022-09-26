
from typing import List



#----------------------------------------------------------------#
# Getting CUI's
#----------------------------------------------------------------#

def get_ents(sent_list: List[str], nlp, top_N: int = 2):
  """
  sent_list: list of sentence strings
  top_N:     int directing how many aliaseed terms to get
  desc:      uses spaCy pipeline to get entities and link them to terms,
             adds this information, entities lists of the sentences, 
             as a newa_field to the doc
  """
  new_ent_sents = []
  for sent in sent_list:
    nlp_sent = nlp(sent)
    new_ents = []
    for ent in nlp_sent.ents:
      for umls_ent in ent._.kb_ents:
        new_ent = {}
        new_ent['raw_text'] = ent.text
        new_ent['label'] = ent.label_
        new_ent['start'] = ent.start_char
        new_ent['end'] = ent.end_char
        new_ent['cui'] = {'val':umls_ent[0], 'score':umls_ent[1]}
        aliases = linker.kb.cui_to_entity[umls_ent[0]]._asdict()['aliases']
        new_ent['alias_expansion'] = aliases[:min(len(aliases), top_N)]
        new_ent["negation"] = ent._.negex
        #new_ent['covered_text'] = linker.kb.cui_to_entity[umls_ent[0]]
        new_ents.append(new_ent)
        break   # only get first one
    new_ent_sents.append(new_ents)
    
      
  return new_ent_sents



def add_entities(ct_doc, top_N=2):
  """
  desc:    helper function to add the entities got from get_entities() to the doc
  """
  ct_doc.inc_ents = get_ents(ct_doc.elig_crit.include_criteria, top_N)
  ct_doc.exc_ents = get_ents(ct_doc.elig_crit.exclude_criteria, top_N)
  return ct_doc

