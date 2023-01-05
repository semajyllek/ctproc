
import logging 

import re
import json
from lxml import etree
from typing import Dict, List, Optional, Set, Union

from clinproc.regex_patterns import AGE_PATTERN
from clinproc.utils import get_str_or_none, data_to_str, process_age_field, filter_words

logger = logging.getLogger(__file__)


class EligCrit:
    def __init__(self, raw_text: str) -> None:
        self.raw_text: str = raw_text
        self.include_criteria: List[str] = []
        self.exclude_criteria: List[str] = []
    


class CTDocument:
    def __init__(self, nct_id: str):
        self.nct_id: str = nct_id 
    
        self.aliased_crits: Optional[Dict[str, str]] = None
        self.aliased_sents: List[str] = []
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
        self.moved_negations: Optional[str] = None

    

        

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



    def concatenate_data(self, ignore_fields = [], grab_only_fields = [], lower=False) -> None:
        """
        results:  dictionary of string key, string, list, or dict values
        returns:  2 item dictionary of 'id', 'content' fields, where id is preserved
                  but all other values get concatenated into a single string value 
                  for 'contents' 
        """
        new_results = {'id':None, 'contents':None}
        contents = ""
        for field, value in self._asdict().items():
            if field == 'id':
                new_results['id'] = value
            else:
                if len(grab_only_fields) != 0:
                    if field in grab_only_fields:
                        contents += data_to_str(value, ignore_fields, grab_only_fields)
                    
                    elif (field not in ignore_fields):
                        contents += data_to_str(value, ignore_fields, grab_only_fields)
            
        contents = contents.strip() if not lower else contents.strip().lower()
        self.contents = re.sub('    ', ' ', contents)
        

    def move_negs(self):
        self.move_neg(inc_or_exc="inc")
        self.move_neg(inc_or_exc="exc")

    
    def entity_expand(self) -> None:
        if self.config.mnegs:
            self.move_negs()
        
        
        if self.config.expand:
            self.move_aliases("include")
            self.move_aliases("exclude")


 

    def process_doc_age(self, xml_root: etree.ElementTree) -> None:
        field_val = xml_root.find('eligibility/criteria/textblock')
        if field_val is None:
            logger.info("no age field exists for this document")
            
        self.age = process_age_field(field_val.text)
    