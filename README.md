
### Project Description & API

This is a library for processing clinical trials data from clinicaltrials.gov
It offers methods for parsing the XML and content fields of the documents.  
The main api is through the `process_data` method, with default values shown here:

```
from ctproc import CTConfig, CTProc

zip_data   = "/path/to/zip_folder"
write_file = "/path/to/write/file.jsonl"

id_ = 'NCT00001444'
config = CTConfig(
    zip_data=zip_data, 
    write_file=write_file,
    id_to_print=id_, 
    max_trials=25,
    add_nlp=True       # must have en_core_sci_md spaCy model installed
)

cp = ClinProc(config)
id2doc = {res.nct_id : res for res in cp.process_data()}
id_doc = id2doc[id_]

print(id_doc.elig_crit.include_criteria)


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

### Installation

You can use pip to install,
```
pip install ctproc
```

But due to pypi limitations to not including linked libraries, you will need to install the spaCy `en_core_sci_md` model like:
```
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_md-0.5.1.tar.gz
```

\*Note that the initial `import ctproc` will take a few minutes due to having to load the scispacy model.

### What it Does:

In particular the library methods break the `eligbility/criteria/textblock` block of text into inclusion and exclusion criteria,
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



TODO:

- construct a module to identify labs and ranges in the criteria data (to be used by ctmatch to match with values in the patient descriptions)


https://github.com/semajyllek/ctproc



