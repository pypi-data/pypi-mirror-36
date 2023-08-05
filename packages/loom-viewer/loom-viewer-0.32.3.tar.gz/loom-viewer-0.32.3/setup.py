from setuptools import setup, find_packages

# pylint: disable=exec-used
__version__ = '0.0.0'
exec(open('loom_viewer/_version.py').read())

setup(
    name="loom-viewer",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "loompy",
        "matplotlib",
        "scikit-learn",
        "h5py",
        "pandas",
        "scipy",
        "pillow",
        "numpy",
        "requests",
        "flask",
        "flask-compress",
        "gevent",
        "typing",
        "mypy_extensions"
    ],

    # loom command
    # scripts=["loom_viewer/loom"],
    entry_points={
        "console_scripts": [
            "loom = loom_viewer:main",
        ],
    },

    # static files from MANIFEST.in
    include_package_data=True,

    # metadata for upload to PyPI
    author="Linnarsson Lab",
    author_email="sten.linnarsson@ki.se",
    description="View .loom files in the browser",
    license="BSD",
    keywords="loom omics transcriptomics bioinformatics",
    url="https://github.com/linnarsson-lab/loom-viewer",
)
