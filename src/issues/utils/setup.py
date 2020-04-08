from issues.api.user import fetch_user
from issues.api.organization import fetch_user_organizations

def setup_user():
	""" setup user and organization """
	user = fetch_user()
	orgs = fetch_user_organizations()