import os
import sys
from performance import html
from logging_wrapper import init_logging_file
import settings.update as SU

l = len("performance_report.py")
TEST_ENV_DIR = sys.argv[0][0:-l]
TEST_DATE_PATH = ""
TEST_REPORT_PATH = ""
print sys.argv
if len(sys.argv) >= 3:
    TEST_DATE_PATH = sys.argv[1]#get test_main.py file location
    TEST_REPORT_PATH = sys.argv[2]#get the report result
else:
    print >> sys.stderr, "You should give me a path of the KPI data and the path of the report"
    exit(1)
os.chdir(TEST_ENV_DIR)
SU.update()

init_logging_file(test_env_xxx=TEST_ENV_DIR)

print html(TEST_DATE_PATH,TEST_REPORT_PATH)
exit(0)