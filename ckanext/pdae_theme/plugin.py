import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template
from ckan.common import config


def get_datasets(sort_key='metadata_modified desc'):
    if (sort_key == 'popular'):
        sort_key = 'score desc'
    datasets = toolkit.get_action('package_search')(
        data_dict={'rows': 10, 'sort': sort_key})
    return datasets['results']


def get_announce():
    announce = config.get('ckan.pdae_theme.announce', '')
    return announce


def learn():
    return render_template('home/learn.html')


class PdaeThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
                             'ckanext-pdae_theme')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')
        schema.update({
            'ckan.pdae_theme.announce': [ignore_missing, unicode_safe]
        })
        return schema

    def get_helpers(self):
        return {
            'pdae_theme_get_datasets': get_datasets,
            'get_announce': get_announce
        }

    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        rules = [
            ('/centro-de-aprendizaje', 'learn', learn)
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)
        return blueprint
