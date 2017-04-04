'''
    This module contains the handler for web requests pertaining to
    the editing of a module's preclusions.
'''


import json
from app import RENDER
import web
from components import model, session


class EditModulePreclusions(object):
    '''
        This class handles the editing of a module's preclusions.
    '''
    def GET(self):
        '''
            Handles the loading of the 'Edit Module Preclusions' page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            input_data = model.validate_input(web.input(), ["code"])
            module_code = input_data.code

            preclusions = model.get_preclusion_units(module_code)
            return RENDER.moduleEditPreclusion(module_code, preclusions)


    def POST(self):
        '''
            Handles the submission of updated module preclusions
            for a target module.
        '''
        response = False

        input_data = model.validate_input(web.input(), ["code"], show_404=False)

        if input_data:
            module_code = input_data.code
            preclusions = json.loads(input_data.preclusions)
            response = model.edit_preclusion(module_code, preclusions)

        return json.dumps(response)