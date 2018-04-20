# OpenHlTest
[![Validated](https://travis-ci.org/OpenHLTest/data-models.svg?branch=master)](https://travis-ci.org/OpenHLTest/data-models)
[![Package](https://img.shields.io/pypi/v/openhltest.svg)](https://pypi.org/project/openhltest)
[![Version](https://img.shields.io/pypi/pyversions/openhltest.svg)](https://pypi.org/project/openhltest)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)

OpenHlTest is a collaborative effort by test vendors to develop programmatic interfaces and tools for agnosticly managing test equipment.  

OpenHlTest's initial focus is the following:
- a consistent set of vendor-neutral data models (written in YANG)
- continuous integration yielding a single set of client tools
- test vendor server implementations of the data models

## Contributing to OpenHlTest
This repository is primarily for publishing the models, documents, and other material developed by the OpenHlTest working group. We generally do not accept pull requests in this repository.

Feedback and suggestions to improve OpenHlTest models is welcomed on the public mailing list, or by opening a GitHub issue

# Continuous Integration
On every commit to the repository folder travis continuous integration will start and do the following:
- identify model changes, if none the build will stop
- use pyang to validate the models.
- use pyang to generate and update the views folder with a model text view and html view
- use pyang to generate the python client files under the python_client/openhltest folder
- run python client unit tests
- generate pydoc html and markdown documentation
- include documentation and model views in the openhltest folder
- package and upload the openhltest folder as the [openhltest python package](https://pypi.org/project/openhltest/) to pypi.python.org

## OK continuous integration is great but what does it mean to me?
Anytime the model is updated you can install the latest version of the OpenHlTest python client simply by doing the following:  
- **pip install openhltest --upgrade --no-cache-dir**
