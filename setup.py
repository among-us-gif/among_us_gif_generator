import setuptools

def get_version():
    version_file = "src/gifgen/_version.py"
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]

setuptools.setup(
    name='AmongUsGenerator',
    version='0.0.1',
    author='David Dellsperger', 
    author_email='david.dellsperger@gmail.com',
    description='Among Us Crewmate and GIF Generator', 
    url='https://github.com/among-us-gif/among_us_gif_generator',
    packages=['gifgen'],
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
    install_requires=['Pillow>=7.0.0', 'numpy'])