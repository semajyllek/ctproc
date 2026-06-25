# contains eligibility criteria strings for testing in ctprop_test.py


#-------------------------------------------------------------------------------------------#
# 1. "normal" criteria statements with dashes and clear semi-structure
# ------------------------------------------------------------------------------------------#


normal_raw   =  """
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
                  """

norm_inc_crit = [
  "Patients with HF or IHD who are not currently taking the study medications of interest" \
  + " (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD)" \
  + " and whose primary care physicians are part of the study population"
]


norm_exc_crit = [
  'Patients who are unable or unwilling to give informed consent', 
  'previously taken the study medications according to dispensing records', 
  'allergy or intolerance to study medications', 
  'residents of long-term care facilities', 
  'unable to confirm a diagnosis of either HF or IHD', 
  'primary care physician has already contributed 5 patients to the study'
]






#-------------------------------------------------------------------------------------------#
# 2. raw text contains only inclusion criteria (uses norm_inc_crit above)
# ------------------------------------------------------------------------------------------#

inc_only_raw  =  """
                    Inclusion Criteria:
                         -  Patients with HF or IHD who are not currently taking the study medications of
                            interest (ACE inhibitors/angiotensin receptor blockers for HF or statins for IHD) and
                            whose primary care physicians are part of the study population
                  """




#-------------------------------------------------------------------------------------------#
# 3. raw text contains only exclusion criteria (uses norm_exc_crit above)
# ------------------------------------------------------------------------------------------#


exc_only_raw   =  """
                  Exclusion Criteria:
                      -  Patients who are unable or unwilling to give informed consent,
                      -  previously taken the study medications according to dispensing records
                      -  allergy or intolerance to study medications
                      -  residents of long-term care facilities
                      -  unable to confirm a diagnosis of either HF or IHD
                      -  primary care physician has already contributed 5 patients to the study
                """


#---------------------------------------------------------------------------#
# 5. test 5 is on the empty raw text field
# --------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
# 5. spaced with dashes variation (from NCT01414829)
# --------------------------------------------------------------------------#

normal_spaced_raw  =  """
          Inclusion Criteria:

          -  all referred for gastroscopy with clinical or endoscopic signs of peptic disease

        Exclusion Criteria:

          -  coagulation disorders

          -  pregnant women

"""

norm_spaced_inc_crit = [
  'all referred for gastroscopy with clinical or endoscopic signs of peptic disease'
]

norm_spaced_exc_crit = [
  'coagulation disorders',
  'pregnant women'
]



#---------------------------------------------------------------------------#
# 6. spaced with no dashes variation (artificially from NCT01414829)
# --------------------------------------------------------------------------#


normal_no_dash_raw   =  """
                
          Inclusion Criteria:

           all referred for gastroscopy with clinical or endoscopic signs of peptic disease

        Exclusion Criteria:

           coagulation disorders

           pregnant women
""" 


norm_no_dash_inc_crit = [
  'all referred for gastroscopy with clinical or endoscopic signs of peptic disease'
]

norm_no_dash_exc_crit = [
  'coagulation disorders',
  'pregnant women'
]



#-----------------------------------------------------------------------------------------#
# 7. numbered subcriteria variation (slightly modified for tighter testing from NCT01414829)
# - also skips last semantically empty criteria with hacky code
# ----------------------------------------------------------------------------------------#



sub_numbers_raw = """
        Inclusion Criteria:

          -  History of liver steatosis during the preceding 24 months

          -  History of fasting TGs > 200 mg/dL (confirmed at screening).

          -  Liver fat ≥ 10% as determined by the central MRI laboratory.

          -  Subjects on the following medications can be included if these medications are
             medically necessary, cannot be stopped and the investigator feels their dose will
             remain stable for the duration of the double-blind treatment period:

               1. Stable dose of anti-diabetic medications (metformin and/or sulfonylureas) for at
                  least 8 weeks prior to screening.

               2. Stable doses of beta-blockers and thiazide diuretics for at least 8 weeks prior
                  to screening.
 

        Exclusion Criteria:

          -  Treatment with omega-3-acid ethyl esters or omega-3-polyunsaturated fatty acid
             (PUFA)-containing supplements > 200 mg per day within 8 weeks of screening.

          -  Treatment with antiretrovirals, tamoxifen, methotrexate, cyclophosphamide,
             isotretinoin, bile acid binding resins or pharmacologic doses of oral glucocorticoids
             (≥10 mg of prednisone per day or equivalent) within 8 weeks of screening.

        Other protocol defined inclusion/exclusion criteria may apply
      
"""

