from django.core.management import BaseCommand

from users.models import CustomUser

 
class Command(BaseCommand):
    names_list = ['aadil', 'farhan', 'berlin', 'helsinki', 'aqib', 'jules', 'stark', 'osman', 'dundar']
    def handle(self, *args, **options):
        for name in self.names_list:
            email = name+'@gmail.com'
            password = 'test'
            CustomUser.objects.create_user(email, password, name=name)
            msg = f"user with email {email} has been successfully created "
            self.stdout.write(msg)

