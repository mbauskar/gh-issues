from django.contrib import admin

# Register your models here.
from issues.models import (
	Organization, GitHubUser, Repo, Team, Label, PullRequest, Issue, PullRequestReviewer)

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'should_track')

class GitHubUserAdmin(admin.ModelAdmin):
	list_display = ('github_username', 'first_name', 'last_name')

class RepoAdmin(admin.ModelAdmin):
	list_display = ('name', 'should_track')

class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', )

class LabelAdmin(admin.ModelAdmin):
	list_display = ('name', )

class PullRequestAdmin(admin.ModelAdmin):
	list_display = ('number', 'title', 'state')

class IssueAdmin(admin.ModelAdmin):
	list_display = ('number', 'title', 'state')

class PullRequestReviewerAdmin(admin.ModelAdmin):
	list_display = ('name', 'status')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(GitHubUser, GitHubUserAdmin)
admin.site.register(Repo, RepoAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(PullRequest, PullRequestAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Label, LabelAdmin)
# admin.site.register(PullRequestReviewer, PullRequestReviewerAdmin)