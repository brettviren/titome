import setuptools

# ver_globals = {}
# with open("moo/version.py") as fp:
#     exec(fp.read(), ver_globals)
# version = ver_globals["version"]
version = '0.0.0'

setuptools.setup(
    name="titome",
    version=version,
    author="Brett Viren",
    author_email="brett.viren@gmail.com",
    description="Time To Meet",
    url="https://brettviren.github.io/titome",
    py_modules=['titome'],
    python_requires='>=3.5',    # use of typing probably drive this
    install_requires=[
        "click",
        "rich",
        "arrow",
    ],
    entry_points = dict(
        console_scripts = [
            'titome = titome:main',
        ]
    ),
    include_package_data=True,
)
