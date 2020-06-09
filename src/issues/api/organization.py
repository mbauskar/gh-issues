from issues.models import Organization, Repo
from issues.utils.request import github_request
from issues.api.repo import fetch_and_save_organization_repos

def fetch_user_organizations():
	""" fetch organization from github and save it in db """

	orgs = []
	orgs_info = github_request('user/orgs')
	if not orgs_info:
		return None

	orgs = list(Organization.objects.all())
	already_exists_orgs = [org.name for org in orgs]
	for org_info in orgs_info:
		org_name = org_info.get('login', None)
		if org_name not in already_exists_orgs:
			orgs.append(Organization.objects.create(name=org_info.get('login', '')))

		fetch_and_save_organization_repos(org_name)

	return orgs
