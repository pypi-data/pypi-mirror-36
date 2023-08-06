from setuptools import find_packages, setup
# Read more here: https://www.codementor.io/arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku

setup(
    name='simple_django_logger',
    # packages=[
    #     'simple_django_logger',  # this must be the same as the name above
    #     'simple_django_logger.middleware',
    #     'simple_django_logger.migrations'],
    packages=find_packages(),
    include_package_data=True,
    version='3.0.0',
    description='A basic logger for Django',
    author='Eshan Das',
    author_email='eshandasnit@gmail.com',
    url='https://github.com/eshandas/simple_django_logger',  # use the URL to the github repo
    download_url='https://github.com/eshandas/simple_django_logger/archive/3.0.0.tar.gz',  # Create a tag in github
    keywords=['django', 'logger'],
    classifiers=[],
    install_requires=[
        'Django>=2.0',
        'requests>=2.0',
        'djangorestframework>=3.8',
        'user-agents>=1.1.0',
        'django-user-agents>=0.3.2'],
)
