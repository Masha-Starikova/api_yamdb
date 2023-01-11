import csv

from django.core.management.base import BaseCommand
from reviews.models import Title, Review, Category, Genre

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели User из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/titles.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                titles = Title()
                titles.id = row['id']
                titles.name = row['name']
                titles.year = row['year']
                titles.category = row['category']

        with open(
            f'{IMPORT_DATA_ADRESS}/review.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                reviews = Review()
                reviews.id = row['id']
                reviews.title = row['title_id']
                reviews.text = row['year']
                reviews.author = row['autor']
                reviews.score = row['score']
                reviews.pub_date = row['pub_date']

        with open(
            f'{IMPORT_DATA_ADRESS}/genre.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                genre = Genre()
                genre.id = row['id']
                genre.name = row['name']
                genre.slug = row['slug']

        with open(
            f'{IMPORT_DATA_ADRESS}/category.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                category = Category()
                category.id = row['id']
                category.name = row['name']
                category.slug = row['slug']
