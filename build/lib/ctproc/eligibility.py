
import re
from ctproc.utils import clean_sentences
from ctproc.regex_patterns import INC_ONLY_PATTERN, EXC_ONLY_PATTERN, BOTH_INC_AND_EXC_PATTERN


#----------------------------------------------------------------#
# Eligibility Processing
#----------------------------------------------------------------#

def process_eligibility_naive(elig_text):
    """
    elig_text:    a block of raw text like this example:

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
    for h, chunk in enumerate(re.split(r'(?:[Ee]xclu(?:de|sion) criteria:?)|(?:[Ii]neligibility [Cc]riteria:?)', elig_text, flags=re.IGNORECASE)):
      for s in re.split(r'\n\n', chunk): 
        for ss in re.split(r'- ', s):
          ss = re.sub(r'\n   +', ' ', ss).strip()
          if len(ss) > 0:
            if h == 0:
              inc_crit.append(ss)
            else:
              exc_crit.append(ss)
      
    return clean_sentences(inc_crit), clean_sentences(exc_crit)



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
  while (i < len(sent_list)) and (re.match("exclu(?:sion|ded)", sent_list[i], flags=re.IGNORECASE) is None):
    i += 1
  return sent_list[:max(1,i)], sent_list[min(len(sent_list), i):]




