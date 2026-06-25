from collections import Counter
from typing import Set

def get_word_counts(docs):
  """
  docs:       list of dicts contasining clinical trial data
  """
  all_words = []
  for doc in docs:
    for inc_sent in doc["eligibility/criteria/textblock"]['include_criteria']:
      all_words += [w.lower() for w in inc_sent.split()]
    
    for exc_sent in doc["eligibility/criteria/textblock"]['exclude_criteria']:
      all_words += [w.lower() for w in exc_sent.split()]

  return Counter(all_words)


def filter_out_stop_counts(word_counts, stopwords: Set[str]):
  """
  word_counts:     dict[str, int]
  desc:            removes a globally defined fixed set of words from spaCy library from word count dicts
  """
  for word in stopwords:
    if word in word_counts:
      del word_counts[word]
  return word_counts
