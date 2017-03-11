'''
    test_add_module.py tests the add module page
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION
import web

class TestCode(object):
    '''
        runs tests to test accessability and components in add module page
    '''
    HEADER_TITLE = '<h2><span class="glyphicon glyphicon-plus"></span> Add a new module</h2>'
    FORM_LABEL_CODE = '<label for="module-code" class="col-2 col-form-table">Module Code:</label>'
    FORM_INPUT_CODE = '<input class="form-control" type="text" id="module-code" name="code" '+\
                      'pattern="[A-Z0-9]{0,12}$" placeholder="e.g. CS1010" required>'
    FORM_LABEL_NAME = '<label for="module-name">Module Name:</label>'
    FORM_INPUT_NAME = '<input class="form-control" type="text" id="module-name"'+\
                      ' name="name" pattern="[a-zA-Z0-9 \-]+$" '+\
                      'placeholder="e.g. Programming methodology" required>'
    FORM_LABEL_DESCRIPTION = '<label for="module-description">Module Description:</label>'
    FORM_TEXTAREA_DESCRIPTION = '<textarea class="form-control" type="text" rows="6" '+\
                                'id="module-description" name="description" '+\
                                'placeholder="Description" required></textarea>'
    FORM_LABEL_MC = '<label for="module-mc">Module Credits:</label>'
    FORM_INPUT_MC = '<input class="form-control" type="number" min="0" max="12" id="module-mc"'+\
                    ' name="mc" placeholder="e.g. 4" required>'
    FORM_INPUT_BUTTON = '<input class="btn btn-lg btn-primary" type="submit" value="Submit">'

    URL_NORMAL = '/addModule'

    def __init__(self):
        self.middleware = None
        self.test_app = None

    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))
        # Sets up the simulated 'login' state
        SESSION['id'] = web.ACCOUNT_LOGIN_SUCCESSFUL


    def test_add_module_valid_response(self):
        '''
            tests that add module page is accessable
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)

    def test_add_module_page_content(self):
        '''
            tests that add module page contains all required labels and inputs
        '''
        root = self.test_app.get(self.URL_NORMAL)
        root.mustcontain(self.HEADER_TITLE)

        #for code
        root.mustcontain(self.FORM_LABEL_CODE)
        root.mustcontain(self.FORM_INPUT_CODE)
        #for name
        root.mustcontain(self.FORM_LABEL_NAME)
        root.mustcontain(self.FORM_INPUT_NAME)
        #for description
        root.mustcontain(self.FORM_LABEL_DESCRIPTION)
        root.mustcontain(self.FORM_TEXTAREA_DESCRIPTION)
        #for mc
        root.mustcontain(self.FORM_LABEL_MC)
        root.mustcontain(self.FORM_INPUT_MC)
        #checks that submit button exit
        root.mustcontain(self.FORM_INPUT_BUTTON)
