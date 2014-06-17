from setuptools import setup,find_packages

setup(
    name = "pyautoloads",
    version = "0.1",
    package_data = {}, 
    packages = find_packages(),
    install_requires = ["pymysql","sqlalchemy","tornado","mako","pipe"],
    zip_safe = False,
)

