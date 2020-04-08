from issues.management.commands import IssuesBaseCommand

from issues.api.sync import sync

class Command(IssuesBaseCommand):
	help = 'Fetch issues from github and create / update the issues entries in DB'
	output_transaction = True

	def handle(self, **options):
		try:
			info = sync()
			self.success(f'setup completed')
		except Exception as e:
			import traceback
			traceback.print_exc()
			self.error(e)