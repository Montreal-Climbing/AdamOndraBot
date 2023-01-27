import setuptools

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name = 'ondra-bot',
    version = '0.1.0',
    description = 'A discord bot',
    long_description = readme,
    packages = setuptools.find_packages()
)
