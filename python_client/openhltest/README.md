# OpenHlTest Python Client
The openhltest folder is the repository for the OpenHlTest python client module.

## Auto generated python client
The auto generated library will follow these guidelines:
1) It will be auto-generated every time there is a model change that has been successfully validated.
2) It will be hierarchical and match the hierarchy of the yang model.
3) It will consist of base infrastructure that encapsulates transport, serialization and errors.
4) Once the library has been generated and unit tests pass it will be packaged and posted on pypi.python.org.  
5) The library will be available for install using the command:
```
pip install openhltest
```

## Base infrastructure that is not auto-generated
1) Https transport class encapsulated in HttpTransport
2) Crudx and utility methods encapsulated in YangBase  
   - dump method
   - convert python dict objects to openhltest input/output objects
   - convert openhltest input/output objects to python dict objects 

## The pyang plugin python_client_plugin.py will auto generate the following
1) classes for the following yang keywords:  
   - container
   - list
   - input
   - output
2) class @property accessors for the following yang keywords: 
   - leaf
   - leaf-list
3) class methods for the following yang keywords:  
   - action
   - rpc
4) class @property accessors to access child container, list classes
5) class create_... methods to create child list siblings (only rw list keyword)  
   - rw list will have the yang key as a required parameter
   - all other leaf, leaf-list keywords will be defaulted to None if keyword default is not present
6) class update method to allow for updating dirty properties
7) class delete method to allow for deletion (only rw list keyword)
8) class dump method

### Documentation
1) Documentation is auto generated and located in the openhltest/docs folder. It will include the following:  
   - yang model views
   - docstrings from yang models
   - pydoc html generated from docstrings
   - markdown generated from docstrings

### Sample code
Sample code is located in the openhltest/samples folder.
