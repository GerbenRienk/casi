# casi
A.k.a. the Castor API Scriptlet Inventory.  
Exploring the possibilities of using the castor api with python to retrieve data from it and store it in a file or in another database.  

The idea is to give some examples of what is possible, with much comments between the code, so that all can be changed easily to fit the needs and purposes of others.

The code was tested against castor 2020.2.20 

## preparations
In order to use the python-scripts we must complete the config file. This is config/casi.config. Note that on github only an example config-file exists, so we must create a fresh casi.config, for example by copying casi_example.config.
The url won't need any changing, but we must supply the **client-id** and the **client-secret**.
This is described at [https://data.castoredc.com/api](https://data.castoredc.com/api)
and at [https://helpdesk.castoredc.com/article/124-application-programming-interface-api](https://helpdesk.castoredc.com/article/124-application-programming-interface-api)

## requirements
- Install python 3.x
- Install with pip: requests

## where to start?
If you're just starting with python and the api, start simple. Go to the helpdesk article that explains the client-id and secret, and copy and paste these in your /src/config/casi.config  
To test if you did it correctly, run the scriptlet /src/extract/test_token.py and if you get an output like "the access-token is: etc." then you're good to go.  

Next step could be to list all your studies. (Or maybe that's just one study.) When you run /src/extract/list_studies.py you can see which studies are available to you.
