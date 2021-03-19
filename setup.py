from setuptools import setup, find_packages

setup(
    name='django-smorest',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['templates/*'],
    },
    author_email="vazgen@hilearn.io",
    description="Use flask-smorest for django project.",
    classifiers=['Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha'],
    install_requires=["flask==1.1.1",
                      "flask-smorest==0.18.2",
                      "django==2.2.18",
                      "djangorestframework==3.11.0",
                      "webargs==5.5.3"],
)
