from setuptools import setup

setup(
    name='simulator',
    version='0.1.0',
    description='A group project particle detector.',
    url='https://github.com/Richard-Sti/Particle-Detector',
    author='Richard Stiskalek',
    author_email='richard.stiskalek@protonmail.com',
    license='None',
    packages=['simulator'],
    install_requires=['scipy',
                      'numpy',
                     ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
