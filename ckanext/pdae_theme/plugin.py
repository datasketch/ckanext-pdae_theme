from datetime import datetime

import ckan.logic as logic
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from babel.dates import format_date
from ckan.common import config
from ckan.lib import base
from ckan.lib.helpers import lang


def get_datasets(sort_key="metadata_modified desc"):
    if (sort_key == "popular"):
        sort_key = "score desc"
    datasets = toolkit.get_action("package_search")(
        data_dict={"rows": 10, "sort": sort_key})
    return datasets["results"]


def get_announce():
    announce = config.get("ckan.pdae_theme.announce", "")
    return announce


def get_featured_banner():
    featured_banner = {
        "title": config.get("ckan.pdae_theme.featured_banner_title", ""),
        "text": config.get("ckan.pdae_theme.featured_banner_text", ""),
        "button": config.get("ckan.pdae_theme.featured_banner_button", ""),
        "href": config.get("ckan.pdae_theme.featured_banner_href", "")
    }
    return featured_banner


def get_update_frequency():
    return {"update_frequency": update_frequency}


def show_featured_banner():
    featured_banner = get_featured_banner()
    title = featured_banner["title"]
    text = featured_banner["text"]
    return bool(title or text)


def pdae_theme_render_datetime(date_str, date_format="d 'de' MMMM 'de' y", locale=""):
    if not date_str:
        return ""
    if not locale:
        locale = lang()
    datetime_ = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return format_date(datetime_, format=date_format, locale=locale)


def create_update_frequency():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    try:
        data = {"id": "update_frequency"}
        toolkit.get_action("vocabulary_show")(context, data)
    except toolkit.ObjectNotFound:
        data = {"name": "update_frequency"}
        vocab = toolkit.get_action("vocabulary_create")(context, data)
        for tag in (u"Tiempo real", u"Diaria", u"Semanal", u"Mensual", u"Bimestral", u"Trimestral", u"Semestral", u"Anual"):
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)


def update_frequency():
    create_update_frequency()
    try:
        tag_list = toolkit.get_action("tag_list")
        update_frequency = tag_list(
            data_dict={"vocabulary_id": "update_frequency"})
        return update_frequency
    except toolkit.ObjectNotFound:
        return None


def get_menu_labels():
    menu = {
        'dataset': config.get("ckan.pdae_theme.dataset_link_label", "Catálogo de Datos Abiertos"),
        'blog': config.get("ckan.pdae_theme.blog_link_label", "Blog / Noticias"),
        'regulations': config.get("ckan.pdae_theme.regulations_link_label", "Normativa"),
        'learn': config.get("ckan.pdae_theme.learn_link_label", "Centro de aprendizaje"),
        'faq': config.get("ckan.pdae_theme.learn_faq_link_label", "Preguntas frecuentes"),
        'manuals': config.get("ckan.pdae_theme.learn_manuals_link_label", "Manuales de usuario"),
        'courses': config.get("ckan.pdae_theme.learn_courses_link_label", "Cursos de capacitación"),
        'participation': config.get("ckan.pdae_theme.participation_link_label", "Participación ciudadana")
    }
    return menu


def get_support_email():
    email = config.get("ckan.pdae_theme.support_email",
                       "datosabiertos@planificacion.gob.ec")
    return email


def get_social_media():
    return {
        "twitter": config.get("ckan.pdae_theme.twitter"),
        "facebook": config.get("ckan.pdae_theme.facebook")
    }


def get_groups_with_packages():
    context = {'ignore_auth': True}
    groups = logic.get_action('group_list')(context, {"all_fields": True})
    groups = filter(lambda g: g["package_count"] > 0, groups)
    return list(groups)


class PdaeThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IMiddleware)

    def make_middleware(self, app, config):
        def error_handler(e):
            extra_vars = {
                u'code': e.code,
                u'content': e.description,
                u'name': e.name
            }
            return base.render(u'error_document_template.html', extra_vars), 500

        app.register_error_handler(500, error_handler)
        return app

    def make_error_log_middleware(self, app, config):
        return app

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets",
                             "ckanext-pdae_theme")

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator("ignore_missing")
        unicode_safe = toolkit.get_validator("unicode_safe")
        schema.update({
            "ckan.pdae_theme.announce": [ignore_missing, unicode_safe],
            "ckan.pdae_theme.featured_banner_title": [ignore_missing, unicode_safe],
            "ckan.pdae_theme.featured_banner_text": [ignore_missing, unicode_safe],
            "ckan.pdae_theme.featured_banner_button": [ignore_missing, unicode_safe],
            "ckan.pdae_theme.featured_banner_href": [ignore_missing, unicode_safe],
            "ckan.pdae_theme.dataset_link_label": [unicode_safe],
            "ckan.pdae_theme.blog_link_label": [unicode_safe],
            "ckan.pdae_theme.regulations_link_label": [unicode_safe],
            "ckan.pdae_theme.learn_link_label": [unicode_safe],
            "ckan.pdae_theme.learn_faq_link_label": [unicode_safe],
            "ckan.pdae_theme.learn_manuals_link_label": [unicode_safe],
            "ckan.pdae_theme.learn_courses_link_label": [unicode_safe],
            "ckan.pdae_theme.participation_link_label": [unicode_safe],
            "ckan.pdae_theme.support_email": [unicode_safe],
            "ckan.pdae_theme.facebook": [unicode_safe],
            "ckan.pdae_theme.twitter": [unicode_safe]
        })
        return schema

    def get_helpers(self):
        return {
            "pdae_theme_get_datasets": get_datasets,
            "get_announce": get_announce,
            "get_featured_banner": get_featured_banner,
            "show_featured_banner": show_featured_banner,
            "pdae_theme_render_datetime": pdae_theme_render_datetime,
            "update_frequency": update_frequency,
            "get_menu_labels": get_menu_labels,
            "get_support_email": get_support_email,
            "get_social_media": get_social_media,
            "get_groups_with_packages": get_groups_with_packages
        }

    def _modify_package_schema(self, schema):
        schema.update({
            "dataset_lang": [toolkit.get_validator("ignore_missing"),
                             toolkit.get_converter("convert_to_extras")]
        })
        schema.update({
            "update_frequency": [
                toolkit.get_validator("ignore_missing"),
                toolkit.get_converter("convert_to_tags")("update_frequency")
            ]
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

        schema.update({
            "dataset_lang": [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })

        schema["tags"]["__extras"].append(
            toolkit.get_converter("free_tags_only"))
        schema.update({
            "update_frequency": [
                toolkit.get_converter("convert_from_tags")(
                    "update_frequency"),
                toolkit.get_validator("ignore_missing")
            ]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []
