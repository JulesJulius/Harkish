import os
import importlib
from modules import Module

class ModuleLoader:
    def __init__(self, client):
        self.client = client
        self.modules = []
        self.load_modules()

    def load_modules(self):
        module_dir = 'modules'
        for module_file in os.listdir(module_dir):
            if module_file.endswith('.py') and module_file != '__init__.py':
                module_name = module_file[:-3]
                module = importlib.import_module(f'{module_dir}.{module_name}')
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, Module) and obj != Module:
                        self.modules.append(obj(self.client))

    async def on_message(self, message):
        for module in self.modules:
            await module.on_message(message)
