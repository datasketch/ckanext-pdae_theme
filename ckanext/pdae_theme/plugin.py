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


def get_featured_banner():
    featured_banner = {
        'title': config.get('ckan.pdae_theme.featured_banner_title', ''),
        'text': config.get('ckan.pdae_theme.featured_banner_text', ''),
        'button': config.get('ckan.pdae_theme.featured_banner_button', ''),
        'href': config.get('ckan.pdae_theme.featured_banner_href', '')
    }
    return featured_banner


def show_featured_banner():
    featured_banner = get_featured_banner()
    title = featured_banner['title']
    text = featured_banner['text']
    return bool(title or text)


def learn():
    return render_template('home/learn.html')


class PdaeThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
                             'ckanext-pdae_theme')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')
        schema.update({
            'ckan.pdae_theme.announce': [ignore_missing, unicode_safe],
            'ckan.pdae_theme.featured_banner_title': [ignore_missing, unicode_safe],
            'ckan.pdae_theme.featured_banner_text': [ignore_missing, unicode_safe],
            'ckan.pdae_theme.featured_banner_button': [ignore_missing, unicode_safe],
            'ckan.pdae_theme.featured_banner_href': [ignore_missing, unicode_safe]
        })
        return schema

    def get_helpers(self):
        return {
            'pdae_theme_get_datasets': get_datasets,
            'get_announce': get_announce,
            'get_featured_banner': get_featured_banner,
            'show_featured_banner': show_featured_banner
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

    def _modify_package_schema(self, schema):
        schema.update({
            'custom_text': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def create_package_schema(self):
        schema = super(PdaeThemePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(PdaeThemePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(PdaeThemePlugin, self).show_package_schema()

        ignore_missing = toolkit.get_validator('ignore_missing')
        convert_from_extras = toolkit.get_converter('convert_from_extras')

        schema.update({
            'custom_text': [convert_from_extras, ignore_missing]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []
