# import routes.mapper

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template


def learn():
    return render_template('home/learn.html')


class PdaeThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
                             'pdae_theme')

    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        rules = [
            ('/centro-de-aprendizaje', 'learn', learn)
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)
        return blueprint
