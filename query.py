query = """
{
search(query: "location:Nashville", type: USER, first: 100) {
    userCount
    edges {
      node {
        ... on User {
          name
          login
          location
          repositories(last: 10) {
            totalCount
            nodes {
              id
              languages(first: 5) {
                nodes {
                  name
                }
              }
            }
          }
        }
      }
    }
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
  }
}
"""
