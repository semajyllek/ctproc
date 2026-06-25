
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from pprint import pprint

from ctmatch_utils import get_processed_data
from proc import CTConfig, CTProc, CTDocument, CTTopic
from scripts.vis_scripts import (
  analyze_test_rels
)




def proc_docs(doc_path: str, output_path: str) -> Dict[str, CTDocument]:

	ct_config = CTConfig(
		data_path=doc_path, 
		write_file=output_path,
    	nlp=True
	)

	cp = CTProc(ct_config)
	id2doc = {res.id : res for res in cp.process_data()}
	return id2doc



def proc_topics(topic_path: str, output_path: str) -> Dict[str, CTTopic]:
	
	ct_config = CTConfig(
		data_path=topic_path, 
		write_file=output_path,
    	nlp=True,
    	is_topic=True,
	)

	cp = CTProc(ct_config)
	id2topic = {res.id : res for res in cp.process_data()}
	return id2topic


def get_doc_data_tuples() -> List[Tuple[str]]:
	trec22_pt1_docs = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_docs_21/ClinicalTrials.2021-04-27.part1.zip'
	trec_pt1_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part1.jsonl'

	trec22_pt2_docs = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_docs_21/ClinicalTrials.2021-04-27.part2.zip'
	trec_pt2_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part2.jsonl'

	trec22_pt3_docs = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_docs_21/ClinicalTrials.2021-04-27.part3.zip'
	trec_pt3_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part3.jsonl'

	trec22_pt4_docs = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_docs_21/ClinicalTrials.2021-04-27.part4.zip'
	trec_pt4_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part4.jsonl'

	trec22_pt5_docs = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_docs_21/ClinicalTrials.2021-04-27.part5.zip'
	trec_pt5_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part5.jsonl'

	data_tuples = [
		(trec22_pt1_docs, trec_pt1_target), 
		(trec22_pt2_docs, trec_pt2_target), 
		(trec22_pt3_docs, trec_pt3_target),
		(trec22_pt4_docs, trec_pt4_target),
		(trec22_pt5_docs, trec_pt5_target)
	]
	
	return data_tuples


def get_topic_data_tuples() -> List[Tuple[str]]:
	trec21_topic_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_21_topics.xml'
	trec21_topic_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec21_topics.jsonl'
	trec22_topic_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_22_topics.xml'
	trec22_topic_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_topics.jsonl'

	data_tuples = [
		(trec21_topic_path, trec21_topic_target), 
		(trec22_topic_path, trec22_topic_target)
	]
	return data_tuples


def age_match(min_doc_age: float, max_doc_age: float, topic_age: float) -> bool:
	if topic_age < min_doc_age:
		return False
	if topic_age > max_doc_age:
		return False
	return True

def gender_match(doc_gender: str, topic_gender: str) -> bool:
	if doc_gender == 'All':
		return True
	if doc_gender == topic_gender:
		return True
	return False


def explore_pairs(id2topic: Dict[str, Dict[str, str]], id2relled_docs: Dict[str, Dict[str, str]], trec_rel_dict: Dict[str, Dict[str, str]], max_print:int = 1000) -> None:
	rel_scores = defaultdict(int)
	age_mismatches, gender_mismatches = 0, 0
	i = 0

	for pt_id, topic in id2topic.items():
		for doc_id in trec_rel_dict[pt_id]:
			if doc_id in id2relled_docs:
				rel_score = trec_rel_dict[pt_id][doc_id]
				rel_scores[rel_score] += 1
				if rel_score == 2:
					doc = id2relled_docs[doc_id]

					
					
					age_matches = age_match(doc['elig_min_age'], doc['elig_max_age'], topic['age'])
					if not age_matches:
						print(f"\nage mismatch\n")
						print('*'*200)
						print(f"topic id: {pt_id}, nct_id: {doc['id']}, rel score: {rel_score}")
						print(f"topic info: \nage: {topic['age']}, gender: {topic['gender']}")
						print(topic['raw_text'])
						print(f"doc info: gender: {doc['elig_gender']}, min age: {doc['elig_min_age']}, max age: {doc['elig_max_age']}")
						print(doc['elig_crit']['raw_text'])
						age_mismatches += 1

					gender_matches = gender_match(doc['elig_gender'], topic['gender'])
					if not gender_matches:
						print(f"\ngender mismatch!!\n")
						gender_mismatches += 1

					
					i += 1
					if i == max_print:
						return


	print(rel_scores.items())
	print(f"{age_mismatches=}, {gender_mismatches=}")


				

def proc_trec_docs_and_topics():

	# process trec22 relevancy judgements
	trec_rel_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_21_judgments.txt'
	type_dict, trec_rel_dict, all_qrelled_docs = analyze_test_rels(trec_rel_path)

	id2topic = dict()
	for source, target in get_topic_data_tuples():
		id2topic += proc_topics(topic_path, topic_target)
		print(f"processed topic source: {source}, and wrote to {target}")
	
	id2doc = dict()
	for source, target in get_doc_data_tuples():
		id2doc += proc_docs(source, target)
		print(f"processed doc source: {source}, and wrote to {target}")




if __name__ == '__main__':
	# process trec21 relevancy judgements
	#trec_rel_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_21_judgments.txt'
	#type_dict, trec_rel_dict, all_qrelled_docs = analyze_test_rels(trec_rel_path)

	topic_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/trec_22_topics.xml'
	topic_target = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_topics.jsonl'
	id2topic = proc_topics(topic_path, topic_target)
	

	# processed_topics_path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec21_topics.jsonl'
	# id2topic = {t['id']:t for t in get_processed_data(processed_topics_path)}

	# processed1path = '/Users/jameskelly/Documents/cp/ctmatch/data/trec_data/processed_trec_data/processed_trec22_docs_part1.jsonl'
	# id2relled_docs1 = {doc['id']:doc for doc in get_processed_data(processed1path, get_only=all_qrelled_docs)}

	# explore_pairs(id2topic, id2relled_docs1, trec_rel_dict, max_print=1000)


					






