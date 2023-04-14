
import logging

from typing import Any, List, Optional

from ctconfig import CTConfig
from utils import filter_words, convert_age_to_year
from regex_patterns import TOPIC_AGE_PATTERN, TOPIC_GENDER_PATTERN
from ctbase import CTBase, CTEntity, NLPTools

logger = logging.getLogger(__file__)



class CTTopic(CTBase):
	def __init__(self, id: str, raw_text: str, nlp_tools: Optional[NLPTools] = None) -> None:
		super().__init__(id=id, nlp_tools=nlp_tools)
		self.raw_text: Optional[str] = raw_text
		self.text_sents: Optional[List[str]] = None
		self.filtered_sents: Optional[List[str]] = None
		self.ent_sents : Optional[List[List[CTEntity]]] = None
		self.age: Optional[float] = None
		self.gender: Optional[str] = None
		


	def get_age_and_gender_text(self) -> str:
		if self.text_sents is None:
			logger.info("no sentences, using raw text to get topic age")
			return self.raw_text
		return self.text_sents[0]


	def add_age_data(self, text: str) -> None:
		m = TOPIC_AGE_PATTERN.search(text)
		if m is not None:
			self.age = convert_age_to_year(float(m.group('age_val')), m.group('age_unit'))
		else:
			self.age = 999.0

	def add_gender_data(self, text: str) -> str:
		m = TOPIC_GENDER_PATTERN.search(text)
		if m is not None:
			self.gender = self.map_to_gender_yuck(m.group('gender').strip())
		else:
			self.gender = "All"

	def add_age_and_gender_data(self) -> None:
		text = self.get_age_and_gender_text()
		self.add_age_data(text)
		self.add_gender_data(text)


	def map_to_gender_yuck(self, label: str):
		m = {"boy", "male", "man", "M"}
		f = {"girl", "female", "woman", "F"}
		if label in m:
			return "Male"
		if label in f:
			return "Female"
		return "All"


	def add_nlp_features(self, config: CTConfig) -> None:
		nlp_sents = self.nlp_tools.NLP(self.raw_text)
		self.text_sents = [s.text for s in nlp_sents.sents]
		
		if config.remove_stops:
			self.filtered_sents = [filter_words(sent, self.nlp_tools.STOP_WORDS) for sent in self.text_sents]
			
		if config.add_ents:
			self.ent_sents = self.get_ents([nlp_sents], config)
			
		if config.expand:
			self.expand_with_aliases()


	def expand_with_aliases(self):
		"""
		desc:   expands the text and entities with aliases

		"""
		self.aliased_topic = [self.get_aliased_text(text_sent, ent_sent) for text_sent, ent_sent in zip(self.text_sents, self.ent_sents)]


            


		
		


