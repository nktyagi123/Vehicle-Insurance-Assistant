from rouge_score import rouge_scorer
import json

# Define a simple template function for expected queries
def generate_template_query(natural_language_query):
    # Create a simple template based on the query intent
    if "price" in natural_language_query and "under" in natural_language_query:
        price = int(natural_language_query.split("under $")[1])
        return json.dumps({"query": {"range": {"price": {"lte": price}}}})
    elif "recent articles" in natural_language_query:
        return json.dumps({"query": {"match": {"date": "recent"}}})
    # Add more templates as necessary
    return json.dumps({"query": {"match_all": {}}})

# Mock function for generating Elasticsearch query
def generate_elasticsearch_query(natural_language_query):
    # Placeholder for Gemini Pro model or similar generative model call
    # Assume the model generated query as an example
    return json.dumps({"query": {"range": {"price": {"lte": 50}}}})

# Evaluate with ROUGE-L against dynamically generated template
def evaluate_live_query(natural_language_query):
    expected_query = generate_template_query(natural_language_query)
    generated_query = generate_elasticsearch_query(natural_language_query)
    
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(expected_query, generated_query)
    
    print(f"Input Query: {natural_language_query}")
    print(f"Expected Template Query: {expected_query}")
    print(f"Generated Query: {generated_query}")
    print(f"ROUGE-L Precision: {scores['rougeL'].precision:.2f}")
    print(f"ROUGE-L Recall: {scores['rougeL'].recall:.2f}")
    print(f"ROUGE-L F1 Score: {scores['rougeL'].fmeasure:.2f}")

    # Set a threshold for passing ROUGE score (e.g., 0.7 F1 score)
    if scores['rougeL'].fmeasure >= 0.7:
        print("Generated query meets quality threshold.")
    else:
        print("Generated query does not meet quality threshold. Consider revising.")

# Test the function with a live input
evaluate_live_query("Find products price under $50")
