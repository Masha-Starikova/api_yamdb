import csv

from django.core.management.base import BaseCommand
from reviews.models import User

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели User из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/users.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                user = User()
                user.id = row['id']
                user.username = row['username']
                user.email = row['email']

                if User.objects.filter(id=user.id).exists():
                    self.stdout.write(
                        f'Юзер с id {user.id} уже существует в базе.'
                    )

                elif User.objects.filter(username=user.username).exists():
                    self.stdout.write(
                        f'Юзер c юзернеймом {user.username}'
                        f' уже существует в базе.'
                    )

                elif User.objects.filter(email=user.email).exists():
                    self.stdout.write(
                        f'Юзер с адресом {user.email}'
                        f' уже существует в базе.'
                    )

                else:
                    user = User()
                    user.id = row['id']
                    user.username = row['username']
                    user.email = row['email']
                    user.role = row['role']
                    user.bio = row['bio']
                    user.first_name = row['first_name']
                    user.last_name = row['last_name']
                    user.confirmation_code = row['confirmation_code']
                    user.save()

                    self.stdout.write(f'Юзер {user.username} внесен в базу.')
