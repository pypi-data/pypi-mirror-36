from setuptools import find_packages, setup

VERSION = '0.2'


setup(
    name='git-ignore',
    version=VERSION,
    description='Git ignore template helper',
    url='https://github.com/hanpannet/Git-ignore',
    author='Qiushi Pan',
    author_email='ice.gitshell@gmail.com',
    license='MIT',
    keywords='git gitignore template default',
    packages=find_packages(),
    package_data={
        'git_ignore': ['template/*.gitignore'],
    },
    # include_package_data=True,
    install_requires=["click >= 6.7"],
    # scripts = ['directory/__main__.py'],
    entry_points={'console_scripts': 'git-ignore = git_ignore:main'},
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)
