import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swimlane_records_updater",
    version="13",
    author="Jeremy m Crews",
    author_email="jeremy.m.crews@gmail.com",
    description="Common Record Updater for Swimlane apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremymcrews/swimlane_record_updater",
    packages=setuptools.find_packages(),
    install_requres=[
        'swimlane',
        'ConfigParser'
    ],
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)