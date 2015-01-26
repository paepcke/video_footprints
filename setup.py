from setuptools import setup, find_packages

test_requirements = ['mongomock>=1.0.1', 'sentinels>=0.0.6', 'nose>=1.0', 'python-dateutil>=2.2']

setup(
    name = "video_footprints",
    version = "0.1",
    packages = find_packages(),

    # Dependencies on other packages:
    setup_requires   = ['nose>=1.1.2'],
    tests_require    = test_requirements,
    install_requires = ['pymysql_utils>=0.51',
			'configparser>=3.3.0r2', 
			'argparse>=1.2.1', 
			] + test_requirements,

    # Unit tests; they are initiated via 'python setup.py test'
    #test_suite       = 'video_footprints/test',
    test_suite       = 'nose.collector', 

    #data_files = [('pymysql_utils/data', datafiles)],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
     #   '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
     #   'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Finds number of views for each minute of each video in an OpenEdX course.",
    license = "BSD",
    keywords = "json, relation, OpenEdX",
    url = "https://github.com/paepcke/video_footprints",   # project home page, if any
)
