from simple_history import register
from django.apps import apps

models = list(apps.get_app_config('core').get_models()) + list(apps.get_app_config('service').get_models())
models = [model for model in models]
for model in models:
    register(model)
