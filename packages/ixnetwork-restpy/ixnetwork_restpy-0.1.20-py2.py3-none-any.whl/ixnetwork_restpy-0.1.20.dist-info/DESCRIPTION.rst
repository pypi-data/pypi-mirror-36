# IxNetwork REST API Client
**This is an alpha build and is subject to change!**

## Features
- classes are generated from the latest released version of IxNetwork
  - the only class that can be directly be instantiated is the TestPlatform class
  - all other classes are accessed via a child property on the parent class
  - classes have helper methods depending on the type of class
	- required classes are automatically populated with one and only instance
	- user list classes have `add, remove, find` helper methods
  - every instantiated class encapsulates instances retrieved from the server 
  - encapsulated instances can be accessed using iterators or indexes
  - class iterator/index support includes: `__iter__ __next__ __getitem__ __len__`
- installs via pip  
  - pip install -U ixnetwork-restpy
- documentation that is part of the REST API browser is inlined in all generated classes  
  - inlined documentation is also available via a static documentation browser distributed with the package  
  - no need to connect to a running instance of IxNetwork to get API documentation
- samples distributed with the package

## Limitations
- minimum IxNetwork support is 8.42



