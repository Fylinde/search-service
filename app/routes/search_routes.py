# app/routes/search_routes.py

from fastapi import APIRouter, HTTPException, Query, Depends
from app.services.search_service import add_document, search_query, suggest_autocomplete, perform_search, suggest_category
from elasticsearch import Elasticsearch, NotFoundError
from typing import Optional, List
from app.services.semantic_search import semantic_search
from app.services.recommendation_service import get_user_recommendations
from sqlalchemy.orm import Session
from app.database import get_db

es = Elasticsearch()
router = APIRouter()

@router.post("/index")
async def index_data(data: dict):
    """
    Index new data into Elasticsearch.
    """
    try:
        result = add_document(data)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def search(q: str):
    """
    Search the Elasticsearch index.
    """
    try:
        result = search_query(q)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_items(q: str):
    try:
        result = es.search(index="categories", body={"query": {"match": {"name": q}}})
        return result['hits']['hits']
    except NotFoundError:
        raise HTTPException(status_code=404, detail="No results found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/", response_model=List[dict])
def search_categories(q: str = Query(...)):
    try:
        # Perform the actual search logic
        search_results = perform_search(q)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error searching categories")
    

@router.get("/suggest", response_model=List[str])
def suggest_categories(term: str):
    """
    Suggest categories based on the term.
    """
    suggestions = suggest_category(term)  # Define the logic for generating suggestions
    return suggestions
    
    
   
@router.get("/semantic_search")
def perform_semantic_search(q: str = Query(...)):
    """
    Perform a semantic search using BERT-based NLP.
    :param q: The search query.
    :return: Ranked results based on semantic similarity.
    """
    results = semantic_search(q)
    return {"query": q, "results": results}

@router.get("/search")
def search_elasticsearch(q: str = Query(...)):
    """
    Perform a search using Elasticsearch.
    :param q: The search query.
    :return: Elasticsearch search results.
    """
    results = perform_search(q)  # This calls the Elasticsearch-based search
    return {"query": q, "results": results} 

@router.get("/search")
async def search_query(q: str, db: Session = Depends(get_db)):
    """
    Perform a basic search query using the `perform_search` function.

    Args:
        q (str): The search query

    Returns:
        List of search results
    """
    search_results = perform_search(q)
    if not search_results:
        raise HTTPException(status_code=404, detail="No results found")
    return search_results


@router.get("/recommendations")
async def get_recommendations(user_id: int):
    """
    Get personalized recommendations for a user.

    Args:
        user_id (int): ID of the user

    Returns:
        List of recommended products
    """
    recommendations = get_user_recommendations(user_id)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return recommendations