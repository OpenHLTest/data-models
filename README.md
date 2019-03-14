# OpenHLTest
[![Validated](https://travis-ci.org/OpenHLTest/data-models.svg?branch=master)](https://travis-ci.org/OpenHLTest/data-models)
[![Package](https://img.shields.io/pypi/v/openhltest.svg)](https://pypi.org/project/openhltest)
[![Version](https://img.shields.io/pypi/pyversions/openhltest.svg)](https://pypi.org/project/openhltest)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)

OpenHLTest is a collaborative effort by test vendors to develop agnostic programmatic interfaces and tools for managing test equipment.  

OpenHLTest's focus is the following:
- a consistent set of YANG vendor-neutral data models 
- continuous integration yielding a single set of client artifacts
- test vendor server implementations of the data models

## Artifacts
On every commit to the repository a [Travis job](https://travis-ci.org/OpenHLTest/data-models) will do the following:
- validate the models
- generate the python package and the documentation browser artifacts
- upload the [python package](https://pypi.org/project/openhltest/) and the [documentation browser](https://openhltest.github.io/docs/index.html)

## Contributing
This repository is primarily for publishing the models, documents, and other material developed by the OpenHLTest working group. We generally do not accept pull requests in this repository.

Feedback and suggestions to improve OpenHLTest models is welcomed by opening a [GitHub issue](https://github.com/OpenHLTest/data-models/issues).
