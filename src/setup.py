from setuptools import setup, find_packages

setup(name='draiving',
    version='0.01',
    description='A library for small scale DIY self driving cars',
    url='-',
    author='Yannis Chatzikonstantinou',
    author_email='yconst@gmail.com',
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 2.7'
    ],
    keywords='selfdriving cars drive',

    install_requires=['numpy', 
                      'pillow',
                      'docopt',
                      'tornado',
                      'requests',
                      'envoy',
                      'picamera',
                      'pandas'
                     ],

    packages=find_packages(exclude=(['tests', 'docs', 'env'])),
)