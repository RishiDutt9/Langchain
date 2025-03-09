import requests 
import json 


url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2",
    "prompt": "Tell me a short story and make it funny",
}

respose = requests.post(url, json=data, stream=True)

#Check the response status code

if respose.status_code == 200:
    print("Generated Text :",end="",flush=True)
    #Iterate over the response
    for line in respose.iter_lines():
        if line:
            #Decode the line and parse the json
            decode_line = line.decode('utf-8')
            results = json.loads(decode_line)
            #Get the text from the response
            generated_text = results.get("response","")
            print(generated_text, end="",flush=True)
else:
    print("Failed to get the response")