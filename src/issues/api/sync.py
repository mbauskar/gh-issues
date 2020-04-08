from django.db.models import Max

from issues.api.repo import get_enabled_repos
from issues.api.issue import (fetch_and_save_repo_issues,
	get_last_updated_date_from_issues)

def sync():
	'''
		fetch github issue of all the enabled organizations and repositories
		and create or update issues in DB
	'''

	enabled_repos = get_enabled_repos(None, values_list=['id'])
	if not enabled_repos:
		return {}

	annotate = { 'last_updated': Max('gh_updated_at') }
	issues = get_last_updated_date_from_issues(repo=None, repos=enabled_repos,
		values_list=['repo_id', 'last_updated'], annotate=annotate)
	last_updated_mapper = { issue[0]: issue[1] for issue in issues }

	for repo in enabled_repos:
		last_updated = last_updated_mapper.get(repo, None)
		fetch_and_save_repo_issues(repo, last_updated=last_updated)
