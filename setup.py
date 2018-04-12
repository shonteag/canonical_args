from setuptools import setup, find_packages



setup(name="canonical_args",
	  version="0.1",
	  author="Shonte Amato-Grill",
	  author_email="shonte.amatogrill@gmail.com",
	  maintainer="Shonte Amato-Grill",
	  maintainer_email="shonte.amatogrill@gmail.com",
	  packages=find_packages(exclude=["test", "tests"]),
	  classifiers=[
	      "Programming Language :: Python :: 2.7"
	  ]
)
