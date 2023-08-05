from setuptools import setup, find_packages
from gitmit import VERSION

setup(
      name = "gitmit"
    , version = VERSION
    , packages = ['gitmit'] + ['gitmit.%s' % pkg for pkg in find_packages('gitmit')]
    , include_package_data = True

    , install_requires =
      [ "dulwich==0.19.6"
      ]

    , extras_require =
      { "tests":
        [ "noseOfYeti>=1.5.0"
        , "nose"
        , "mock==1.0.1"
        , "tox"
        ]
      }

    , entry_points =
      { 'console_scripts' :
        [ 'gitmit = gitmit.executor:main'
        ]
      }

    # metadata for upload to PyPI
    , url = "https://github.com/delfick/gitmit"
    , author = "Stephen Moore"
    , author_email = "delfick755@gmail.com"
    , description = "Python library to discover commit times of all files under a git repository"
    , long_description = open("README.rst").read()
    , license = "MIT"
    , keywords = "git,commit,mtime"
    )

