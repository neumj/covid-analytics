from setuptools import setup, find_packages

reqs = [
    "bokeh",
    "numpy",
    "pandas",
]

conda_reqs = [
    "bokeh",
    "numpy",
    "pandas"
]

test_pkgs = []

setup(
    name="covidanalytics",
    python_requires='>3.4',
    description="Python package for exploring COVID data.",
    url="https://github.com/neumj/covid-analytics",
    install_requires=reqs,
    conda_install_requires=conda_reqs,
    test_requires=test_pkgs,
    packages=find_packages(),
    include_package_data=True
)

