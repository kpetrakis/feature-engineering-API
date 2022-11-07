# Feature Engineering API
The goal of this project was to create an API (with fastAPI framework) for a feature engineering process. The are 2 main endpoints for the API. The first one returns the results of the 'feature engineering' process in a JSON forma. The second just checks if the API is up and running. 

## ENDPOINTS
*```[GET] /api/api_status```: Returns {"status":"UP"} if the API is up and running.

* ```[GET] /api/features/customers```: Part of the second of the 2 basic endpoints asked by the project requirements. It returns all the features generated for the customers dataframe, after applying the feature engineering process. The customers dataframe contains the annual income for each customer.

* ```[GET] /api/features/loans```: The other part of the second of the 2 main endpoints. It returns all the features generated for the loans dataframe, after applying the feature engineering process. Loans dataframe corresponds to the dataframe produced by the json file provided.

* ```[GET] /api/customers/{customer_id}```: It return the entry in the customers dataframe (customer_ID, annual_income) corresponding to the given customer id. 

* ```[GET] /api/loans/{customer_id}```: It returns the entry in the loans dataframe which corresponds to the given customer_id.

* ```[GET] /api/features/customers/{customer_id}```: It return the entry in the generated features dataframe for the customers with the given customer_id.

* ```[GET] /api/features/loans/{customer_id}```: It returns the entry in the generated features dataframe for the loans which corresponds to the given customed_id.

#### Endpoints summary
All the implemented endpoints are available at http://localhost:8000/docs/


## USAGE
#### Setup Python virtual enviroment
1. sudo apt install python3-pip
2. run the installer
3. python -m venv optasia_api_venv
4. source optasia_api_venv/bin/activate

#### Export PYTHONPATH
export PYTHONPATH = ${PYTHONPATH}:/path/to/your/project/dir

#### Deploy with docker-compose
Execute ```docker-compose up -d --build``` 

After the app starts navigate to http://localhost:8000 in your browser.


#### Stop and remove container
```docker-compose down```

