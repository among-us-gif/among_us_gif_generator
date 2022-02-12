from setuptools import find_packages
from setuptools import setup

setup(
    name='among-us-gif-generator',
    version='0.0.1',
    description='Among Us Crewmate and GIF Generator',
    author='David Dellsperger',
    author_email='david.dellsperger@gmail.com',
    long_description='Among Us Crewmate and GIF Generator which has a plethora of cli options to generate gifs and or images for different purposes with among us data',
    url='https://github.com/among-us-gif/among_us_gif_generator',
    packages=find_packages(exclude=('tests*', 'testing*')),
    entry_points={
        'console_scripts': [
            'amongusgif = gifgen.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    package_dir={'gifgen': 'gifgen'},
    package_data={'gifgen': ['assets/*.png', 'assets/*.ttf']},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        'Pillow>=7.0.0',
        'numpy',
    ],
)
