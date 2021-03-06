'''
    test_database.py
    Contains test cases for database related functions.
'''
from nose.tools import assert_equal, assert_false, assert_true
from components import model


# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
    This class runs the test cases for database related functions.
    '''
    def __init__(self):
        self.test_module_code = "AA1111"
        self.test_module_name = "Dummy Module"
        self.test_module_desc = "Dummy Description"
        self.test_module_mc = 1
        self.test_module_status = "Active"
        self.test_module_mounted_count = 2
        self.test_module_fixed_mounting_s1 = "AY 16/17 Sem 1"
        self.test_module_fixed_mounting_s2 = "AY 16/17 Sem 2"
        self.test_module_tenta_mounting_s1 = "AY 17/18 Sem 1"
        self.test_module_tenta_mounting_s2 = "AY 17/18 Sem 2"
        self.test_module_quota1 = 10
        self.test_module_quota2 = 20
        self.module_CRD_tested = False
        self.fixed_mounting_CRD_tested = False
        self.tenta_mounting_CRD_tested = False
        self.prereq_CRD_tested = False
        self.prereq_delete_all_tested = False
        self.test_prereq_code = "BB1111"
        self.test_prereq_index = 0
        self.test_prereq2_code = "BB1112"
        self.test_prereq2_index = 1
        self.preclude_CRD_tested = False
        self.preclude_delete_all_tested = False
        self.test_preclude_code = "CC1111"
        self.test_preclude_code2 = "CC1112"
        self.starred_CRD_tested = False
        self.test_user = "testUser"
        self.test_salt = "salt"
        self.test_password = "pass"


    def setUp(self):
        '''
            Add dummy modules and mountings into database
        '''
        self.test_module_CRD()
        self.module_CRD_tested = True
        model.add_module(self.test_module_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)

        self.test_fixed_mounting_CRD()
        self.fixed_mounting_CRD_tested = True

        self.test_tenta_mounting_CRD()
        self.tenta_mounting_CRD_tested = True
        model.add_tenta_mounting(self.test_module_code,
                                 self.test_module_tenta_mounting_s1,
                                 self.test_module_quota1)

        self.test_prereq_CRD()
        self.prereq_CRD_tested = True
        self.test_prereq_delete_all()
        self.prereq_delete_all_tested = True
        self.test_preclude_CRD()
        self.preclude_CRD_tested = True
        self.test_preclude_delete_all()
        self.preclude_delete_all_tested = True
        self.test_starred_CRD()
        self.starred_CRD_tested = True


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_prerequisite(self.test_module_code, self.test_prereq_code)
        model.delete_tenta_mounting(self.test_module_code, self.test_module_tenta_mounting_s1)
        model.delete_module(self.test_module_code)


    def test_module_CRD(self):
        '''
            Tests creating, reading and deleting of modules.
        '''
        if not self.module_CRD_tested:
            model.add_module(self.test_module_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)

            module_info = model.get_module(self.test_module_code)
            assert_true(module_info is not None)

            assert_equal(self.test_module_code, module_info[0])
            assert_equal(self.test_module_name, module_info[1])
            assert_equal(self.test_module_desc, module_info[2])
            assert_equal(self.test_module_mc, module_info[3])
            assert_equal(self.test_module_status, module_info[4].rstrip())

            model.delete_module(self.test_module_code)
            module_info = model.get_module(self.test_module_code)
            assert_true(module_info is None)
            return


    def test_fixed_mounting_CRD(self):
        '''
            Tests creating, reading and deleting of fixed mountings.
        '''
        if not self.fixed_mounting_CRD_tested:
            model.add_fixed_mounting(self.test_module_code,
                                     self.test_module_fixed_mounting_s1,
                                     self.test_module_quota1)
            model.add_fixed_mounting(self.test_module_code,
                                     self.test_module_fixed_mounting_s2,
                                     self.test_module_quota2)

            mounting_data = model.get_fixed_mounting_and_quota(self.test_module_code)
            assert_equal(self.test_module_mounted_count, len(mounting_data))

            mounting_s1 = mounting_data[0][0]
            mounting_s2 = mounting_data[1][0]
            quota_s1 = mounting_data[0][1]
            quota_s2 = mounting_data[1][1]

            assert_equal(self.test_module_fixed_mounting_s1, mounting_s1)
            assert_equal(self.test_module_fixed_mounting_s2, mounting_s2)
            assert_equal(self.test_module_quota1, quota_s1)
            assert_equal(self.test_module_quota2, quota_s2)

            model.delete_fixed_mounting(self.test_module_code,
                                        self.test_module_fixed_mounting_s1)
            model.delete_fixed_mounting(self.test_module_code,
                                        self.test_module_fixed_mounting_s2)

            mounting_data = model.get_fixed_mounting_and_quota(self.test_module_code)
            assert_true(len(mounting_data) == 0)
            return


    def test_tenta_mounting_CRD(self):
        '''
            Tests creating, reading and deleting of tentative mountings.
        '''
        if not self.tenta_mounting_CRD_tested:
            model.add_tenta_mounting(self.test_module_code,
                                     self.test_module_tenta_mounting_s1,
                                     self.test_module_quota1)
            model.add_tenta_mounting(self.test_module_code,
                                     self.test_module_tenta_mounting_s2,
                                     self.test_module_quota2)

            mounting_data = model.get_tenta_mounting_and_quota(self.test_module_code)
            assert_equal(self.test_module_mounted_count, len(mounting_data))

            mounting_s1 = mounting_data[0][0]
            mounting_s2 = mounting_data[1][0]
            quota_s1 = mounting_data[0][1]
            quota_s2 = mounting_data[1][1]

            assert_equal(self.test_module_tenta_mounting_s1, mounting_s1)
            assert_equal(self.test_module_tenta_mounting_s2, mounting_s2)
            assert_equal(self.test_module_quota1, quota_s1)
            assert_equal(self.test_module_quota2, quota_s2)

            model.delete_tenta_mounting(self.test_module_code,
                                        self.test_module_tenta_mounting_s1)
            model.delete_tenta_mounting(self.test_module_code,
                                        self.test_module_tenta_mounting_s2)

            mounting_data = model.get_tenta_mounting_and_quota(self.test_module_code)
            assert_true(len(mounting_data) == 0)
            return


    def test_delete_module_with_mounting(self):
        '''
            Tests deleting of modules with tentative mounting.
        '''
        outcome = model.delete_module(self.test_module_code)
        assert_false(outcome)
        module_info = model.get_module(self.test_module_code)
        assert_true(module_info is not None)
        return


    def test_add_mod_with_repeat_code(self):
        '''
            Tests that adding of module with duplicated code will fail.
        '''
        # Not duplicate code --> success
        outcome = model.add_module("AA2222", "Dummy Module", "Dummy Description", 1, "New")
        assert_true(outcome)

        # Duplicate code --> fail
        outcome = model.add_module(self.test_module_code, self.test_module_name,
                                   self.test_module_desc, self.test_module_mc, "New")
        assert_false(outcome)

        model.delete_module("AA2222")


    def test_add_mounting_with_repeat_code_and_ay_sem(self):
        '''
            Tests that a module cannot have more than one mounting in the same AY/Sem
        '''
        outcome = model.add_tenta_mounting(self.test_module_code,
                                           self.test_module_tenta_mounting_s1,
                                           123)
        assert_false(outcome)


    def test_update_module(self):
        '''
            Tests updating of module info
        '''
        # Update one field
        model.update_module(self.test_module_code, "Dummy module 2",
                            self.test_module_desc, self.test_module_mc)
        module_info = model.get_module(self.test_module_code)
        assert_equal(self.test_module_code, module_info[0])
        assert_equal("Dummy module 2", module_info[1])
        assert_equal(self.test_module_desc, module_info[2])
        assert_equal(self.test_module_mc, module_info[3])
        assert_equal(self.test_module_status, module_info[4].rstrip())

        # Update multiple fields
        model.update_module(self.test_module_code, "Dummy module 2",
                            "Dummy description 2", 2)
        module_info = model.get_module(self.test_module_code)
        assert_equal(self.test_module_code, module_info[0])
        assert_equal("Dummy module 2", module_info[1])
        assert_equal("Dummy description 2", module_info[2])
        assert_equal(2, module_info[3])
        assert_equal(self.test_module_status, module_info[4].rstrip())

        # Update fails because MC cannot be a string of alphabets
        outcome = model.update_module(self.test_module_code, "Dummy module 2",
                                      "Dummy description 2", "abc")
        assert_false(outcome)


    def test_update_quota(self):
        '''
            Tests updating of module's quota for a target tentative AY/Sem
        '''
        model.update_quota(self.test_module_code,
                           self.test_module_tenta_mounting_s1, 999)

        mounting_data = model.get_tenta_mounting_and_quota(self.test_module_code)
        assert_equal(1, len(mounting_data))

        mounting_s1 = mounting_data[0][0]
        quota_s1 = mounting_data[0][1]

        assert_equal(mounting_s1, self.test_module_tenta_mounting_s1)
        assert_equal(quota_s1, 999)


    def test_add_validate_and_delete_admin(self):
        '''
            Tests addition, validation, and deletion of admins.
        '''
        salted_pass = "7064b94a4296650fcf5af42f25a41f5e70000fb140baa56623c" +\
                        "df4da2a2bc25f0db5168f57b1ebd96b10c40737c1a73285907" +\
                        "265f619ac85b281cd2fc5f4207d"
        is_admin_valid = model.validate_admin("Admin 1", "pass")
        assert_false(is_admin_valid)

        model.add_admin("Admin 1", "salt", salted_pass)
        is_admin_valid = model.validate_admin("Admin 1", "pass")
        assert_true(is_admin_valid)

        model.delete_admin("Admin 1")
        is_admin_valid = model.validate_admin("Admin 1", "pass")
        assert_false(is_admin_valid)


    def test_is_existing_module(self):
        '''
            Tests if is_existing_module() function is working correctly.
        '''
        current_test_module_code = "ZZ7654"

        assert_false(model.is_existing_module(current_test_module_code))
        model.add_module(current_test_module_code, "Exist Module",
                         "I describe myself", 4, "New")
        assert_true(model.is_existing_module(current_test_module_code))
        model.delete_module(current_test_module_code)


    def test_prereq_CRD(self):
        '''
            Tests creating, reading and deleting of prerequisites.
        '''
        if not self.prereq_CRD_tested:
            model.add_module(self.test_prereq_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)

            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_prerequisite(self.test_module_code, self.test_prereq_code)
            model.delete_module(self.test_prereq_code)
            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_prereq_delete_all(self):
        '''
            Tests deleting all prerequisites of specific module.
        '''
        if not self.prereq_delete_all_tested:
            model.add_module(self.test_prereq_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)
            model.add_module(self.test_prereq2_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)

            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)
            model.add_prerequisite(self.test_module_code, self.test_prereq2_code,
                                   self.test_prereq2_index)

            outcome = model.delete_all_prerequisite(self.test_module_code)
            assert_true(outcome)

            model.delete_module(self.test_prereq_code)
            model.delete_module(self.test_prereq2_code)
            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_preclude_CRD(self):
        '''
            Tests creating, reading and deleting of preclusions.
        '''
        if not self.preclude_CRD_tested:
            model.add_module(self.test_preclude_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)

            outcome = model.add_preclusion(self.test_module_code, self.test_preclude_code)
            assert_true(outcome)

            # Module should not preclude itself check
            outcome = model.add_preclusion(self.test_preclude_code, self.test_preclude_code)
            assert_false(outcome)

            # Modules should mutually preclude each other
            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])

            preclude_info = model.get_preclusion(self.test_preclude_code)
            assert_true(preclude_info is not None)
            assert_equal(self.test_module_code, preclude_info[0][0])

            model.delete_preclusion(self.test_module_code, self.test_preclude_code)
            model.delete_module(self.test_preclude_code)

            # After deleting preclusion, it should not exist
            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return


    def test_preclude_delete_all(self):
        '''
            Tests deleting all preclusions of specific module.
        '''
        if not self.preclude_delete_all_tested:
            model.add_module(self.test_preclude_code, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)
            model.add_module(self.test_preclude_code2, self.test_module_name, self.test_module_desc,
                             self.test_module_mc, self.test_module_status)

            model.add_preclusion(self.test_module_code, self.test_preclude_code)
            model.add_preclusion(self.test_module_code, self.test_preclude_code2)

            outcome = model.delete_all_preclusions(self.test_module_code)
            assert_true(outcome)

            preclude_info_1 = model.get_preclusion(self.test_preclude_code)
            preclude_info_2 = model.get_preclusion(self.test_preclude_code2)
            preclude_info_3 = model.get_preclusion(self.test_module_code)

            model.delete_module(self.test_preclude_code)
            model.delete_module(self.test_preclude_code2)

            assert_true(len(preclude_info_1) == 0)
            assert_true(len(preclude_info_2) == 0)
            assert_true(len(preclude_info_3) == 0)
            return


    def test_starred_CRD(self):
        '''
            Tests starring, reading and unstarring of modules.
        '''
        if not self.starred_CRD_tested:
            model.add_admin(self.test_user, self.test_salt, self.test_password)
            model.star_module(self.test_module_code, self.test_user)
            assert_true(model.is_module_starred(self.test_module_code, self.test_user))

            starred_info = model.get_starred_modules(self.test_user)
            assert_true(starred_info is not None)
            assert_equal(self.test_module_code, starred_info[0][0])
            assert_equal(self.test_module_name, starred_info[0][1])

            model.unstar_module(self.test_module_code, self.test_user)
            starred_info = model.get_starred_modules(self.test_user)
            model.delete_admin(self.test_user)
            assert_true(len(starred_info) == 0)
            return
