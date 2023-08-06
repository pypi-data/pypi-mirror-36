from setuptools import setup

def readme():
    try:
        import pypandoc
        return pypandoc.convert_file('README.md', 'rst')

    except (ImportError, IOError, OSError):
        with open('README.md') as f:
            return f.read()

setup(
    name = 'jakopicevca',
    version = '1.1',
    description = 'Programs for Astro Pi - Mission Space Lab - Team Jakopičevca',
    long_description = readme(),
    license = 'GPLv3+',

    install_requires = [
        'jakopicevca2017'
    ],

    extras_require = {
        'pandoc': ['pypandoc']
    },

    author = 'Team Jakopičevca',
    author_email = 'filip.stamcar@hotmail.com',
    url = 'https://github.com/filips123/jakopicevca/',
    keywords = 'RaspberryPi AstroPi MissionSpaceLab OŠRJ ESA',
    platforms = 'Linux',

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy'
    ],

    include_package_data = True
)
