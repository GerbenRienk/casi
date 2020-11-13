# casi
A.k.a. the Castor Synch Interface.  
Exploring the possibilities of using the castor api with python to retrieve data from it and store it in another database.

## preparations
In order to use the python-scripts we must complete the config file. This is config/casi.config. Note that on github only an example config-file exists, so we must create a fresh casi.config, for example by copying casi_example.config.
The url won't need any changing, but we must supply the client-id and the client-secret.
This is described at [https://data.castoredc.com/api](https://data.castoredc.com/api)
and at [https://helpdesk.castoredc.com/article/124-application-programming-interface-api](https://helpdesk.castoredc.com/article/124-application-programming-interface-api)

## requirements
- Install python 3.x
- Install with pip requests

The code was tested against castor 2020.2.20 
