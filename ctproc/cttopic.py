
import logging

import re
from typing import Any, Callable, List, Optional

from ctproc.ctconfig import CTConfig
from ctproc.utils import filter_words
from ctproc.regex_patterns import TOPIC_AGE_GENDER_PATTERN
from ctproc.ctbase import CTBase, CTEntity, NLPTools

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


	def get_age_text(self) -> str:
		if self.text_sents is None:
			logger.info("no sentences, using raw text to get topic age")
			return self.raw_text
		return self.text_sents[0]

	def add_age_and_gender_data(self) -> None:
		age_text = self.get_age_text()
		m = TOPIC_AGE_GENDER_PATTERN.search(age_text)
		if m is not None:
			self.age = self.age_to_num_topic(float(m.group('age_val')), m.group('age_unit'))
			self.gender = self.map_to_gender_yuck(m.group('gender').strip())
		else:
			self.age = 999.0
			self.gender = "Any"

	def age_to_num_topic(self, val: float, unit: str) -> float:
		if unit == 'month':
			return val / 12.0
		if unit == 'week':
			return val / 52.0
		if unit == 'day':
			return val / 365.0
		return val

	def map_to_gender_yuck(self, label: str):
		m = {"boy", "male", "man"}
		f = {"girl", "female", "woman"}
		if label in m:
			return "male"
		if label in f:
			return "female"
		return "any"


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


            


		
		


