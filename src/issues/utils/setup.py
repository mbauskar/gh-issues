from issues.api.user import get_user
from issues.api.organization import get_organizations

def setup_user():
	""" setup user and organization """
	user = get_user()
	orgs = get_organizations()
	print(user, orgs)