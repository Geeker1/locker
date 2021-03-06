from setuptools import setup

setup(
    name='rental',
    packages=['rental'],
    include_package_data=True,
    install_requires=[
        'flask',
        'bcrypt',
        'flask-sqlalchemy',
        'gunicorn',
        'psycopg2-binary'
    ]
)
