# coding: utf-8


import sys


__APP_NAME = "Phony"


def check_requirements():
    py_required_version = (3, 8, 10)
    if sys.version_info < py_required_version:
        py_version_str = "{}.{}.{}".format(*py_required_version)
        sys.exit("{} requires Python >= {}".format(__APP_NAME, py_version_str))

def run():
    import generator.phone_number_generator as app
    app.run()

if __name__ == "__main__":
    check_requirements()
    run()