sub_numbers_inc_crit = [
  'History of liver steatosis during the preceding 24 months',
  'History of fasting TGs > 200 mg/dL (confirmed at screening)',
  'Liver fat ≥ 10% as determined by the central MRI laboratory',
  'Subjects on the following medications can be included if these medications are medically necessary, cannot be stopped and the investigator feels their dose will remain stable for the duration of the double-blind treatment period',
  'Stable dose of anti-diabetic medications (metformin and/or sulfonylureas) for at least 8 weeks prior to screening',
  'Stable doses of beta-blockers and thiazide diuretics for at least 8 weeks prior to screening'
]

sub_numbers_exc_crit = [
  'Treatment with omega-3-acid ethyl esters or omega-3-polyunsaturated fatty acid (PUFA)-containing supplements > 200 mg per day within 8 weeks of screening',
  'Treatment with antiretrovirals, tamoxifen, methotrexate, cyclophosphamide, isotretinoin, bile acid binding resins or pharmacologic doses of oral glucocorticoids (≥10 mg of prednisone per day or equivalent) within 8 weeks of screening'
]






#-----------------------------------------------------------------------------------------#
# 8. all caps headers variation (from NCT00902733)
# ----------------------------------------------------------------------------------------#

headers_raw = """
        DISEASE CHARACTERISTICS:

          -  Diagnosis of pancreatic cancer (all stages)

        PATIENT CHARACTERISTICS:

          -  Admitted to City of Hope National Medical Center

               -  Resides within a 30-mile radius of the medical center

          -  No prior cancer

        PRIOR CONCURRENT THERAPY:

          -  No prior therapy
      
"""

headers_inc_crit = [
  'Diagnosis of pancreatic cancer (all stages)',
  'Admitted to City of Hope National Medical Center',
  'Resides within a 30-mile radius of the medical center',
  'No prior cancer',
  'No prior therapy'
]

headers_exc_crit = []






#-----------------------------------------------------------------------------------------#
# 9. no dash + sub numbering in exclusion criteria (from NCT02352805)
# ----------------------------------------------------------------------------------------#

no_dash_sub_numbers_raw = """
       Inclusion Criteria:

        Need for therapy with extracorporeal circulation / circulatory support due to cardiac
        failure, or lung failure, or renal failure, or a combination of these diseases

        Exclusion Criteria:

          1. History of previously diagnosed hereditary coagulation and/or platelet disorders

          2. Refusal to receive blood transfusion

          3. Participation in other clinical research studies involving evaluation of other
             investigational drugs or devices within 30 days of randomization

          4. Diagnosis of hepatitis B, hepatitis C, and HIV

          5. Age > 85 years
      
"""

no_dash_sub_numbers_inc_crit = [
  'Need for therapy with extracorporeal circulation / circulatory support due to cardiac failure, or lung failure, or renal failure, or a combination of these diseases'
]

no_dash_sub_numbers_exc_crit = [
  'History of previously diagnosed hereditary coagulation and/or platelet disorders',
  'Refusal to receive blood transfusion',
  'Participation in other clinical research studies involving evaluation of other investigational drugs or devices within 30 days of randomization',
  'Diagnosis of hepatitis B, hepatitis C, and HIV',
  'Age > 85 years'   
]





#-------------------------------------------------------------------------------------------#
# 10. individually labelled criteria (from NCT01145885) 
# - note how the word Criteria gets wrongly removed from the words in 'Inclusion Criteria 6' 
# ------------------------------------------------------------------------------------------#


indv_label_raw = """
       Inclusion criteria:

          -  Inclusion Criteria 1. Patients with histologically or cytologically confirmed
             diagnosis of advanced, non resectable and / or metastatic solid tumour

          -  Inclusion Criteria 2. Male

          -  Inclusion Criteria 3. Age >=18 and =<70 years

          -  Inclusion Criteria 4. Written informed consent

          -  Inclusion Criteria 5. Eastern Cooperative Oncology Group (ECOG) performance score =<2

          -  Inclusion Criteria 6. Recovery from Common Terminology Criteria for Adverse Events
             (CTCAE) Grade >=2 therapy-related toxicities from previous chemo-, hormone-, immuno-,
             or radiotherapy

        Exclusion criteria:

          -  Exclusion Criteria 1. Serious concomitant non-oncological disease considered by the
             investigator

          -  Exclusion Criteria 2. Active infectious disease

          -  Exclusion Criteria 3. Viral hepatitis, Human Immunodeficiency Virus (HIV) infection

"""

