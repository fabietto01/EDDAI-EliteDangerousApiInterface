from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.apps import apps

class Command(BaseCommand):
    """
    Import data into the database.
    Args:
        input (str): The name of the file to import data from.
        format (str): The format of the input data. Choices are 'json' or 'xml'. Default is 'json'.
    Raises:
        FileNotFoundError: If the input file is not found.
        CommandError: If there is an error deserializing the data or any other exception occurs.
    Returns:
        None
    """
    help = 'Import data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            "-i", "--input", type=str,
            help="The name of the file to import data from",
            required=True,
        )
        parser.add_argument(
            "-f", "--format", type=str, choices=['json', 'xml'],
            help="The format of the input data",
            default="json",
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting import...")

        input_file = options['input']
        format_label = options['format']

        try:
            
            with open(input_file, 'r') as file:
                for obj in serializers.deserialize(format_label, file):
                    obj.save()

        except FileNotFoundError:
            raise CommandError(f"File {input_file} not found")
        except serializers.base.DeserializationError as e:
            raise CommandError(f"Error deserializing data: {e}")
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")