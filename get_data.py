import requests
from query import query
from secret import token

headers = {"Authorization": token}

def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
           
result = run_query(query) 
print (result)