indv_label_inc_crit = [
  'Patients with histologically or cytologically confirmed diagnosis of advanced, non resectable and / or metastatic solid tumour',
  'Male',
  'Age >=18 and =<70 years',
  'Written informed consent',
  'Eastern Cooperative Oncology Group (ECOG) performance score =<2',
  'Recovery from Common Terminology for Adverse Events (CTCAE) Grade >=2 therapy-related toxicities from previous chemo-, hormone-, immuno-, or radiotherapy'
]


indv_label_exc_crit = [
  'Serious concomitant non-oncological disease considered by the investigator',
  'Active infectious disease',
  'Viral hepatitis, Human Immunodeficiency Virus (HIV) infection'
]




#-------------------------------------------------------------------------------------------#
# 11. dash and all caps header like 
# - INCLUSION CRITERIA:
#    ...
# (from NCT00362167) 
# ------------------------------------------------------------------------------------------#


dash_and_header_raw = """
        -  INCLUSION CRITERIA:

        Patients of 4 years of age and older, both genders, and all racial/ethnic groups with
        acute or chronic pain that will help the Branch fulfill its objectives.

        Women of childbearing potential, or who are pregnant or lactating, will only undergo tests
        and procedures, and/or receive medications for which data exists proving minimal risk to
        the fetus. The diagnostic tests will only include medically-indicated radiation exposure.

        Referral is needed from the patients' physician or dentist.

        EXCLUSION CRITERIA:

        Patients with significant cognitive impairment.

        Pregnancy or lactation, if this status precludes proposed diagnostic procedures or
        therapies.

        Patients with serious organ system dysfunction (e.g. heart failure, ischemic heart
        disease).
      
"""


dash_and_header_inc_crit = [
  'Patients of 4 years of age and older, both genders, and all racial/ethnic groups with acute or chronic pain that will help the Branch fulfill its objectives',
  'Women of childbearing potential, or who are pregnant or lactating, will only undergo tests and procedures, and/or receive medications for which data exists proving minimal risk to the fetus. The diagnostic tests will only medically-indicated radiation exposure',
  "Referral is needed from the patients' physician or dentist"
]

dash_and_header_exc_crit = [
  'Patients with significant cognitive impairment',
  'Pregnancy or lactation, if this status precludes proposed diagnostic procedures or therapies',
  'Patients with serious organ system dysfunction (e.g. heart failure, ischemic heart disease)' 
]



#-------------------------------------------------------------------------------------------#
# 12. include statement contains an exclude statement. 
#     this is problematic because the current program removes these words,
#     note the erroneous change:
#     'Exclusion of differential diagnoses' -> 'of differential diagnoses'
#  (from NCT02196155)
# ------------------------------------------------------------------------------------------#

exc_in_inc_raw = """
        Inclusion Criteria:

          -  Exclusion of differential diagnoses

          -  Written informed consent

        Exclusion Criteria

          -  Active differential diagnoses

          -  Neurological diseases affecting the peripheral nervous system
      
"""

exc_in_inc_inc_crit = [
  'of differential diagnoses',
  'Written informed consent'
]

exc_in_inc_exc_crit = [
  'Active differential diagnoses',
  'Neurological diseases affecting the peripheral nervous system'
]


#-------------------------------------------------------------------------------------------#
# 13. numbered criteria with no spaces (from NCT00387855)
# ------------------------------------------------------------------------------------------#

num_no_space_raw = """
        Inclusion Criteria:

          1. Attendance at school participating in study

          2. English speaking youth with parental consent.

        Exclusion Criteria:

        1.Youth who do not speak and read English
      
"""

num_no_space_inc_crit = [
  'Attendance at school participating in study',
  'English speaking youth with parental consent'
]

num_no_space_exc_crit = [
  'Youth who do not speak and read English'
]


