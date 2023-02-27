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
TOPIC_AGE_GENDER_PATTERN = re.compile(r'(?P<age_val>\d+)(([- ](?P<age_unit>[^-]+)[- ]old)| ?y\.?o\.?).*(?P<gender>woman| man|female| male|boy|girl) .*')
