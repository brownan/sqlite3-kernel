from setuptools import setup, find_packages

setup(
    name="sqlite3_kernel",
    version = "1.0",
    packages=find_packages(),
    description="SQLite3 Jupyter Kernel",
    url = "https://github.com/brownan/sqlite3_kernel",
    classifiers = [
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: SQL',
    ]
)