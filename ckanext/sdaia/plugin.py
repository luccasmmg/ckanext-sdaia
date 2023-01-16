import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from flask import Blueprint, render_template

def group_create(context, data_dict=None):
    return {'success': False, 'msg': 'No one is allowed to create groups'}

@toolkit.chained_action
@toolkit.side_effect_free
def package_search(original_action, context, data_dict):
    result = original_action(context, data_dict)
    result['Modified'] = True
    return result

def hello_world():
    '''A simple view function'''
    return config.get('ckanext.sdaia.hello_message') + ", this is my first ckan extension"

class SdaiaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
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

    #IAuthActionS
    def get_auth_functions(self):
        return {
            'group_create': group_create,
        }

    def update_package_schema(self):
        schema = super(SdaiaPlugin, self).update_package_schema()
        schema.update({
            'custom_text_sdaia': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def show_package_schema(self):
        schema = super(SdaiaPlugin, self).show_package_schema()
        schema.update({
            'custom_text_sdaia': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def configure(self, config):
        # Certain config options must exists for the plugin to work. Raise an
        # exception if they're missing.
        missing_config = "{0} is not configured. Please amend your .ini file."
        config_options = (
            'ckanext.sdaia.hello_message',
        )
        for option in config_options:
            if not config.get(option, None):
                raise RuntimeError(missing_config.format(option))

