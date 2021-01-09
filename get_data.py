import requests
from query import block
from secret import token
from termcolor import colored


startCursor = ""
endCursor = ""
headers = {"Authorization": token}
hasNextPage = "True"
colors =["red","green","yellow","blue","magenta","cyan","white","red","green","yellow","blue","magenta","cyan","white"]

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
    nodes = result["data"]["search"]["edges"][0]["node"]["repositories"]["nodes"]
    user = result["data"]["search"]["edges"][0]["node"]["name"]
    color_counter=0
    for node in nodes:
        color_counter+=1
        repos = node["languages"]["nodes"]
        for repo in repos:
            print (user,(colored(node["id"], colors[color_counter])),repo["name"])

    print ("Cursors",startCursor, endCursor, "Has next page:", hasNextPage)  
    while hasNextPage == 'True':
        result = run_query(endCursor) 
        endCursor = result["data"]["search"]["pageInfo"]["endCursor"]
        startCursor = result["data"]["search"]["pageInfo"]["startCursor"]
        hasNextPage =  str(result["data"]["search"]["pageInfo"]["hasNextPage"])
        nodes = result["data"]["search"]["edges"][0]["node"]["repositories"]["nodes"]
        user = result["data"]["search"]["edges"][0]["node"]["name"]
        color_counter=0
        for node in nodes:
            color_counter+=1
            repos = node["languages"]["nodes"]
            for repo in repos:
                print (user,(colored(node["id"], colors[color_counter])),repo["name"])
        if hasNextPage == 'True':
            print ("---------------------------------------------------------------------------------")
            print("Cursors",startCursor, endCursor, "Has next page:", (colored(hasNextPage, colors[1])))
            print ("---------------------------------------------------------------------------------")

        else:
            print ("---------------------------------------------------------------------------------")
            print("Cursors",startCursor, endCursor, "Has next page:", (colored(hasNextPage, colors[0])))
            print ("---------------------------------------------------------------------------------")


parse_query()
