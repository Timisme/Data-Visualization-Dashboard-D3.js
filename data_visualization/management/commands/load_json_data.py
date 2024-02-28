import json
import os
from datetime import datetime
from django.db import transaction
from data_visualization.models import DataPoint
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Loads data from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str,
                            help='Path to the JSON file containing the data')

    def handle(self, *args, **options):
        # Path to the JSON file
        json_file_path = options['json_file']

        # Ensure the file exists
        if not os.path.isfile(json_file_path):
            raise CommandError(
                'File "{}" does not exist.'.format(json_file_path))

        # Open and load the JSON file
        with open(json_file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

            # Iterate over each entry in the JSON data
            instances = []
            for entry in data:
                try:
                    # Create and save a new DataPoint instance
                    field_names = [field.name for field in DataPoint._meta.get_fields() if field.name != "id"]
                    kwargs = {}
                    for field_name in field_names:
                        # turn string datetime into datetime object
                        if field_name in ["added", "published"]:
                            if entry[field_name] != "":
                                value = datetime.strptime(entry[field_name], "%B, %d %Y %H:%M:%S")
                            else:
                                value = None
                        else:
                            value = entry[field_name] if entry[field_name] != "" else None

                        kwargs[field_name] = value

                    instances.append(DataPoint(**kwargs))
                except Exception as e:
                    # If an error occurs, print it and skip to the next entry
                    print(f"Error loading entry: {e}")
                    continue

            #TODO: use bulk create instead (skip existing ones)
            with transaction.atomic():
                DataPoint.objects.all().delete()
                DataPoint.objects.bulk_create(instances)

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded data from "{}"'.format(json_file_path))
        )
