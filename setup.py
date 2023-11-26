import os

from setuptools import setup
from setuptools import find_packages
from qpt.version import version

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.MD"), encoding='utf-8') as f:
    long_description = '\n' + f.read()
# long_description = '\n' + "https://github.com/QPT-Family/QPT"

setup(
    name='QPT',
    version=version,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GT-ZhangAcer/QPT',
    license='LGPL',
    author='GT-ZhangAcer',
    author_email='zhangacer@foxmail.com',
    description='QPT-Python环境打包工具',
    install_requires=['wget',
                      "click",
                      "pefile",
                      "pillow",
                      "toml",
                      "pip>=23.1",
                      "QPT-SDK"],
    python_requires='>=3.8',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'qpt = qpt.command:cli',
        ]}
)
