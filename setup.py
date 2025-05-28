from setuptools import setup, find_packages

setup(
    name='freelance_project_tracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'SQLAlchemy'
    ],
    entry_points={
        'console_scripts': [
            'fpt=app.cli:cli',
        ],
    },
)
