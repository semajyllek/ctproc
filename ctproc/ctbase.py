
from typing import Any, Callable, Dict, Generator, List, NamedTuple, Optional, Set, Tuple
from ctproc.ctconfig import CTConfig


DONT_ALIAS = {"yo", "girl", "boy", "er", "changes", "patient", "male", "female", "age"}




class CTEntity(NamedTuple):
    raw_text: str
    label: str
    start: int
    end: int 
    cui: Dict[str, str]
    alias_expansion: List[str]
    negation: bool 



class NLPTools(NamedTuple):
	NLP: Callable
	linker: Any 
	STOP_WORDS: Set[str]
	

class CTBase:

	def __init__(self, id: str, nlp_tools: Optional[NLPTools] = None)-> None:
		self.id = id
		self.nlp_tools: Optional[NLPTools] = nlp_tools
		

	def get_ents(self, nlp_sent: Any, config: CTConfig) -> List[List[CTEntity]]:
		new_ent_sents = []
		for sent in nlp_sent:	
			ent_sent = [self.proc_spacy_ent(ent, config.max_aliases) for ent in sent.ents]
			new_ent_sents.append(ent_sent)
		
		return new_ent_sents


	def proc_spacy_ent(self, spacy_ent, max_aliases: int = 2) -> CTEntity:
		"""
		spacy_ent:    an Entity object returned by spaCy parser
		max_aliases:  max number of aliases to return, 
		              default 2 because more expands a lot and doesn't add much information
		desc:         converts to CTEntity object with select fields
		"""
		linker = self.nlp_tools.linker
		
		# only take first UMLS entity, others have lower scores and not likely to add information...
		umls_ent = spacy_ent._.kb_ents[0]
		aliases=linker.kb.cui_to_entity[umls_ent[0]]._asdict()['aliases']
		return CTEntity(
			raw_text=spacy_ent.text,
			label=spacy_ent.label_,
			start=spacy_ent.start_char,
			end=spacy_ent.end_char,
			cui={'val':umls_ent[0], 'score':umls_ent[1]},
			alias_expansion=aliases[:min(len(aliases), max_aliases)],
			negation=spacy_ent._.negex,
		)

	
	#----------------------------------------------------------------------------------------------#
	# methods for getting representations of eligibility criteria where aliases have been added
	#----------------------------------------------------------------------------------------------#

	def get_aliased_text(self, text_sent: str, ent_sent: List[CTEntity], dont_alias: Set[str] = DONT_ALIAS) -> str:
		"""
		text_sent:       the text sentence to be transformed into an aliased version
		ent_sent:          the entity repesentation of the sentence used to supply the aliases
		dont_alias:      by default, globally defined set of terms to not be aliased for noticable
						 domain errors, e.g. the term ER, included in many documents,
						 to endoplasmic reticulum
		desc:            returns a string with the entities in the text replaced (or expanded) with their aliases
		"""

		new_text = text_sent
		added = 0
		for ent in ent_sent:

			if ent.raw_text.lower()[:-1] in dont_alias:
					continue

			new_aliases = [a for a in self.get_new_aliases(ent)]
			if len(new_aliases) == 0:
				continue

			begin, end = self.get_ent_begin_and_end(new_text, ent.start + added)
			new_aliases = self.handle_right_alias_end(end, new_aliases)
			add_part = ' '.join(new_aliases)   
				
			if len(add_part) == 0:
				continue

			add_part = add_part + ' '     
			new_text = begin + add_part + end	
			added += len(add_part)
			
		return new_text


	def get_new_aliases(self, ct_ent: CTEntity) -> Generator[None, None, List[str]]:
		for alias in ct_ent.alias_expansion:
			alias = alias.lower().strip(',.?')
			if alias != ct_ent.raw_text.lower():
				yield alias


	def get_ent_begin_and_end(self, new_crit: str, ent_index: int) -> Tuple[str, str]:
		begin = new_crit[:ent_index]
		if not begin.endswith(' ') and (len(begin) > 0):
			begin += ' '
		end = new_crit[ent_index:]
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


