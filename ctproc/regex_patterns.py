import re

CT_FILE_PATTERN = re.compile("\S+(NCT.*\.xml)")

EMPTY_PATTERN = re.compile(r'[\n\s]+')
INC_ONLY_PATTERN = re.compile(r'[\s\n]+[Ii]nclusion [Cc]riteria:?([\w\W ]*)')
EXC_ONLY_PATTERN = re.compile(r'[\n\r ]+[Ee]xclusion [Cc]riteria:?([\w\W ]*)')
AGE_PATTERN = re.compile(r'(?P<age>\d+) *(?P<units>\w+).*')
YEAR_PATTERN = re.compile(r'(?P<year>[yY]ears?.*)')
MONTH_PATTERN = re.compile(r'(?P<month>[mM]o(?:nth)?)')
WEEK_PATTERN = re.compile(r'(?P<week>[wW]eeks?)')

BOTH_INC_AND_EXC_PATTERN = re.compile(r'[\s\n]*[Ii]nclusion [Cc]riteria:?(?: +[Ee]ligibility[ \w]+\: )?(?P<include_crit>[ \n(?:\-|\d)\.\?\"\%\r\w\:\,\(\)]*)[Ee]xclusion [Cc]riteria:?(?P<exclude_crit>[\w\W ]*)')


TOPIC_ID_PATTERN = re.compile(r'.*<NUM>(?P<id>\d+)<\/NUM>\n\s+<TITLE>(?P<raw_text>.*)\n\s+<\/TOP>')
TOPIC_AGE_PATTERN = re.compile(r'(?P<age_val>\d+)[- ]?(?P<age_unit>[a-zY]+)?.*')
TOPIC_GENDER_PATTERN = re.compile(r'[ \d](?P<gender>woman|man|female|male|boy|girl|M|F) .*')


def test_regex(s: str) -> None:
	m = TOPIC_AGE_PATTERN.search(s)
	if m is not None:
		print(m.groupdict())
	else:
		print('no age match')

	m = TOPIC_GENDER_PATTERN.search(s)
	if m is not None:
		print(m.groupdict())
	else:
		print('no match')



if __name__ == '__main__':
	s1 = '70 y/o with COPD on 2.5-3.5L O2 at baseline, OSA and obesity hypoventilation syndrome, dCHF, discharged [**2132-8-24**] now presents with agitation and altered mental status with hypoxia and O2 sats 70s on BipAp with 5L.'
	s2 = ''
	s3 = '64yo woman with multiple myeloma, s/p allogeneic transplant with recurrent disease and with systemic amyloidosis (involvement of lungs, tongue, bladder, heart), on hemodialysis for ESRD who represents for malaise, weakness, and generalized body aching x 2 days.'
	s4 = '74M hx of CAD s/p CABG, EF 60% prior CVA (no residual deficits), HTN, HL, DMII, Moderate to Severe PVD was referred to cardiology for evaluation of PVD, and on examination patient was found to have carotid bruits.'
	s5 = 'A 31 yo male with no significant past medical history presents with productive cough and chest pain.'
	s6 = 'A 31 yo man with no significant past medical history presents with productive cough and chest pain.'
	s7 = 'A 6 year old girl who has pain in her right knee for 2 days.'
	s8 = 'A 6 month old boy who has pain in their right knee for 2 days.'
	s9 = 'A 6 day old boy who has pain in his right knee for 2 days.'
	s10 = 'A 6 day old who has pain in his right knee for 2 days.'
	s11 = '13F with history of asthma, allergic rhinitis, and GERD presents with a 2 day history of cough, fever, and shortness of breath.'

	test_regex(s11)

  