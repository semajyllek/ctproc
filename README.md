
This is a library for processing clinical trials data from clinicaltrials.gov
It offers methods for parsing the XML and content fields of the documents.  
The main api is through the `process_data` method, with default values shown here:

```
from clinproc import process_data

zip_data   = "/path/to/zip_folder"
write_file = "/path/to/write/file.jsonl"

processed_trials = process_data(
                       zip_data, 
                       write_file, 
                       concat=False, 
                       max_trials=1e7, 
                       start=-1, 
                       add_ents=True, 
                       mnegs=True, 
                       expand=True,
                       remove_stops=True,
                       id_to_print="", 
                       get_only=None
                   )
```

Output will be `.jsonl` format in that write location, one processed document per line.
This uses Zipfile so you don't have to uncompress your data.
Some usefule features are the text processing utilities built into the `process_data` routine.

spaCy's pipeline for text processing, is leveraged greatly, for entity linking, sentence segmentation, alias expansion, 
and negation. 

The field of utility to many is the 'eligibility/criteria/textblock` field, where the eligbility criteria are given in a
somewhat structured block of text like shown below. 

```
     Inclusion Criteria:
         -  Patients with HF or IHD who are not currently taking the study medications of
            interest (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD) and
            whose primary care physicians are part of the study population
     Exclusion Criteria:
         -  Patients who are unable or unwilling to give informed consent,
         -  previously taken the study medications according to dispensing records
         -  allergy or intolerance to study medications
         -  residents of long-term care facilities
         -  unable to confirm a diagnosis of either HF or IHD
         -  primary care physician has already contributed 5 patients to the study
 ```



In particular the library methods break the `eligbility/criteria/textblock``block of text into inclusion and exclusion criteria,
for further processing. This works in most cases but does break on difficult structures of this field where there are conditions of exclusion 
and inclusion mixed in with one another. It's also possible the structure could change entirely and other fields will come;
this project is not affiliated with clinicaltrials.gov in any way.

There are a number of different representations the method process_data() will return inside the processed document, turned on by default
unless args are specified like:

- concatenation into a single field of a user selected set of fields and subfields 
- mapping to UMLS CUI values: https://www.nlm.nih.gov/research/umls/index.html
- alias expansion from raw text associated with linked CUI values, with an attempt to maintain sentence structure
- an attempt at moving of negation in one criteria or the other to the oppsing field (inc -> exc, exc -> inc)
- removal of stopword or a list of words from the contents field constructed by the concatenation methods


Thank you so much for being interested in this project. I have a ton of things I want to do to it. First up make Document
objects instead of returning dictionaries, next make a more rigorous eligbility parser that can handle some of the more tricky cases in the data.

Please consider making a contribution if you think others would benefit!

https://github.com/semajyllek/clinproc



