'''
    test_view_module.py tests the page views and navigations for
    viewing a target module's overview.

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.
    #3 Navigating to other valid pages from the target page should be successful.

    For #3, we do not check the full correctness of the UI for the other pages, as this
    will be handled by its corresponding test cases.
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''


    URL_VIEW_MODULE_VALID = '/viewModule?code=BT5110'
    URL_VIEW_MODULE_INVALID = '/viewModule?code=CS0123'

    FORM_EDIT_MODULE_INFO = '<form id="edit-module-button" name="edit-module-button" ' +\
                            'action="/editModule" method="post">'
    FORM_EDIT_MODULE_INFO_BUTTON = '<input class="btn btn-lg btn-primary" type="submit"' +\
                                   ' value="Edit General Module Info" ' +\
                                   'data-toggle="tooltip" data-placement="right" ' +\
                                   'title="Edit the module\'s name, description ' +\
                                   'and MCs">'

    CONTENT_SUMMARY = "Module Info Overview"
    CONTENT_CODE = "BT5110"
    CONTENT_NAME = "Data Management and Warehousing"
    CONTENT_MC = "(4 MCs)"
    CONTENT_DESCRIPTION = "Module Description:"
    CONTENT_PRECLUSION = "Module Preclusions:"
    CONTENT_PREREQUISITE = "Module Prerequisites"
    CONTENT_QUOTA = "Class Quota for AY-Semesters"
    CONTENT_TABLE_MOUNT_FLAG = "<th>Mounted</th>"
    CONTENT_TABLE_QUOTA = "<th>Quota</th>"
    CONTENT_TABLE_STUDENT_DEMAND = "<th>Students Planning to Take</th>"

    FORM_OVERLAPPING_MODULE = '<form id="view-overlapping-with-module" '+\
                              'name="view-overlapping-with-module" '+\
                              'action="/overlappingWithModule" '+\
                              'method="get">'
    FORM_OVERLAPPING_MODULE_BUTTON = '<input type="submit" class="btn btn-lg btn-primary" '+\
                                     'value="View Modules That Overlap With This Module.">'


    def __init__(self):
        self.middleware = None
        self.test_app = None


    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))
        session.set_up(self.test_app)


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        session.tear_down(self.test_app)


    def test_view_valid_module_overview_valid_response(self):
        '''
            Tests whether user can access page for showing module overview
            if target module is valid.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_view_invalid_module_overview_valid_response(self):
        '''
            Tests if user will fail to access page for showing module overview
            if target module is invalid.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_INVALID)
        assert_equal(root.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        root.mustcontain("Not Found")


    def test_view_module_overview_goto_valid_individual_module(self):
        '''
            Tests if navigation to a valid individual module view
            is succesful.

            (i.e. navigation to module info for valid target module and
            valid target AY-semester and quota)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        response = root.goto(url, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)


    def test_view_module_overview_goto_individual_module_invalid_code(self):
        '''
            Tests if navigation to an individual module view
            with invalid module code is unsuccesful.

            (i.e. navigation to module info for invalid target module and
            valid target AY-semester and quota)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_INVALID + '&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        response = root.goto(url, method='get')

        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        response.mustcontain("Not Found")


    # '''
    #     Tests if navigation to an individual module view
    #     with invalid AY-semester is unsuccesful.

    #     (i.e. navigation to module info for valid target module and
    #     quota, but invalid AY-semester)

    #     NOTE: Checking for invalid AY-semester is not implemented yet.
    # '''
    # '''
    # @raises(Exception)
    # def test_view_module_overview_goto_individual_module_invalid_ay_sem(self):
    #     root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
    #     url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F18+Sem+1' +\
    #           '&quota=60'
    #     response = root.goto(url, method='get')
    # '''


    # '''
    #     Tests if navigation to an individual module view
    #     with invalid quota is unsuccesful.

    #     (i.e. navigation to module info for invalid quota and
    #     valid target module and AY-semester)

    #     NOTE: Checking for invalid quota is not implemented yet.
    # '''
    # '''
    # @raises(Exception)
    # def test_view_module_overview_goto_individual_module_invalid_quota(self):
    #     root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
    #     url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F17+Sem+1' +\
    #           '&quota=70'
    #     response = root.goto(url, method='get')
    # '''


    def test_view_module_overview_contents(self):
        '''
            Tests if all the necessary info is displayed in the module
            overview page.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)

        root.mustcontain(self.CONTENT_SUMMARY)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_PRECLUSION)
        root.mustcontain(self.CONTENT_PREREQUISITE)
        root.mustcontain(self.CONTENT_QUOTA)
        root.mustcontain(self.CONTENT_TABLE_MOUNT_FLAG)
        root.mustcontain(self.CONTENT_TABLE_QUOTA)
        root.mustcontain(self.CONTENT_TABLE_STUDENT_DEMAND)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO_BUTTON)
        root.mustcontain(self.FORM_OVERLAPPING_MODULE)
        root.mustcontain(self.FORM_OVERLAPPING_MODULE_BUTTON)


    def test_goto_edit_general_info(self):
        '''
            Tests if user can access the 'Edit General Module Info' option
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        edit_form = root.forms__get()["edit-module-button"]

        response = edit_form.submit()
        assert_equal(response.status, 200)

    def test_goto_overlapping_with_module(self):
        '''
            test if user can access to moverlapping with module page
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        edit_form = root.forms__get()["view-overlapping-with-module"]

        response = edit_form.submit()
        assert_equal(response.status, 200)
