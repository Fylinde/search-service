# app/services/search_service.py

from elasticsearch import Elasticsearch, NotFoundError
from app.config import settings
from fastapi import HTTPException


# Initialize Elasticsearch client
es = Elasticsearch(hosts=["http://elasticsearch:9200"])

def perform_search(query: str):
    try:
        # Perform the search query on the "categories" index in Elasticsearch
        result = es.search(
            index="categories",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "description", "meta_keywords"]
                    }
                }
            }
        )
        return [hit["_source"] for hit in result['hits']['hits']]
    except NotFoundError:
        # Handle case where no results are found
        raise HTTPException(status_code=404, detail="No results found for the query.")
    except Exception as e:
        # Catch and log other potential errors
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

def add_document(data: dict):
    """
    Add a document to the Elasticsearch index.
    """
    res = es.index(index=settings.ELASTICSEARCH_INDEX, body=data)
    return res

def search_query(query: str):
    """
    Search for a document in the Elasticsearch index.
    """
    res = es.search(index=settings.ELASTICSEARCH_INDEX, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description"]
            }
        }
    })
    return res["hits"]["hits"]

def suggest_autocomplete(term: str):
    """
    Provide autocomplete suggestions.
    """
    res = es.search(index=settings.ELASTICSEARCH_INDEX, body={
        "suggest": {
            "product-suggest": {
                "prefix": term,
                "completion": {
                    "field": "name_suggest"
                }
            }
        }
    })
    return res["suggest"]["product-suggest"]

def suggest_category(term: str):
    """
    Suggest categories based on a partial search term.
    
    :param term: Partial search term (e.g., 'iph' for 'iPhone')
    :return: List of category suggestions
    """
    # Example of a basic suggest query in Elasticsearch
    body = {
        "suggest": {
            "category-suggest": {
                "prefix": term,
                "completion": {
                    "field": "name_suggest",
                    "fuzzy": {
                        "fuzziness": 2
                    }
                }
            }
        }
    }

    response = es.search(index="categories", body=body)
    suggestions = response["suggest"]["category-suggest"][0]["options"]

    # Extract just the suggested text
    return [suggestion["_source"]["name"] for suggestion in suggestions]