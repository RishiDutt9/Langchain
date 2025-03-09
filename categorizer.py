import ollama
import os

# Path for input and output files
input_path = r"C:\Users\Rishi\OneDrive\Desktop\ML\Ollama\list.txt"
output_path = r"C:\Users\Rishi\OneDrive\Desktop\ML\Ollama\Categorizedlist.txt"

if not os.path.exists(input_path):
    print("File does not exist")
    exit(1)

# Read the Uncategorised list
with open(input_path, 'r') as f:
    items = f.read().strip()

prompt = f"""
You are an assistant in a store who categorizes items and sorts the grocery items. Here is the list of items: {items}
Please:
    1. Categorize the items into appropriate categories such as Produce, Meat, Dairy, Frozen, Bakery, Pantry, Household, Personal Care, Other.
    2. Sort the items in each category.
    3. Present the categorized list in a clear and organized manner using bullet points or numbers.
"""

# Send the prompt and get the response
try:
    response = ollama.generate(model="llama3.2", prompt=prompt)
    generated_text = response.get("response", "")
    print("===========Generated text:============\n")
    print(generated_text)

    # Write the output to the output file
    with open(output_path, 'w') as f:
        f.write(generated_text.strip())

    print("Output file generated successfully")
except Exception as e:
    print(f"Error: {e}")




