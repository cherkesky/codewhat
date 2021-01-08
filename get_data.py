import requests
from query import block
from secret import token

startCursor = ""
endCursor = ""
headers = {"Authorization": token}
hasNextPage = "True"

def run_query(endCursor=""): 
    if endCursor == "":
        searchQuery = 'search(, first: 1, query: "location:Nashville", type: USER)'
    else:
        searchQuery = f'search(first: 1, after: "{endCursor}", query: "location:Nashville", type: USER)'
    
    query = f"""
    {{
    {searchQuery}
    {block}
    }}
    """

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



def parse_query():
    result = run_query() 
    endCursor = result["data"]["search"]["pageInfo"]["endCursor"]
    startCursor = result["data"]["search"]["pageInfo"]["startCursor"]
    hasNextPage =  str(result["data"]["search"]["pageInfo"]["hasNextPage"])
    print (result)
    print ("Cursors",startCursor, endCursor, "Has next page:", hasNextPage)  
    while hasNextPage == 'True':
        result = run_query(endCursor) 
        endCursor = result["data"]["search"]["pageInfo"]["endCursor"]
        startCursor = result["data"]["search"]["pageInfo"]["startCursor"]
        hasNextPage =  str(result["data"]["search"]["pageInfo"]["hasNextPage"])
        print (result)
        print ("Cursors",startCursor, endCursor, "Has next page:", hasNextPage)  

parse_query()
