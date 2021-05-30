#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pipreqs - Generate pip requirements.txt file based on imports

Usage:
    pipreqs [options] [<path>]

Arguments:
    <path>                The path to the directory containing the application
                          files for which a requirements file should be
                          generated (defaults to the current working
                          directory).

Options:
    --use-local           Use ONLY local package info instead of querying PyPI.
    --pypi-server <url>   Use custom PyPi server.
    --proxy <url>         Use Proxy, parameter will be passed to requests
                          library. You can also just set the environments
                          parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information.
    --ignore <dirs>...    Ignore extra directories, each separated by a comma.
    --no-follow-links     Do not follow symbolic links in the project
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard
                          output.
    --force               Overwrite existing requirements.txt
    --diff <file>         Compare modules in requirements.txt to project
                          imports.
    --clean <file>        Clean up requirements.txt by removing modules
                          that are not imported in project.
    --no-pin              Omit version of output packages.
"""
from __future__ import print_function, absolute_import
from contextlib import contextmanager
import os
import sys
import re
import codecs
import ast
import traceback

REGEXP = [
    re.compile(r'^import (.+)$'),
    re.compile(r'^from ((?!\.+).*?) import (?:.*)$')
]

if sys.version_info[0] > 2:
    open_func = open
    py2 = False
else:
    open_func = codecs.open
    py2 = True
    py2_exclude = ["concurrent", "concurrent.futures"]


@contextmanager
def _open(filename=None, mode='r'):
    """Open a file or ``sys.stdout`` depending on the provided filename.

    Args:
        filename (str): The path to the file that should be opened. If
            ``None`` or ``'-'``, ``sys.stdout`` or ``sys.stdin`` is
            returned depending on the desired mode. Defaults to ``None``.
        mode (str): The mode that should be used to open the file.

    Yields:
        A file handle.

    """
    if not filename or filename == '-':
        if not mode or 'r' in mode:
            file = sys.stdin
        elif 'w' in mode:
            file = sys.stdout
        else:
            raise ValueError('Invalid mode for file: {}'.format(mode))
    else:
        file = open(filename, mode)

    try:
        yield file
    finally:
        if file not in (sys.stdin, sys.stdout):
            file.close()


def get_all_imports(
        path, encoding=None, extra_ignore_dirs=None, follow_links=True):
    imports = set()
    raw_imports = set()
    candidates = []
    ignore_errors = False
    ignore_dirs = [".hg", ".svn", ".git", ".tox", "__pycache__", "env", "venv"]

    if extra_ignore_dirs:
        ignore_dirs_parsed = []
        for e in extra_ignore_dirs:
            ignore_dirs_parsed.append(os.path.basename(os.path.realpath(e)))
        ignore_dirs.extend(ignore_dirs_parsed)

    walk = os.walk(path, followlinks=follow_links)
    for root, dirs, files in walk:
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        candidates.append(os.path.basename(root))
        files = [fn for fn in files if os.path.splitext(fn)[1] == ".py"]

        candidates += [os.path.splitext(fn)[0] for fn in files]
        for file_name in files:
            file_name = os.path.join(root, file_name)
            with open_func(file_name, "r", encoding=encoding) as f:
                contents = f.read()
            try:
                tree = ast.parse(contents)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for subnode in node.names:
                            raw_imports.add(subnode.name)
                    elif isinstance(node, ast.ImportFrom):
                        raw_imports.add(node.module)
            except Exception as exc:
                if ignore_errors:
                    traceback.print_exc(exc)
                    print("Failed on file: %s" % file_name)
                    continue
                else:
                    print("Failed on file: %s" % file_name)
                    raise exc

    # Clean up imports
    for name in [n for n in raw_imports if n]:
        # Sanity check: Name could have been None if the import
        # statement was as ``from . import X``
        # Cleanup: We only want to first part of the import.
        # Ex: from django.conf --> django.conf. But we only want django
        # as an import.
        cleaned_name, _, _ = name.partition('.')
        imports.add(cleaned_name)

    packages = imports - (set(candidates) & imports)

    with open(join("stdlib"), "r") as f:
        data = {x.strip() for x in f}

    data = {x for x in data if x not in py2_exclude} if py2 else data
    return list(packages - data)


def filter_line(l):
    return len(l) > 0 and l[0] != "#"


def generate_requirements_file(path, imports):
    with _open(path, "w") as out_file:
        print('Writing {num} requirements: {imports} to {file}'.format(
            num=len(imports),
            file=path,
            imports=", ".join([x['name'] for x in imports])
        ))
        fmt = '{name}=={version}'
        out_file.write('\n'.join(
            fmt.format(**item) if item['version'] else '{name}'.format(**item)
            for item in imports) + '\n')


def output_requirements(imports):
    generate_requirements_file('-', imports)


def get_locally_installed_packages(encoding=None):
    packages = {}
    ignore = ["tests", "_tests", "egg", "EGG", "info"]
    for path in sys.path:
        for root, dirs, files in os.walk(path):
            for item in files:
                if "top_level" in item:
                    item = os.path.join(root, item)
                    with open_func(item, "r", encoding=encoding) as f:
                        package = root.split(os.sep)[-1].split("-")
                        try:
                            package_import = f.read().strip().split("\n")
                        except:  # NOQA
                            # TODO: What errors do we intend to suppress here?
                            continue
                        for i_item in package_import:
                            if ((i_item not in ignore) and
                                    (package[0] not in ignore)):
                                version = None
                                if len(package) > 1:
                                    version = package[1].replace(
                                        ".dist", "").replace(".egg", "")

                                packages[i_item] = {
                                    'version': version,
                                    'name': package[0]
                                }
    return packages


def get_import_local(imports):
    local = get_locally_installed_packages()
    result = []
    for item in imports:
        if item.lower() in local:
            result.append(local[item.lower()])
        elif item in local:
            result.append(local[item])

    # removing duplicates of package/version
    result_unique = [
        dict(t)
        for t in set([
            tuple(d.items()) for d in result
        ])
    ]

    return result_unique


def get_pkg_names(pkgs):
    """Get PyPI package names from a list of imports.

    Args:
        pkgs (List[str]): List of import names.

    Returns:
        List[str]: The corresponding PyPI package names.

    """
    result = set()
    with open(join("mapping"), "r") as f:
        data = dict(x.strip().split(":") for x in f)
    for pkg in pkgs:
        # Look up the mapped requirement. If a mapping isn't found,
        # simply use the package name.
        result.add(data.get(pkg, pkg))
    # Return a sorted list for backward compatibility.
    return sorted(result, key=lambda s: s.lower())


def get_name_without_alias(name):
    if "import " in name:
        match = REGEXP[0].match(name.strip())
        if match:
            name = match.groups(0)[0]
    return name.partition(' as ')[0].partition('.')[0].strip()


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


def parse_requirements(file_):
    """Parse a requirements formatted file.

    Traverse a string until a delimiter is detected, then split at said
    delimiter, get module name by element index, create a dict consisting of
    module:version, and add dict to list of parsed modules.

    Args:
        file_: File to parse.

    Raises:
        OSerror: If there's any issues accessing the file.

    Returns:
        tuple: The contents of the file, excluding comments.
    """
    modules = []
    # For the dependency identifier specification, see
    # https://www.python.org/dev/peps/pep-0508/#complete-grammar
    delim = ["<", ">", "=", "!", "~"]

    try:
        f = open_func(file_, "r")
    except OSError:
        print("Failed on file: {}".format(file_))
        raise
    else:
        try:
            data = [x.strip() for x in f.readlines() if x != "\n"]
        finally:
            f.close()

    data = [x for x in data if x[0].isalpha()]

    for x in data:
        # Check for modules w/o a specifier.
        if not any([y in x for y in delim]):
            modules.append({"name": x, "version": None})
        for y in x:
            if y in delim:
                module = x.split(y)
                module_name = module[0]
                module_version = module[-1].replace("=", "")
                module = {"name": module_name, "version": module_version}

                if module not in modules:
                    modules.append(module)

                break

    return modules


def compare_modules(file_, imports):
    """Compare modules in a file to imported modules in a project.

    Args:
        file_ (str): File to parse for modules to be compared.
        imports (tuple): Modules being imported in the project.

    Returns:
        tuple: The modules not imported in the project, but do exist in the
               specified file.
    """
    modules = parse_requirements(file_)

    imports = [imports[i]["name"] for i in range(len(imports))]
    modules = [modules[i]["name"] for i in range(len(modules))]
    modules_not_imported = set(modules) - set(imports)

    return modules_not_imported


def diff(file_, imports):
    """Display the difference between modules in a file and imported modules."""  # NOQA
    modules_not_imported = compare_modules(file_, imports)

    print(
        "The following modules are in {} but do not seem to be imported: "
        "{}".format(file_, ", ".join(x for x in modules_not_imported)))


def clean(file_, imports):
    """Remove modules that aren't imported in project from file."""
    modules_not_imported = compare_modules(file_, imports)
    re_remove = re.compile("|".join(modules_not_imported))
    to_write = []

    try:
        f = open_func(file_, "r+")
    except OSError:
        print("Failed on file: {}".format(file_))
        raise
    else:
        try:
            for i in f.readlines():
                if re_remove.match(i) is None:
                    to_write.append(i)
            f.seek(0)
            f.truncate()

            for i in to_write:
                f.write(i)
        finally:
            f.close()

    print("Successfully cleaned up requirements in " + file_)


