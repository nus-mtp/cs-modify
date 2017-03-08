'''
    This module contains the handler for displaying the outcome of a form submission
    (E.g. adding/editing/restoring a module)
'''

from app import RENDER, SESSION
import web
from components import model


class Outcome(object):
    '''
        This class handles the display of a form submission's outcome
    '''
    def POST(self, *received_data):
        if received_data is not None:
            data = received_data
            action = data[0]
            outcome = data[1]
            module_code = data[2]

            outcome_message = None
            redirect_page = None

            if action == "add_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been added successfully!"
                    redirect_page = "/viewModule?code="+module_code
                else:
                    outcome_message = "Error: Module code already exists! Please use another module code."
                    redirect_page = "/modules"

            elif action == "edit_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been edited successfully!"
                else:
                    outcome_message = "Error: Failed to edit module."
                redirect_page = "/viewModule?code="+module_code

            elif action == "edit_mounting":
                ay_sem = data[3]
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been edited successfully!"
                else:
                    outcome_message = "Error: Failed to edit module."
                redirect_page = "individualModuleInfo?code="+module_code+"&targetAY="+\
                                ay_sem.replace(' ', '+').replace('/', '%2F')

            elif action == "restore_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been restored successfully!"
                    redirect_page = "/viewModule?code="+module_code
                else:
                    outcome_message = "Error: Failed to restore module."
                    redirect_page = "/modifiedModules"

            elif action == "delete_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been deleted successfully!"
                else:
                    outcome_message = "Error: Module " + module_code + " currently has " +\
                                      "mountings that refer to it. " +\
                                      "Remove all mountings before deleting module!"
                redirect_page = "/modules"

            return RENDER.outcome(outcome_message, redirect_page)