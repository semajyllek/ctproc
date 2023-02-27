
import logging 

import re
import json
from xml import etree
from typing import Any, Dict, Generator, List, NamedTuple, Optional, Set, Union

from ctproc.ctconfig import CTConfig
from ctproc.ctbase import CTBase, NLPTools
from ctproc.regex_patterns import AGE_PATTERN
from ctproc.utils import get_str_or_none, data_to_str, convert_age_to_year, filter_words

logger = logging.getLogger(__file__)



class EligCrit:
    def __init__(self, raw_text: str) -> None:
        self.raw_text: str = raw_text
        self.include_criteria: List[str] = []
        self.exclude_criteria: List[str] = []
        self.inc_aliased_crit: List[str] = []
        self.exc_aliased_crit: List[str] = []

    def __str__(self) -> str:
        return repr(f"raw_text:\n{self.raw_text}\ninclude_criteria:\n{self.include_criteria}\nexclude_criteria:\n{self.exclude_criteria}\n")
    


class CTDocument(CTBase):
    def __init__(self, nct_id: str, nlp_tools: Optional[NLPTools] = None):
        super().__init__(id=nct_id, nlp_tools=nlp_tools)

        self.brief_summary: Optional[str] = None
        self.brief_title: str = None 
        self.condition: Optional[str] = None
        self.condition_browse: Optional[str] = None
        self.contents: Optional[str] = None
        self.detailed_description: Optional[str] = None
        self.elig_crit: Optional[EligCrit] = None
        self.elig_gender: str = "All"
        self.elig_max_age: float = 999. 
        self.elig_min_age: float = 0. 
        self.intervention_browse_mesh_term: Optional[str] = None
        self.intervention_name: Optional[str] = None
        self.intervention_type: Optional[str] = None 


    def filter_crit(self, words_to_remove: Set[str]) -> None:
        """
        desc:    helper function to add versions of the criteria without stopwords to the doc
          """
        self.inc_filtered = [filter_words(sent, words_to_remove) for sent in self.elig_crit.include_criteria]
        self.exc_filtered = [filter_words(sent, words_to_remove) for sent in self.elig_crit.exclude_criteria]


    def get_text_fields(self, xml_root: etree.ElementTree) -> None:
        self.brief_summary = get_str_or_none("brief_summary/textblock", xml_root)
        self.detailed_description = get_str_or_none("detailed_description/textblock", xml_root)


    def make_content_field(self) -> None:
        """
        doc:     dict containing clinical trial information
        desc:    transfers the content of the summary field to the new `contents`
             field, if summary exists, otherwise contents field becomes emtpy string
        """
        summary = self.brief_summary
        self.contents = summary[0] if summary is not None else ""
        del self.brief_summary



    def concat_check(self, field: str, ignore_fields: List[str], grab_only_fields: List[str]) -> bool:
        if len(grab_only_fields) != 0:
            if field in grab_only_fields:
                return True
            return False
                 
        if field not in ignore_fields:
            return True
        return False

                    
    def concatenate_data(self, ignore_fields = [], grab_only_fields = [], lower=False) -> None:
        """
        results:  dictionary of string key, string, list, or dict values
        returns:  2 item dictionary of 'id', 'content' fields, where id is preserved
                  but all other values get concatenated into a single string value 
                  for 'contents' 
        """
        contents = ""
        for field, value in self._asdict().items():
            if self.concat_check(field, ignore_fields, grab_only_fields):
                contents += data_to_str(value, ignore_fields, grab_only_fields).strip()

        if lower:
            contents.lower()

        self.contents = re.sub('    ', ' ', contents)
        

    def expand_with_aliases(self):
        """
		desc:           uses entities and location from the spaCy pipeline process,
						with linked UMLS (CUI) terms, and there associated raw text forms
						it iserts these values into the sentence in the position where
						the entity is located, preserving the sentence except for the new
						semantic redundancy. syntactic redundancy is not avoided, as many terms 
						share value with other aliases, or the portion of the sentence being considered 
						(entities can span multiple tokens), except in the case where these 
						(possibly near) identical values are adjacent, in which case the last term of the 
						inserted material will be dropped before inserting. 
						**if max_ents > 1 this creates longer expanded sentences**

		"""
        
        self.elig_crit.inc_aliased_crit = [self.get_aliased_text(text_sent, ent_sent) for (text_sent, ent_sent) in zip(self.elig_crit.include_criteria, self.inc_ents)]
        self.elig_crit.exc_aliased_crit = [self.get_aliased_text(text_sent, ent_sent) for (text_sent, ent_sent) in zip(self.elig_crit.exclude_criteria, self.exc_ents)]



        
    def process_age_field(self, field_val) -> Optional[str]:
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



    def process_doc_age(self, xml_root: etree.ElementTree) -> None:
        min_age = self.process_doc_age_helper(xml_root, 'eligibility/minimum_age') 
        if min_age is not None:
             self.elig_min_age = min_age
        
        max_age = self.process_doc_age_helper(xml_root, 'eligibility/maximum_age')
        if max_age is not None:
            self.elig_max_age = max_age
    

    def process_doc_age_helper(self, xml_root: etree.ElementTree, age_field: str) -> None:
        field_val = xml_root.find(age_field)
        if field_val is None:
            logger.info("no age field exists for this document")
            return None
        age = self.process_age_field(field_val.text)
        return age
       

    def get_filtered_doc_as_dict(self) -> Dict[str, str]:
        """
        desc:    creates smaller, filtered versions of the documents for
                 some other types of uses
        """
        filtered = {}
        filtered['nct_id'] = self.nct_id
        filtered['min_age'] = self.elig_min_age
        filtered['max_age'] = self.elig_max_age
        filtered['gender'] = self.elig_gender
        filtered['include_cuis'] = ' '.join([ent['cui']['val'] for ent in self.inc_ents])
        filtered['exclude_cuis'] = ' '.join([ent['cui']['val'] for ent in self.exc_ents])
        return filtered 



    def add_nlp_features(self, config: CTConfig) -> None:
        if config.remove_stops:
            self.inc_filtered = [filter_words(sent, self.nlp_tools.STOP_WORDS) for sent in self.elig_crit.include_criteria]
            self.exc_filtered = [filter_words(sent, self.nlp_tools.STOP_WORDS) for sent in self.elig_crit.exclude_criteria]
    
        if config.add_ents:
            self.add_doc_ent_sents(config)
            
        if config.expand:
            self.expand_with_aliases()

            
    def add_doc_ent_sents(self, config: CTConfig) -> None:
        inc_nlp_sents = [self.nlp_tools.NLP(s) for s in self.elig_crit.include_criteria]
        exc_nlp_sents = [self.nlp_tools.NLP(s) for s in self.elig_crit.exclude_criteria]
        self.inc_ents = self.get_ents(inc_nlp_sents, config)
        self.exc_ents = self.get_ents(exc_nlp_sents, config)
