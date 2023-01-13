import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template

@toolkit.chained_action
@toolkit.side_effect_free
def package_search(original_action, context, data_dict):
    result = original_action(context, data_dict)
    result['Modified'] = True
    return result

def hello_world():
    '''A simple view function'''
    return "Hello World, this is my first ckan extension"

class SdaiaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'sdaia')

    
    #IBlueprint
    def get_blueprint(self):
        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        # Add plugin url rules to Blueprint object
        blueprint.add_url_rule(
            u'/hello_world', 
            u'/hello_world', 
            hello_world,
            methods=['GET']
        )
        return blueprint

    #IActions
    def get_actions(self):
        return {
            'package_search': package_search,
        }
