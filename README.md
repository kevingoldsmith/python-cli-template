# python-cli-template
a template repo for my python cli projects, just to speed things up. The
template project has support for a config file, argument parsing, command-line
and file logging. The project also uses Black for cleaning up, PyLint for
linting, PyTest for testing and mypy for type-checking. It also includes the
start of makefile.

It does not include any support for documentation, packaging or anything else
yet, because I don't tend to do that for these types of projects, but I may
add that in the future.

To get things going, you can
```
make init
source venv/bin/activate
make all
```

* the template.py and test_template.py files should be renamed for a new project
* _CONFIG_FILE and _LOG_FILE constants should be updated
* add your business logic in main()
