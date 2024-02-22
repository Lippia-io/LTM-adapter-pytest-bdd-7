from setuptools import setup, find_packages

setup(
    name='pytest-bdd-7-adapter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
    ],
    description='Un adaptador para pytest-bdd',
    dependency_links=[
        'git+ssh://git@ssh.crowdaronline.com:lippia/products/test-manager/adapters/pytest-bdd-7-adapter.git@CMasche#egg=pytest-bdd-7-adapter'
    ],
    license='MIT'
)
