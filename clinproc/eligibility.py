
import re
from utils import clean_sentences, check_sentences
from regex_patterns import INC_ONLY_PATTERN, EXC_ONLY_PATTERN, BOTH_INC_AND_EXC_PATTERN


#----------------------------------------------------------------#
# Eligibility Processing
#----------------------------------------------------------------#

def process_eligibility(elig_text):
  """
  desc:  this version is not the default for the package and may work in some 
          cases where the naive version fails. it relies heavily on sometimes 
          complicated regex patterns

  """

  if elig_text is not None:
    if re.search('[Ii]nclusion [Cc]riteria:[^\w]+\n', elig_text):
      if re.search('[Ee]xclusion Criteria:[^\w]+\n', elig_text):
        inc_raw_text, exc_raw_text = BOTH_INC_AND_EXC_PATTERN.match(elig_text).groups()
        include_criteria = clean_sentences(re.split('\-  ', inc_raw_text))
        exclude_criteria = clean_sentences(re.split('\-  ', exc_raw_text))

        if len(exclude_criteria) == 0:
          num_sep_include_criteria = clean_sentences(re.split('[1-9]\.  ', inc_raw_text))
          num_sep_exclude_criteria = clean_sentences(re.split('[1-9]\.  ', exc_raw_text))
          if len(num_sep_exclude_criteria) > 0:
            include_criteria = num_sep_include_criteria
            exclude_criteria = num_sep_exclude_criteria

        include_criteria = check_sentences(include_criteria)
        exclude_criteria = check_sentences(exclude_criteria)
        return (include_criteria, exclude_criteria)

      else:
        include_criteria = INC_ONLY_PATTERN.match(elig_text).groups(0)[0]
        include_criteria = re.split('\-  +', include_criteria)
        include_criteria = check_sentences(clean_sentences(include_criteria))
        return (include_criteria, [])

    elif re.search('[Ee]xclusion [Cc]riteria:[^\w]+\n', elig_text):
      exclude_criteria = EXC_ONLY_PATTERN.match(elig_text).groups(0)
      exclude_criteria = check_sentences(clean_sentences(re.split('\-  +', exclude_criteria)))
      return ([], exclude_criteria)
    
    else:
      return naive_split_inc_exc(get_sentences(clean_sentences([elig_text])[0]))



def process_eligibility_naive(elig_text):
    """
    elig_text:    a block of raw text like -

      Inclusion Criteria:

        -  Men and women over the age of 18

        -  Skin lesion suspected to either BCC or SCC etc

        -  Patient was referred for biopsy diagnostic/therapeutic before hand, and regardless of
            confocal microscope examination, according to the clinical consideration of physician

      Exclusion Criteria:

        -  Pregnant women

        -  Children

    This script uses regex patterns to split this into inclusion and exclusion, 
    gets the sentences, cleans them, checks them for whether they contain 
    any information once extracted and cleaned, in which case they will be removed.



    """
    inc_crit, exc_crit = [], []
    for h, chunk in enumerate(re.split(r'(?:[Ee]xclu(?:de|sion))|(?:[Ii]neligibility) [Cc]riteria:?', elig_text)):
      for s in re.split(r'\n *(?:\d+\.)|(?:\-) ', chunk):
        if h == 0:
          inc_crit.append(s)
        else:
          exc_crit.append(s)
    
    clean_inc = clean_sentences(inc_crit)
    clean_exc = clean_sentences(exc_crit)
    return check_sentences(clean_inc), check_sentences(clean_exc)



def naive_split_inc_exc(sent_list):
  """
  sent_list:   list of sentence strings
  desc:        given a list of sentences, determines where to partition 
                into inclusion, exclusion criteria solely by the presence of 
                the string that the exclusion matern matches against.
                Note: some docs contain only inclusion criteria, others only 
                exclusion criteria, most both. This version is used in the more 
                complicated splitting procedure above, and is not default.
  """
  i = 0
  while (i < len(sent_list)) and (re.match("[Ee]xclu(?:sion|ded)", sent_list[i]) is None):
    i += 1
  return sent_list[:max(1,i)], sent_list[min(len(sent_list), i):]




