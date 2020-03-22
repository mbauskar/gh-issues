from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, null=False)
	updated_at = models.DateTimeField(auto_now=True, null=False)

	class Meta:
		abstract = True


class User(AbstractUser, BaseModel):
	github_username = models.CharField(max_length=255, null=False, primary_key=True)


class Organization(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)


class Repo(BaseModel):
	name = models.CharField(max_length=255, null=False, unique=True)
	full_name = models.CharField(max_length=255, null=False, unique=True)
	private = models.BooleanField()
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Team(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)


class Label(BaseModel):
	name = models.CharField(max_length=255, null=False, primary_key=True)
	color = models.CharField(max_length=255)


class Issue(BaseModel):
	number = models.IntegerField(null=False)
	html_url = models.TextField(null=False)
	title = models.TextField(null=False)
	status = models.CharField(max_length=255, null=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
	closed_at = models.DateTimeField()


class PullRequest(BaseModel):
	number = models.IntegerField(null=False)
	html_url = models.TextField(null=False)
	title = models.TextField(null=False)
	draft = models.BooleanField(default=False)
	status = models.CharField(max_length=255, null=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
	closed_at = models.DateTimeField()
	merged_at = models.DateTimeField()


class TeamMember(BaseModel):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	member = models.ForeignKey(User, on_delete=models.CASCADE)


class IssueLabel(BaseModel):
	issue = models.ForeignKey(GitHubIssue, on_delete=models.CASCADE)
	label = models.ForeignKey(Label, on_delete=models.CASCADE)


class LinkedPullRequest(BaseModel):
	issue = models.ForeignKey(GitHubIssue, on_delete=models.CASCADE)
	pull_request = models.ForeignKey(GitHubPullRequest, on_delete=models.CASCADE)

