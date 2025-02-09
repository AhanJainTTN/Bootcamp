How Python Searches for a Module: The first thing Python will do is look up the name abc in sys.modules. This is a cache of all modules that have been previously imported. If the name isn’t found in the module cache, Python will proceed to search through a list of built-in modules. These are modules that come pre-installed with Python and can be found in the Python Standard Library. If the name still isn’t found in the built-in modules, Python then searches for it in a list of directories defined by sys.path. This list usually includes the current directory, which is searched first. When Python finds the module, it binds it to a name in the local scope. This means that abc is now defined and can be used in the current file without throwing a NameError. If the name is never found, you’ll get a ModuleNotFoundError.

Absolute and Relative Imports

Absolute imports are dependent on sys.path. Any relative path stemming from sys.path can be used to import a package. We can append to sys.path or PYTHONPATH as well if necessary.

Relative imports are only possible if "**package**" is defined i.e. the module should be run as part of a package since that is how it is able to resolve the '.', '..' etc.

"**package**" = package.subpackage.module means the module is part of a subpackage which itself is part of package. This is how it can either go to current directory or '.' i.e. inside .../subpackage/ or inside parent directory or '..' i.e. inside .../package.

Enough information in **package** should be there for effective traversal i.e. if one of the imports are using .. there should at least be two levels in **package** i.e. package.subpackage is the bare minimum nesting needed. Anything less like just subpackage will not work.

When the script is run from some location using the -m location, sys.path[0] reflects the location the script is run from. Also when we are writing the command i.e. pthon3 -m package.subpackage.main we are essentially telling which package and subpackage does main belong to i.e. the package structure. Addtionally where we are running the script from should also be able to build the path.

Ex: If we are running the file as a module from /root/ and the module is in /root/parent/package/subpackage/main.py then we will write python3 -m parent.package.subpackage.main.

This is because to use relative imports the complete path is built from sys.path and **package**

We can say that the absolute path for the module is sys.path + **package**.

sys.path is set either explicity using sys.path.append()
