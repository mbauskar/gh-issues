from issues.models import Issue
from issues.utils.request import github_request
from issues.utils.date import get_gh_formatted_date, get_formatted_date

from issues.api.user import get_or_create_user
from issues.api.label import get_or_create_labels

issue_pr_keys_to_keeps = [
	'number', 'title', 'state', 'html_url', 'closed_at'
]

def fetch_and_save_repo_issues(repo, last_updated):
	""" fetch from the repo and create or update the db """

	uri = 'repos/LiveHealth/livehealthapp/issues'
	filters = {
		'page': 1,
		'state': 'open',
		'per_page': 100,
		'sort': 'created',
		'direction': 'asc'
	}
	if last_updated:
		filters.update({
			'sort': 'updated',
			'since': get_gh_formatted_date(last_updated)
		})

	issues = github_request(uri, payload=filters)
	issue_numbers = [ issue.get('number', None) for issue in issues \
		if issue.get('number', None) ]
	available_issues = get_issues(repo, number__in=issue_numbers)
	available_issues = { issue.number: issue for issue in available_issues }

	to_insert = []

	for issue in issues:
		is_pull = issue.get('pull_request', None)
		print('Issue', issue.get('title', 'NA'))
		if is_pull:
			continue

		author = get_or_create_user(issue.get('user', {}))
		assigned_to = get_or_create_user(issue.get('assignee', {}))
		labels = get_or_create_labels(issue.get('labels', []))

		args = { key: issue.get(key, None) for key in issue_pr_keys_to_keeps }
		conversion_format = '%Y-%m-%dT%H:%M:%SZ'
		args.update({
			'repo_id': repo,
			'author': author,
			'assigned_to': assigned_to,
			'gh_created_at': get_formatted_date(issue.get('created_at', None),
				conversion_format=conversion_format),
			'gh_updated_at': get_formatted_date(issue.get('updated_at', None),
				conversion_format=conversion_format)
		})

		if issue.get('number', None) in available_issues:
			db_issue = available_issues.get(issue.get('number', None), None)

			# to do check if we need to update labels or linked PR
			for key, val in args.items():
				setattr(db_issue, key, val)
			db_issue.save()
		else:
			if labels:
				args.update({ 'labels': labels })

			to_insert.append(args)

	# # bulk insert issues
	bulk_insert_issues(to_insert)


def bulk_insert_issues(issues):
	""" bulk insert issues into db """
	issue_labels = { issue.get('number', 'NA'): issue.pop('labels', []) \
		for issue in issues }

	# bulk inset does not return id's we need id to insert labels
	# issues = [ Issue(**issue) for issue in issues ]
	# db_issues = Issue.objects.bulk_create(issues)

	# add labels
	for args in issues:
		issue = Issue(**args)
		issue.save()
		if issue.number not in issue_labels:
			continue

		labels = issue_labels.get(issue.number, [])
		issue.labels.add(*labels)
		issue.save()


def get_issues(repo, repos=[], values_list=[], **kwargs):
	""" get the issue from db based on filters provided by users """

	filters = {}
	annotate = kwargs.pop('annotate', None)

	filters.update(kwargs)
	if repo:
		repos = [repo]

	repos = repos if isinstance(repos, list) else [repos]
	filters.update({ "repo_id__in": repos })

	issues = Issue.objects.filter(**filters)
	if annotate:
		issues = issues.annotate(**annotate)

	if values_list and len(values_list) == 1:
		issues = issues.values_list(*values_list, flat=True)
	elif values_list and len(values_list) > 1:
		issues = issues.values_list(*values_list)

	return list(issues)


def get_last_updated_date_from_issues(repo=None, repos=[], **kwargs):
	""" get last updated date for the repository from issues """
	return get_issues(repo, repos=repos, **kwargs)
