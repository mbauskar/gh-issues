from issues.management.commands import IssuesBaseCommand

from issues.api.user import get_user
from issues.models import Organization
from issues.api.organization import get_organizations

class Command(IssuesBaseCommand):
	help = 'Setup super user and organizations'
	output_transaction = True

	def handle(self, **options):
		try:
			user = get_user()
			orgs = get_organizations()

			for org in orgs:
				already_exists = org.githubuser_set.filter(
					username=user.username).exists()
				if not already_exists:
					user.organizations.add(org)

			self.success(f'setup completed')
		except Exception as e:
			self.error(e)