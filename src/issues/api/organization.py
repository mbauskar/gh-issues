from issues.models import Organization, Repo
from issues.utils.request import github_request

def get_organizations():
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

		get_and_save_organization_repos(org_name)

	return orgs


def get_and_save_organization_repos(org_name):
	""" fetch all the repos of the org_name """
	def format_repo(repo):
		keys_to_keep = ['name', 'full_name', 'private']
		args = { key: repo.get(key, '') for key in keys_to_keep }
		args.update({ 'organization_id': org_name })
		return args

	repos = github_request(f'orgs/{org_name}/repos')
	repos = list(map(format_repo, repos))

	already_exists_repos = Repo.objects.filter(organization_id=org_name)
	exists_repo_names = list(already_exists_repos.values_list('name', flat=True))
	repo_names = [repo.get('name', '') for repo in repos if repo.get('name', '')]

	to_insert = list(set(repo_names) - set(exists_repo_names))
	for repo in repos:
		repo_name = repo.get('name', None)
		if repo_name in to_insert:
			Repo.objects.create(**repo)