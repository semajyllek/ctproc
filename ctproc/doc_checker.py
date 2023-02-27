# ----------------------------------------------------------------------------------------------- #
# file contains object with simple @classmethods for doing various tests on documents and topics
# ----------------------------------------------------------------------------------------------- #


import logging
from pathlib import Path
from typing import Optional
from ctproc.ctconfig import CTConfig
from ctproc.ctdocument import CTDocument

logger = logging.getLogger(__file__)

class DocChecker:
	
	#inital check

	@staticmethod
	def iter_check(iter: int, config: CTConfig) -> bool:
		if iter < config.max_trials:
			if iter >= config.start:
				return True
		return False
		
	# checks that occur prior to document creation

	@staticmethod
	def combined_predoc_check(ct_file: str, config: CTConfig) -> bool:
		if not (DocChecker.file_check(ct_file) and DocChecker.id_check(ct_file, config)):
			return False
		return True
		
	@staticmethod
	def file_check(ct_file: str) -> bool:
		if not ct_file.endswith('xml'):
			return False
		return True

	@staticmethod	
	def id_check(ct_file: str, config: CTConfig) -> bool:
		nct_id = Path(ct_file).name[:-4]
		if (config.get_only is not None) and (nct_id not in config.get_only):
			return False
			
		if nct_id in config.skip_ids:
			return False
		return True
		
	# checks that occur during creation of doc  

	@staticmethod
	def combined_doc_check(doc: Optional[CTDocument]) -> bool:
		return DocChecker.existence_check(doc) and DocChecker.elig_check(doc)
		
	@staticmethod
	def existence_check(doc: Optional[CTDocument]) -> bool:
		if doc is None:
			return False
		return True
		
	@staticmethod
	def elig_check(doc: CTDocument) -> bool:
		if doc.elig_crit is None:
			logger.info("no eligibility crit!!!")
			return False
		return True



		