from issues.models import Repo
from issues.utils.request import github_request

def fetch_and_save_organization_repos(org_name):
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


def get_repos(org_name, org_names=[], values_list=[], **kwargs):
	''' get repos from db '''
	filters = { 'organization_id__should_track': True }
	filters.update(kwargs)

	if org_name:
		org_names = [org_name]
	elif org_names:
		org_names = org_names if not isinstance(org_names, list) else [org_names]
		filters.update({ 'organization_id__in': org_names })

	repos = Repo.objects.filter(**filters)
	if values_list and len(values_list) == 1:
		repos = repos.values_list(*values_list, flat=True)
	elif values_list and len(values_list) > 1:
		repos = repos.values_list(*values_list)

	return list(repos)


def get_enabled_repos(org_name, org_names=[], **kwargs):
	''' get the enable / should_track=true organizations from the db '''
	return get_repos(org_name, org_names=org_names, should_track=True,
		**kwargs)


def get_disabled_repo(org_name, org_names=[], **kwargs):
	''' get the disabled / should_track = false from db '''
	return get_repos(org_name, org_names=org_names, should_track=False,
		**kwargs)
