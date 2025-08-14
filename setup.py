import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        # Run standard install first
        install.run(self)

        # Create notes directory if it doesn't exist
        notes_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "note_taker")
        os.makedirs(notes_dir, exist_ok=True)
        print(f"[note-taker] Notes directory ready at: {notes_dir}")

        # Check if ~/.local/bin is in PATH
        local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
        user_path = os.environ.get("PATH", "")

        if local_bin not in user_path.split(os.pathsep):
            print(f"[note-taker] WARNING: {local_bin} is not in your PATH.")
            print("           Add it to your shell configuration to run 'note-taker' from anywhere:")
            print(f"           echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.bashrc && source ~/.bashrc")
        else:
            print(f"[note-taker] Found {local_bin} in your PATH ✅")


setup(
    name='note_taker',
    version='0.3.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'note-taker=note_taker.main:main',
        ],
    },
    include_package_data=True,
    description="A simple Neovim-based note-taking CLI",
    author="Lars Reime",
    author_email="clandestino161@pm.me",
    url="https://github.com/clandestino161/note_taker",
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
