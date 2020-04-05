from django.core.management.base import BaseCommand

class IssuesBaseCommand(BaseCommand):
    def warning(self, msg):
        self.stdout.write(self.style.WARNING(msg))
    
    def error(self, msg):
        self.stdout.write(self.style.ERROR(msg))
    
    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))