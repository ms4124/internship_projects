from ollama_client import query_ollama

prompt = "What is artificial intelligence?"
response = query_ollama(prompt)
print("Response:\n", response)