def make_requirements(path):
    encoding = "utf-8"

    candidates = get_all_imports(path,
                                 encoding=encoding,
                                 extra_ignore_dirs=None,
                                 follow_links=True)

    # dependents_candidates = dict()
    # models = list()
    # for candidate_id, candidate in enumerate(candidates):
    #     exec(f"import {candidate} as dependent_module\n"
    #          f"models.append(dependent_module)", {"models": models})
    #     dependent_file_path = models[candidate_id].__file__
    #     dependent_path = os.path.split(dependent_file_path)[0]
    #     dependent_candidates = get_all_imports(dependent_path,
    #                                            encoding=encoding,
    #                                            extra_ignore_dirs=None,
    #                                            follow_links=True)
    #     if candidate in dependent_candidates:
    #         dependent_candidates.remove(candidate)
    #     dependent_candidates = get_pkg_names(dependent_candidates)
    #     dependent_packages_name = get_import_local(dependent_candidates)
    #     dependent_packages_name = dict([(item["name"].replace("_", "-"), item["version"])
    #                                     for item in dependent_packages_name])
    #     dependents_candidates[candidate] = dependent_packages_name

    candidates = get_pkg_names(candidates)

    local = get_import_local(candidates)
    # Get packages that were not found locally

    local_package = dict([(item["name"].replace("_", "-"), item["version"]) for item in local])
    return local_package


