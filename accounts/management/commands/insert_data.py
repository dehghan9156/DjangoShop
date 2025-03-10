from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import Profile
from datetime import datetime

User = get_user_model()
class Command(BaseCommand):

    def __init__(self,*args,**kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self,*args,**options):
        for _ in range(6):
            user = User.objects.create_user(email = self.fake.email(),password = 'a@/123456')
            profile= Profile.objects.create(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.created_date = datetime.now()
            profile.save()
