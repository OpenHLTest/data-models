# OpenHlTest yang data-models
Repository for vendor agnostic yang data models.

Current Model Status

[![Validated](https://travis-ci.org/OpenHLTest/data-models.svg?branch=master)](https://travis-ci.org/OpenHLTest/data-models)


## Continuous Integration
On every commit to the models folder travis continuous integration will start and do the following:
1) use pyang to validate the models.
2) use pyang to generate and update the views folder with text view, javascript view, uml view.
3) use pyang to generate the python client files under the python_client folder
4) run python client unit tests
5) package and upload the python client to pypi.python.org under the openhltest package
