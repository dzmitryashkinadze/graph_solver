from setuptools import setup

setup(
	name="physai",
	version="0.0.1",
	description="A Python library for solving exercises on various topics in Physics",
	packages=["physai"],
    package_data={'physai': ['./models/*.graphml']},
    include_package_data=True,
	install_requires=[
		"numpy",
		"sympy",
		"pint",
		"networkx",
	],
)
