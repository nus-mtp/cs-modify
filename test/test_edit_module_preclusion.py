'''
    this class tests the page for editing module preclusions.
'''

from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session

class TestCode(object):
    '''
        In this test suite, we test whether buttons are present, and if
        any links or buttons (that are not invoking any JavaScript functions) are working.

        Some features/functions here cannot be tested using the nose framework (such as
        the add-unit and save-changes buttons, since they invoke JavaScript functions and
        are not actions of firing requests at the app).
    '''
    URL_EDIT_MODULE_PRECLUSION_SPECIFIC_VALID = '/editModulePreclusions?code=BT5110'
    URL_EDIT_MODULE_PRECLUSION_SPECIFIC_INVALID_CODE = '/editModulePreclusions?code=CS0123'

    EDIT_MODULE_TITLE = '<h1 class="text-center"><b>Edit Preclusions for ' +\
                        '<u id="module-code">BT5110</u></b></h1>'
    EDIT_MODULE_PRECLUSIONS_FORM = '<form id="preclusions-form" action="#" method="post">'
    EDIT_MODULE_PRECLUSIONS_TABLE_INTERFACE = '<table class="table table-hover text-center'
    EDIT_MODULE_PRECLUSIONS_ADD_UNIT_BUTTON = '<button class="btn btn-lg btn-primary" ' +\
                                              'data-toggle="tooltip" data-placement="top" ' +\
                                              'title="Add Module to Preclusions" ' +\
                                              'onclick="addPreclusionModule()">' +\
                                              '<span class="glyphicon glyphicon-plus">' +\
                                              '</span></button>'
    EDIT_MODULE_PRECLUSIONS_SAVE_BUTTON = '<button class="btn btn-lg btn-primary" ' +\
                                          'data-toggle="tooltip" data-placement="top" ' +\
                                          'title="Save Changes" ' +\
                                          'onclick="saveChangesPreclusion()">' +\
                                          '<span class="glyphicon glyphicon-floppy-disk">' +\
                                          '</span></button>'
    EDIT_MODULE_PRECLUSIONS_REVERT_BUTTON = '<button class="btn btn-lg btn-primary" ' +\
                                            'data-toggle="tooltip" data-placement="top" ' +\
                                            'title="Revert All Changes" ' +\
                                            'onclick="revertChangesPreclusion()">' +\
                                            '<span class="glyphicon glyphicon-refresh">' +\
                                            '</span></button>'
    EDIT_MODULE_PRECLUSIONS_BACK_BUTTON = '<a class="btn btn-lg btn-primary" ' +\
                                          'id="preclusion-back-button" ' +\
                                          'href="/editModule?code=BT5110" ' +\
                                          'data-toggle="tooltip" data-placement="top" ' +\
                                          'title="Go Back to Editing BT5110">' +\
                                          '<span class="glyphicon glyphicon-arrow-left">' +\
                                          '</span></a>'

    EDIT_MODULE_CORRECT_REDIRECT = 'Edit <b>General Information</b> For <b>BT5110</b>'


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


    def test_module_preclusion_edit_direct_access_correct_response(self):
        '''
            Tests whether user can access a page for showing
            edit-module-preclusion page directly through a valid URL.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_PRECLUSION_SPECIFIC_VALID)
        assert_equal(root.status, 200)

        root.mustcontain(self.EDIT_MODULE_TITLE)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_FORM)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_TABLE_INTERFACE)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_ADD_UNIT_BUTTON)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_SAVE_BUTTON)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_REVERT_BUTTON)
        root.mustcontain(self.EDIT_MODULE_PRECLUSIONS_BACK_BUTTON)


    def test_module_preclusion_edit_back_button(self):
        '''
            Tests if the back button for edit-module-preclusion page works.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_PRECLUSION_SPECIFIC_VALID)
        response = root.click(linkid="preclusion-back-button")

        assert_equal(response.status, 200)
        response.mustcontain(self.EDIT_MODULE_CORRECT_REDIRECT)


    @raises(Exception)
    def test_module_preclusion_edit_direct_access_invalid_code_url(self):
        '''
            Tests whether user will fail to access edit-module-preclusion
            page if an invalid URL (invalid module code) is used.
        '''
        self.test_app.get(self.URL_EDIT_MODULE_PRECLUSION_SPECIFIC_INVALID_CODE)
