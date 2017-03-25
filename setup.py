from setuptools import setup, find_packages

packages = find_packages()
setup(name='beylerbey',
      version='0.1.0',
      packages=packages,
      install_requires=[
          'SQLAlchemy>=1.0.12',
          # async
          'asyncio_extras',  # for async context managers
          'aiohttp',  # for working with http
          'asyncpg',  # for working with Postgres
          'aiomysql',  # for working with MySQL
      ])
