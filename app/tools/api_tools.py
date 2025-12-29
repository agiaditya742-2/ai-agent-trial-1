
import json

# --- Simulated Internet Search Tool ---
def search_internet(query: str):
    """
    Simulates a search engine query.
    Returns a predefined result based on the query for demonstration purposes.
    """
    print(f"TOOL: Simulating internet search for: {query}")

    # Predefined responses for demonstration
    results = {
        "what is the capital of france?": "The capital of France is Paris.",
        "how to bake a cake?": "To bake a cake, you typically need flour, sugar, eggs, and butter. Mix them together and bake in an oven.",
        "latest AI news": "A new breakthrough in large language models was announced, achieving near-human performance in reasoning tasks."
    }

    # Return a specific result if the query matches, otherwise a generic one
    response = results.get(query.lower(), f"No specific information found for '{query}'. Try a more general search.")

    return json.dumps({"result": response})

# --- (You can add other API-based tools here) ---
