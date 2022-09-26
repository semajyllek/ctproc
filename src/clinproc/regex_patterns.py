import re

CT_FILE_PATTERN = re.compile("\S+(NCT.*\.xml)")

EMPTY_PATTERN = re.compile('[\n\s]+')
INC_ONLY_PATTERN = re.compile('[\s\n]+[Ii]nclusion [Cc]riteria:?([\w\W ]*)')
EXC_ONLY_PATTERN = re.compile('[\n\r ]+[Ee]xclusion [Cc]riteria:?([\w\W ]*)')
AGE_PATTERN = re.compile('(?P<age>\d+) *(?P<units>\w+).*')
YEAR_PATTERN = re.compile('(?P<year>[yY]ears?.*)')
MONTH_PATTERN = re.compile('(?P<month>[mM]o(?:nth)?)')
WEEK_PATTERN = re.compile('(?P<week>[wW]eeks?)')

BOTH_INC_AND_EXC_PATTERN = re.compile("[\s\n]*[Ii]nclusion [Cc]riteria:?(?: +[Ee]ligibility[ \w]+\: )?(?P<include_crit>[ \n(?:\-|\d)\.\?\"\%\r\w\:\,\(\)]*)[Ee]xclusion [Cc]riteria:?(?P<exclude_crit>[\w\W ]*)")
