from django.test import TestCase

# Create your tests here.


from oracle_config import Ora

db = Ora()
test_case = db.check_dr_pead("51003720")
print(test_case)
