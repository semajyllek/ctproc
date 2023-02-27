# contains test_topic object for ctproc_tests.py

from ctproc.cttopic import CTTopic
from ctproc.ctbase import CTEntity

test_topic = CTTopic(
    id='1', 
    raw_text=' A 19-year-old male came to clinic with some sexual concern. He recently engaged in a relationship and is worried about the satisfaction of his girlfriend. He has a "baby face" according to his girlfriend\'s statement and he is not as muscular as his classmates. On physical examination, there is some pubic hair and poorly developed secondary sexual characteristics. He is unable to detect coffee smell during the examination, but the visual acuity is normal. Ultrasound reveals the testes volume of 1-2 ml. The hormonal evaluation showed serum testosterone level of 65 ng/dL with low levels of GnRH. ', 
)
test_topic.gender = 'male'
test_topic.age = 19.0
test_topic.text_sents = [
	' A 19-year-old male came to clinic with some sexual concern.', 
	'He recently engaged in a relationship and is worried about the satisfaction of his girlfriend.', 
	'He has a "baby face" according to his girlfriend\'s statement and he is not as muscular as his classmates.', 
	'On physical examination, there is some pubic hair and poorly developed secondary sexual characteristics.', 
	'He is unable to detect coffee smell during the examination, but the visual acuity is normal.', 
	'Ultrasound reveals the testes volume of 1-2 ml.', 
	'The hormonal evaluation showed serum testosterone level of 65 ng/dL with low levels of GnRH.'
] 
test_topic.filtered_sents = [
	'A 19-year-old male came clinic sexual concern.', 
	'He recently engaged relationship worried satisfaction girlfriend.', 
	'He "baby face" according girlfriend\'s statement muscular classmates.', 
	'On physical examination, pubic hair poorly developed secondary sexual characteristics.', 
	'He unable detect coffee smell examination, visual acuity normal.', 
	'Ultrasound reveals testes volume 1-2 ml.', 
	'The hormonal evaluation showed serum testosterone level 65 ng/dL low levels GnRH.'
]
test_topic.ent_sents = [[
		CTEntity(raw_text='male', label='ENTITY', start=15, end=19, cui={'val': 'C0086582', 'score': 1.0}, alias_expansion=['sex male', 'Male (finding)'], negation=False), 
		CTEntity(raw_text='clinic', label='ENTITY', start=28, end=34, cui={'val': 'C0002424', 'score': 0.9999999403953552}, alias_expansion=['Outpatient Care Facility', 'clinic outpatient'], negation=False), 
		CTEntity(raw_text='sexual concern', label='ENTITY', start=45, end=59, cui={'val': 'C0036864', 'score': 0.7529951930046082}, alias_expansion=['sexual behaviour', 'sexual behaviors'], negation=False), 
		CTEntity(raw_text='relationship', label='ENTITY', start=86, end=98, cui={'val': 'C0439849', 'score': 1.0}, alias_expansion=['Relationships (qualifier value)', 'Related'], negation=False), 
		CTEntity(raw_text='satisfaction', label='ENTITY', start=124, end=136, cui={'val': 'C0242428', 'score': 1.0}, alias_expansion=['Satisfied', 'fulfillment'], negation=False), 
		CTEntity(raw_text='girlfriend', label='ENTITY', start=144, end=154, cui={'val': 'C0521320', 'score': 1.0}, alias_expansion=['Girlfriend', 'girlfriend'], negation=False), 
		CTEntity(raw_text="girlfriend's statement", label='ENTITY', start=194, end=216, cui={'val': 'C0521320', 'score': 0.7549039125442505}, alias_expansion=['Girlfriend', 'girlfriend'], negation=False), 
		CTEntity(raw_text='muscular', label='ENTITY', start=234, end=242, cui={'val': 'C0442025', 'score': 0.9999998807907104}, alias_expansion=['Muscular', 'Muscular (qualifier value)'], negation=True), 
		CTEntity(raw_text='classmates', label='ENTITY', start=250, end=260, cui={'val': 'C0871683', 'score': 0.8928363919258118}, alias_expansion=[], negation=True), 
		CTEntity(raw_text='physical examination', label='ENTITY', start=265, end=285, cui={'val': 'C0031809', 'score': 1.0}, alias_expansion=['Physical Assessment', 'examination procedure'], negation=False), 
		CTEntity(raw_text='pubic', label='ENTITY', start=301, end=306, cui={'val': 'C0034014', 'score': 1.0}, alias_expansion=['Bones, Pubic', 'Pubis'], negation=False), 
		CTEntity(raw_text='hair', label='ENTITY', start=307, end=311, cui={'val': 'C0018494', 'score': 1.0}, alias_expansion=['HAIR', 'Pili'], negation=False), 
		CTEntity(raw_text='poorly', label='ENTITY', start=316, end=322, cui={'val': 'C0205169', 'score': 1.0}, alias_expansion=['badly', 'poorly'], negation=False), 
		CTEntity(raw_text='secondary', label='ENTITY', start=333, end=342, cui={'val': 'C0027627', 'score': 0.9999998807907104}, alias_expansion=['tumour metastasis', 'metastasized'], negation=False), 
		CTEntity(raw_text='sexual characteristics', label='ENTITY', start=343, end=365, cui={'val': 'C0036866', 'score': 0.8323554992675781}, alias_expansion=['Characteristic, Sex', 'Sex Characteristic'], negation=False), 
		CTEntity(raw_text='detect', label='ENTITY', start=383, end=389, cui={'val': 'C0442726', 'score': 1.0}, alias_expansion=['detected', 'detect'], negation=False), 
		CTEntity(raw_text='coffee', label='ENTITY', start=390, end=396, cui={'val': 'C0009237', 'score': 1.0}, alias_expansion=['coffea', 'Coffee (substance)'], negation=False), 
		CTEntity(raw_text='smell', label='ENTITY', start=397, end=402, cui={'val': 'C0037361', 'score': 1.0}, alias_expansion=['olfaction', 'Sense of smell, function'], negation=False), 
		CTEntity(raw_text='examination', label='ENTITY', start=414, end=425, cui={'val': 'C0031809', 'score': 1.0}, alias_expansion=['Physical Assessment', 'examination procedure'], negation=False), 
		CTEntity(raw_text='visual acuity', label='ENTITY', start=435, end=448, cui={'val': 'C0042812', 'score': 1.0}, alias_expansion=['Acuity, Visual', 'Resolving power of eye'], negation=False), 
		CTEntity(raw_text='normal', label='ENTITY', start=452, end=458, cui={'val': 'C0205307', 'score': 1.0}, alias_expansion=['UNREMARKABLE', 'Normal (qualifier value)'], negation=False), 
		CTEntity(raw_text='Ultrasound', label='ENTITY', start=460, end=470, cui={'val': 'C0041618', 'score': 1.0}, alias_expansion=['Ultrasound scan', 'Ultrasound Test'], negation=False), 
		CTEntity(raw_text='testes', label='ENTITY', start=483, end=489, cui={'val': 'C0021358', 'score': 1.0}, alias_expansion=['Posterior colliculus', 'Inferiors, Colliculus'], negation=False), 
		CTEntity(raw_text='volume', label='ENTITY', start=490, end=496, cui={'val': 'C0449468', 'score': 1.0}, alias_expansion=['Volume (property)', 'volumes'], negation=False), 
		CTEntity(raw_text='hormonal', label='ENTITY', start=512, end=520, cui={'val': 'C0458083', 'score': 1.0}, alias_expansion=['Hormonal (qualifier value)', 'Hormonal'], negation=False), 
		CTEntity(raw_text='evaluation', label='ENTITY', start=521, end=531, cui={'val': 'C0220825', 'score': 1.0}, alias_expansion=['efficacy assessment', 'effectiveness assessment'], negation=False), 
		CTEntity(raw_text='serum testosterone', label='ENTITY', start=539, end=557, cui={'val': 'C0428413', 'score': 1.0}, alias_expansion=['Serum testosterone measurement (procedure)', 'Serum testosterone level'], negation=False), 
		CTEntity(raw_text='level', label='ENTITY', start=558, end=563, cui={'val': 'C0441889', 'score': 1.0}, alias_expansion=['Degree', 'Levels'], negation=False), 
		CTEntity(raw_text='low', label='ENTITY', start=581, end=584, cui={'val': 'C0205251', 'score': 0.9999999403953552}, alias_expansion=['Low', 'Low (qualifier value)'], negation=False),
		CTEntity(raw_text='levels', label='ENTITY', start=585, end=591, cui={'val': 'C0441889', 'score': 1.0}, alias_expansion=['Degree', 'Levels'], negation=False), 
        CTEntity(raw_text='GnRH', label='ENTITY', start=595, end=599, cui={'val': 'C0023610', 'score': 1.0}, alias_expansion=['Gonadorelin (substance)', 'Luteinizing hormone releasing factor (LHRF) (LH/RF)'], negation=False)
]]
        
  
