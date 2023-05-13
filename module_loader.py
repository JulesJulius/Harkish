import os
import importlib
from modules import Module
import config

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
                        module_args = config.modules.get(module_name, {})
                        self.modules.append(obj(self.client, **module_args))

    async def on_message(self, message):
        for module in self.modules: await module.on_message(message)

    async def on_ready(self):
        for module in self.modules: await module.on_ready()

    async def on_connect(self):
        for module in self.modules: await module.on_connect()