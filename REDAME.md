1) Create conda environment
   conda create -n venv python=3.10 -y

2) Activate environment 
   conda activate venv

3) Install Dependencies:
    pip install -r requirememts.txt

4) Set hugging face hub :
   conda env config vars set HF_TOKEN= Enter your hugging face token

5) Deactivate or restart terminal:
   conda deactivate
   conda activate rag

6) Run app.py:
   python app.py

7) Follow the link annd use web interface to process question and answer