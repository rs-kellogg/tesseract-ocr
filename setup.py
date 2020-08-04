from setuptools import setup, find_packages

setup(
    name="tesseract-ocr",
    version="0.1.1",
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    maintainer="Will Thompson",
    maintainer_email="wkt@northwestern.edu",
    description="Code for OCR'ing text from PDF files",
    url="https://github.com/rs-kellogg/tesseract-ocr",
    packages=find_packages(include=["kelloggrs", "kelloggrs.*"]),
    include_package_data=False,
    install_requires=[
        "pandas",
        "pyyaml",
        "Pillow",
        "PyMuPDF",
        "sqlalchemy",
        "dask",
        "joblib",
        "pytesseract",
    ],
    extras_require={
        "interactive": [
            "jupyterlab",
            "jupyter_nbextensions_configurator",
            "ipyparallel",
        ]
    },
    entry_points={"console_scripts": [
        "extract_pages=kelloggrs.extract:main",
        "process_pages=kelloggrs.process:main",
    ]},
    setup_requires=["black", "flake8"],
    tests_require=[
        "pytest",
        "pytest-console-scripts",
        "pytest_tornasync",
        "pytest-runner",
    ],
)
