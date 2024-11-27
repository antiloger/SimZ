import os
import importlib.util

def load_custom_components(directory: str):
    for file in os.listdir(directory):
        if file.endswith(".py"):
            module_name = file[:-3]
            module_path = os.path.join(directory, file)
            
            try:

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is None:
                    raise ImportError(f"Cannot find spec for {module_name}")

                if spec.loader is None:
                    raise ImportError(f"No loader found for {module_name}")
                module = importlib.util.module_from_spec(spec)
                if module is None:
                    raise ValueError("Error happening")
                # spec.loader.exec_module()
                spec.loader.exec_module(module)
            except Exception as e :
                print(f"Error loading custom component module {e}")
