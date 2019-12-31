# from importlib import import_module
# from pathlib import Path

# __all__ = [
#     import_module(f".{f.stem}", __package__)
#     for f in Path(__file__).parent.glob("*.py")
#     if "__" not in f.stem
# ]
# del import_module, Path

__all__ = ["capsule", "navigation", "screenbase", "parentnamescreen"]
# import os
# for module in os.listdir(os.path.dirname(__file__)):
#     if module == '__init__.py' or module[-3:] != '.py':
#         continue
#     __import__(module[:-3], locals(), globals())
# del module