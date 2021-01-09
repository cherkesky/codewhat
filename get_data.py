import requests
from query import block
from secret import token
from termcolor import colored

startCursor = ""
endCursor = ""
headers = {"Authorization": token}
hasNextPage = "True"
colors =["red","green","yellow","blue","magenta","cyan","white"]
lang_counter_dict={}

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
    repo_counter=0
    location = result["data"]["search"]["edges"][0]["node"]["location"]
    for node in nodes:
        if color_counter == 6:
            color_counter = 0
        else: 
            color_counter+=1
        repos = node["languages"]["nodes"]
        repo_counter+=1
        for repo in repos:
            print (user,(colored(node["id"], colors[color_counter])),repo["name"])
            if repo["name"] in lang_counter_dict:
                lang_counter_dict[f'{repo["name"]}']+=1
            else:
                lang_counter_dict[f'{repo["name"]}'] = 1
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
            if color_counter == 6:
                    color_counter = 0
            else: 
                color_counter+=1   
            repos = node["languages"]["nodes"]
            repo_counter+=1
            for repo in repos:
                print (user,(colored(node["id"], colors[color_counter])),repo["name"], )
                if repo["name"] in lang_counter_dict:
                    lang_counter_dict[f'{repo["name"]}']+=1
                else:
                   lang_counter_dict[f'{repo["name"]}'] = 1
        if hasNextPage == 'True':
            print ("---------------------------------------------------------------------------------")
            print ("Cursor:", endCursor, "Has next page:", (colored(hasNextPage, colors[1])))
            print ("Location:", location)
            print ("Counters:", "Repos:", repo_counter)
            print ("---------------------------------------------------------------------------------")
        else:
            sorted_lang_counter_dict = sorted(lang_counter_dict.items(), key=lambda x: x[1],reverse=True)
            print ("---------------------------------------------------------------------------------")
            print ("Cursor:", endCursor, "Has next page:", (colored(hasNextPage, colors[0])))
            print ("Location:", location)
            print ("Counters:", "Repos:", repo_counter)
            print ("---------------------------------------------------------------------------------")
            print ((colored("Languages Counted:", colors[6])), sorted_lang_counter_dict )


parse_query()
