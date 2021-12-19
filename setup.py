import os

from setuptools import setup
from setuptools import find_packages
from qpt.version import version

# with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.MD"), encoding='utf-8') as f:
#     long_description = '\n' + f.read()
long_description = '\n' + "https://github.com/QPT-Family/QPT"

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
    description='QPT-基于Python的快捷环境封装工具',
    install_requires=['wget',
                      "click",
                      "pefile",
                      "pillow",
                      "ttkbootstrap"],
    python_requires='>3.5',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'qpt = qpt.command:cli',
        ]}
)
