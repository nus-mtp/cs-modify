'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER, SESSION
import web
from components import model


class Modules(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    def __init__(self):
        self.form = self.create_form()


    def GET(self):
        '''
            This function is called when the '/' page (index.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        else:
            module_infos = model.get_all_modules()
            form = self.form()
            if SESSION['displayErrorMessage'] is True:
                SESSION['displayErrorMessage'] = False
            else:
                SESSION['keyError'] = False

            return RENDER.moduleListing(module_infos, form, SESSION['keyError'])


    def POST(self):
        '''
            This function is called when the 'Add Module' form is submitted
            if form input is invalid, reload the page and shows error message besides field
        '''
        form = self.form()
        if not form.validates():
            modules = model.get_all_modules()
            return RENDER.moduleListing(modules, form, SESSION['keyError'])

        # else add module to db and refresh page
        outcome = model.add_module(form.d.code, form.d.name, form.d.description, form.d.mc, 'New')
        if outcome is False:
            SESSION['keyError'] = True
            SESSION['displayErrorMessage'] = True
        raise web.seeother('/moduleListing')        # load index.html again


    def create_form(self):
        ''' Creates the 'Add Module' form that will appear on the webpage '''
        code_validation_alphanumeric = web.form.regexp(
            r"^\w+$", 'Module code should be alphanumeric.')

        name_validation_alphanumeric = web.form.regexp(
            r"^[\w\s]+$", 'Module name should be alphanumeric.')

        validation_numeric_only = web.form.regexp(
            r"^\d+$", 'Number of MCs should be a number.')

        module_code_textbox = web.form.Textbox('code',
                                               web.form.notnull,
                                               code_validation_alphanumeric,
                                               post="<br><br>",
                                               description="Code")

        module_name_textbox = web.form.Textbox('name',
                                               web.form.notnull,
                                               name_validation_alphanumeric,
                                               post="<br><br>",
                                               description="Name")

        module_description_textarea = web.form.Textarea('description',
                                                        web.form.notnull,
                                                        rows="5",
                                                        cols="55",
                                                        post="<br><br>",
                                                        description="Description")

        module_mcs = web.form.Textbox('mc',
                                      web.form.notnull,
                                      validation_numeric_only,
                                      post="<br><br>",
                                      description="MCs")

        module_form_submit_button = web.form.Button('Add Module',
                                                    class_="btn btn-primary")

        form = web.form.Form(module_code_textbox,
                             module_name_textbox,
                             module_description_textarea,
                             module_mcs,
                             module_form_submit_button)
        return form



class FlagAsRemoved(object):
    '''
        This class handles the flagging of a module as 'To Be Removed'
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/moduleListing')


    def POST(self, module_code):
        ''' Flag module as removed '''
        model.flag_module_as_removed(module_code)
        raise web.seeother('/moduleListing')



class DeleteMod(object):
    '''
        This class handles the deletion of module
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/moduleListing')


    def POST(self, module_code):        # module_code is obtained from the end of the URL
        ''' Delete the module '''
        model.delete_module(module_code)
        raise web.seeother('/moduleListing')
