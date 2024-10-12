# app/services/recommendation_service.py

from typing import List
import random
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Mock data for demonstration, replace this with your actual data from DB
USER_HISTORY = {
    1: ["smartphone", "laptop", "camera"],
    2: ["shoes", "clothes", "watch"],
    3: ["headphones", "tablet", "smartphone"],
}

PRODUCTS = {
    1: "Smartphone",
    2: "Laptop",
    3: "Camera",
    4: "Shoes",
    5: "Clothes",
    6: "Watch",
    7: "Headphones",
    8: "Tablet",
}


def get_user_recommendations(user_id: int) -> List[str]:
    """
    This function provides basic personalized recommendations.
    Replace this with a more sophisticated model if needed.

    Args:
        user_id (int): ID of the user

    Returns:
        List[str]: List of recommended products
    """
    if user_id not in USER_HISTORY:
        return ["No history found for this user."]

    user_history = USER_HISTORY[user_id]
    recommended_products = recommend_based_on_history(user_history)

    return recommended_products


def recommend_based_on_history(history: List[str]) -> List[str]:
    """
    A simple recommendation system based on a user's search history.

    Args:
        history (List[str]): A list of the user's past search queries

    Returns:
        List[str]: List of recommended products
    """
    # Example: simple random selection of other products for now
    # Later, we can apply more advanced algorithms such as collaborative filtering
    recommendations = random.sample(list(PRODUCTS.values()), 3)
    return recommendations

