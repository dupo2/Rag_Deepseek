
# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the Deepseek model:

```bash
ollama pull deepseek-r1:8b
```

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

# Run
Run the Streamlit app:

```bash
streamlit run pdf_rag.py
```

# Model change 
1. Using Ollama pull LLM that you want to use.
2. Change model's name in pdf_rag.py file. (model=**"Model name"**)
```bash
embeddings = OllamaEmbeddings(model="deepseek-r1:8b")

model = OllamaLLM(model="deepseek-r1:8b")
```
3. Run program.