from django.apps import AppConfig

from issues.utils.setup import setup_user


class IssuesConfig(AppConfig):
    name = 'issues'
