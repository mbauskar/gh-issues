from django.db import models
from django.contrib.auth.models import AbstractUser

from base.base_model import BaseModel

class GitHubUser(AbstractUser, BaseModel):
	github_username = models.CharField(max_length=255, null=False, unique=True)

	class Meta:
		db_table = 'GitHubUser'


class Organization(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)

	class Meta:
		db_table = 'Organization'


class Repo(BaseModel):
	name = models.CharField(max_length=255, null=False, unique=True)
	full_name = models.CharField(max_length=255, null=False, unique=True)
	private = models.BooleanField()
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

	class Meta:
		db_table = 'Repo'


class Team(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)
	members = models.ManyToManyField(GitHubUser)
	
	class Meta:
		db_table = 'Team'


class Label(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)
	color = models.CharField(max_length=255)

	class Meta:
		db_table = 'Label'


class GithubBase(models.Model):
	number = models.IntegerField(null=False, unique=True)
	title = models.TextField(null=False)
	status = models.CharField(max_length=255, null=False)
	html_url = models.TextField(null=False)

	labels = models.ManyToManyField(Label)

	# dates to capture
	opened_at = models.DateTimeField()
	closed_at = models.DateTimeField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		abstract = True


class PullRequest(GithubBase):
	draft = models.BooleanField(default=False)
	author = models.ForeignKey(GitHubUser, on_delete=models.CASCADE,
		related_name='pr_author')
	merged_at = models.DateTimeField()
	reviewers = models.ManyToManyField(GitHubUser, through='PullRequestReviewer')

	class Meta:
		indexes = [
			models.Index(fields=['number']),
			models.Index(fields=['status']),
			models.Index(fields=['author']),
			models.Index(fields=['author', 'status']),
		]
		db_table = 'PullRequest'


class Issue(GithubBase):
	author = models.ForeignKey(GitHubUser, on_delete=models.CASCADE,
		related_name='issue_author')
	assigned_to = models.ForeignKey(GitHubUser, on_delete=models.CASCADE,
		related_name='issue_assigned_to')
	pull_requests = models.ManyToManyField(PullRequest)

	class Meta:
		indexes = [
			models.Index(fields=['number']),
			models.Index(fields=['status']),
			models.Index(fields=['author']),
			models.Index(fields=['assigned_to']),
			models.Index(fields=['author', 'status']),
		]
		db_table = 'Issue'


class PullRequestReviewer(BaseModel):
	pull_request = models.ForeignKey(PullRequest, on_delete=models.CASCADE)
	reviewer = models.ForeignKey(GitHubUser, on_delete=models.CASCADE)
	status = models.CharField(max_length=255, null=False)
	submitted_at = models.DateTimeField()
	
	class Meta:
		db_table = 'PullRequestReviewer'


# class TeamMember(BaseModel):
# 	team = models.ForeignKey(Team, on_delete=models.CASCADE)
# 	member = models.ForeignKey(GitHubUser, on_delete=models.CASCADE)

# 	class Meta:
# 		db_table = 'TeamMember'


# class IssueLabel(BaseModel):
# 	issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
# 	label = models.ForeignKey(Label, on_delete=models.CASCADE)

# 	class Meta:
# 		db_table = 'IssueLabel'


# class LinkedPullRequest(BaseModel):
# 	issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
# 	pull_request = models.ForeignKey(PullRequest, on_delete=models.CASCADE)

# 	class Meta:
# 		db_table = 'LinkedPullRequest'

