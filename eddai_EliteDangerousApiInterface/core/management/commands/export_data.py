from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.apps import apps

from datetime import datetime

class Command(BaseCommand):
    """
    Export data from the database.
    Args:
        -a, --app (str): The name of the app to export data from. Default is None.
        -m, --model (str): The name of the model to export data from. Default is None.
        -o, --output (str): The name of the file to output the data to. Default is "exported_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json".
        -f, --format (str): The format of the output data. Choices are 'json' or 'xml'. Default is 'json'.
    Methods:
        - add_arguments(parser): Adds command line arguments to the parser.
        - _get_apps(): Returns a list of all app labels.
        - _get_models(app_label): Returns a list of model names for a given app label.
        - _get_model(all_objects, app_label, model_name): Retrieves all objects from a specific model and app.
        - write_to_file(all_objects, output, format_label): Writes the serialized data to a file.
        - handle(*args, **options): Handles the command execution.
    Raises:
        - CommandError: If the provided app or model name is not found.
    """
    help = 'Export data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            "-a", "--app", type=str,
            help="The name of the app to export data from",
            default=None,
        )
        parser.add_argument(
            "-m", "--model", type=str,
            help="The name of the model to export data from",
            default=None,
        )
        parser.add_argument(
            "-o", "--output", type=str,
            help="The name of the file to output the data to",
            default=f"exported_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
        )
        parser.add_argument(
            "-f", "--format", type=str, choices=['json', 'xml'],
            help="The format of the output data",
            default="json",
        )

    def _get_apps(self) -> list[str]:
        """
        Returns a list of labels for all installed Django apps.

        Returns:
            list[str]: A list of labels for all installed Django apps.
        """
        list_of_apps = []
        for app in apps.get_app_configs():
            list_of_apps.append(app.label)
        return list_of_apps
    
    def _get_models(self, app_label:str):
        """
        Get the models of a specific app.

        Parameters:
        - app_label (str): The label of the app.

        Returns:
        - list: A list of model names.

        """
        app_models = []
        for model in apps.get_app_config(app_label).get_models():
            if model._meta:
                app_models.append(model.__name__)
        return app_models

    def _get_model(self, all_objects:list, app_label:str, model_name:str):
        """
        Retrieves a model object based on the provided app label and model name.

        Args:
            all_objects (list): A list to store the retrieved model objects.
            app_label (str): The label of the Django app where the model is defined.
            model_name (str): The name of the model to retrieve.

        Raises:
            CommandError: If the specified model is not found in the given app.

        Returns:
            None
        """
        try:
            model_class = apps.get_model(app_label, model_name)
            all_objects.extend(model_class.objects.all())
        except LookupError:
            raise CommandError(f"Model {model_name} not found in app {app_label}")
        
    def write_to_file(self, all_objects:list, output:str, format_label:str):
        """
        Write the serialized data of the given objects to a file.

        Args:
            all_objects (list): A list of objects to be serialized.
            output (str): The path to the output file.
            format_label (str): The label specifying the serialization format.

        Raises:
            FileExistsError: If the output file already exists.

        """
        serializer = serializers.get_serializer(format_label)
        with open(output, 'x') as file:
            serializer().serialize(all_objects, stream=file)   

    def handle(self, *args, **options):
        self.stdout.write("Starting export...")
        all_objects = []

        app_label = options['app']
        model_name = options['model']
        format_label = options['format']
        output = options['output']

        if app_label != None and model_name != None:
            self.stdout.write(f"Exporting data from model {model_name} in app {app_label}")
            self._get_model(all_objects, app_label, model_name)
        elif app_label != None and model_name == None:
            app_models = self._get_models(app_label)
            for model in app_models:
                self.stdout.write(f"Exporting data from model {model} in app {app_label}")
                self._get_model(all_objects, app_label, model)
        elif app_label == None and model_name == None:
            all_apps = self._get_apps()
            for app in all_apps:
                app_models = self._get_models(app)
                for model in app_models:
                    self.stdout.write(f"Exporting data from model {model} in app {app}")
                    self._get_model(all_objects, app, model)
        else:
            raise CommandError("You must provide an app name or a model name")
    
        self.stdout.write(f"Writing data to {output} in {format_label} format")
        self.write_to_file(all_objects, output, format_label)
        self.stdout.write("Export complete!") 