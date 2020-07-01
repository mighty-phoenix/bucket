import csv
from django.core.management.base import BaseCommand, CommandError
from subjects.models import Content

## https://dev.to/arsho/writing-django-custom-command-1dl0
## https://gist.github.com/trhura/6395787


content_urls = ['youtube', 'imdb', 'goodreads', 'instagram', 'facebook']

def generate_user(user_pks):
    pk = random.choice(user_pks)
    user = BucketUser.objects.get(pk=pk)
    return user

def generate_subject(subject_pks):
    pk = random.choice(subject_pks)
    subject = Subject.objects.get(pk=pk)
    return subject

def generate_type():
    i = len(CONTENT_TYPES)
    index = random.randint(0,i-1)
    return CONTENT_TYPES[index][0]

def generate_content_url(content_urls):
    i = len(content_urls)
    index = random.randint(0,i-1)
    content_url = 'www.' + content_urls[index] + '.com/' + get_random_string()
    return content_url


class Command(BaseCommand):
    help = 'Upload from csv to Content model.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = Content

    def insert_data_to_db(self, data):
        try:
            self.model_name.objects.create(
                title = data['name'],
                type = 'movie',
                creator = data['director'],
                description = data['description'],
                content_url = data['url']
            )
        except Exception as e:
            raise CommandError("Error in inserting {}: {}".format(
                self.model_name, str(e)))

    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+', type=str, help='The csv file that contains the data.')

    def handle(self, *args, **kwargs):
        for filename in kwargs['filenames']:
            self.stdout.write(self.style.SUCCESS('Reading:{}'.format(filename)))
            try:
                with open(f'{filename}.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if row != "":
                            words = [word.strip() for word in row]
                            data = {
                                'name': words[0],
                                'url': words[1],
                                'description': words[3].strip('\"'),
                                'director': words[4],
                            }
                            self.insert_data_to_db(data)
            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    filename))
