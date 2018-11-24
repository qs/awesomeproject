import requests


def query_api(query, filters={}):
    res = requests.post("https://kesko.azure-api.net/v1/search/products",
                        data={
                            "query": query,
                            "filters": filters
                        },
                        headers={"Ocp-Apim-Subscription-Key": "42c4facc08ce47e598e6c566fb253258"}).json()
    return res
