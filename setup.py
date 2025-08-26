import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation tasks."""
    def run(self):
        install.run(self)
        notes_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "note_taker")
        os.makedirs(notes_dir, exist_ok=True)
        print(f"[notes] Notes directory ready at: {notes_dir}")


setup(
    name='note_taker',
    version='0.4',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'rich',
        'markdown2',
        'weasyprint',
    ],
    entry_points={
        'console_scripts': [
            'notes=note_taker.main:main',
        ],
    },
    include_package_data=True,
    description="A simple Neovim-based note-taking CLI",
    author="Lars Reime",
    author_email="clandestino161@pm.me",
    url="https://github.com/clandestino161/notes.git",
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
