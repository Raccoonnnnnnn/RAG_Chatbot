# LightRAG Setup & Run Guide with Ollama

This guide will help you set up, configure, and run the LightRAG system with Ollama to crawl book data from Tiki, process it, and deploy a chatbot based on that data.

## Table of Contents
1. [Clone LightRAG Repository](#1-clone-lightrag-repository)
2. [Set Up Python Environment](#2-set-up-python-environment)
3. [Install & Configure Ollama](#3-install--configure-ollama)
4. [Configure Environment Variables](#4-configure-environment-variables)
5. [Prepare Data](#5-prepare-data)
6. [Run Ollama Model](#6-run-ollama-model)
7. [Run the Application](#7-run-the-application)
8. [Automate with Crontab](#8-automate-with-crontab)
9. [Push Code to GitHub](#9-push-code-to-github)
10. [Useful Commands](#10-useful-commands)

---

## 1. Clone LightRAG Repository
Clone the repository from GitHub:
```bash
git clone https://github.com/stavidphan/LightRAG.git
cd LightRAG/
```

---

## 2. Set Up Python Environment
Create a Conda environment:
```bash
conda create -n lightrag python=3.11 -y
conda activate lightrag
```
Install required packages:
```bash
pip install -e .
```

---

## 3. Install & Configure Ollama

### 3.1. Install Ollama
Download and install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3.2. Pull Required Models
Download the embedding and LLM models:
```bash
ollama pull nomic-embed-text
ollama pull gemma2:9b
```

---

## 4. Configure Environment Variables
Create a `.env` file in the root directory (LightRAG/) with the following content:
```
# Environment variables for automate_update_data.py
CRAWL_DIR=data/crawl_tiki_data
COMPARE_DIR=data/compare_data
DAYS_TO_KEEP=7
INSERT_BATCH_API=http://localhost:8000/insert_batch
QUERY_API=http://localhost:8000/query
LOG_FILE=logs/update_data.log
LOG_FILE_MODE=w

# Environment variables for get_books.py
BOOKS_CRAWL_LIMIT=3000
# Number of categories to get books from
NUM_CATEGORIES=40

# Environment variables for lightrag_ollama_demo_api.py
DEFAULT_QUERY_MODE=local
TOP_K=5
LLM_MODEL_NAME=gemma2:9b
EMBED_MODEL=nomic-embed-text
# The document list is divided into batches running in parallel, each batch up to INSERT_BATCH_SIZE, documents in each batch are processed sequentially
INSERT_BATCH_SIZE=50
```

---

## 5. Prepare Data
Create directories for storing data:
```bash
mkdir -p data/crawl data/compare logs
```
Check the `categories.json` file:
Ensure the file `src/crawl_tiki_data/categories.json` exists and contains the list of book categories from Tiki. If not, run the category crawl script (if available) or download it manually.

---

## 6. Run Ollama Model
Run Ollama in the terminal:
```bash
ollama serve
```
Keep this terminal running to ensure the API is active.

---

## 7. Run the Application

### 7.1. Start the LightRAG API
Open a new terminal and start the API:
```bash
cd LightRAG
python src/lightrag_ollama_api.py
```
The API will start at `http://localhost:8000`.

### 7.2. Crawl and Update Data
Run the script to crawl and update data:
```bash
python src/automate_update_data.py
```
This script will:
- Crawl book data from Tiki.
- Compare it with old data.
- Insert new data into LightRAG via the API.

### 7.3. Check Logs
Check the logs at `logs/update_data.log` to monitor progress:
```bash
cat logs/update_data.log
```

### 7.4. Query the Chatbot
Use curl or a tool like Postman to send a query:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Find books about programming", "mode": "local", "top_k": 5}'
```

---

## 8. Automate with Crontab
Automate the data update script to run daily (e.g., at 18:51).

Edit the crontab:
```bash
crontab -e
```
Add the following line:
```bash
51 18 * * * cd /Users/duypt/Documents/Coding/LightRAG && /opt/homebrew/Caskroom/miniconda/base/bin/python3 ./src/automate_update_data.py >> ./logs/cron_log.txt 2>&1
```
Explanation: This runs at 18:51, navigates to the project directory, uses Python from Miniconda, and logs output to `logs/cron_log.txt`.

Check the crontab:
```bash
crontab -l
```
Remove a cron job (if needed):
```bash
crontab -e  # Delete the corresponding line
```

---

## 9. Push Code to GitHub

### 9.1. Initialize Git (if needed)
Remove old Git settings (if any):
```bash
git remote remove origin
rm -rf .git
git init
```

### 9.2. Configure User Information
```bash
git config --global user.email "thanhduyphan2123@gmail.com"
git config --global user.name "Stavid Phan"
```

### 9.3. Add and Commit Code
```bash
git add .
git commit -m "Initial commit with updated LightRAG structure"
```

### 9.4. Add Remote and Push
```bash
git remote add origin https://github.com/stavidphan/LightRAG.git
git branch -M main
git push -u origin main
```

---

## 10. Useful Commands

### System Monitoring
- Check disk space:
```bash
df -h
```
- Check RAM:
```bash
free -h
```
- Check CPU:
```bash
htop
```
- Check GPU (if NVIDIA):
```bash
watch -n 1 nvidia-smi
```
- Check system logs when a process is killed:
```bash
sudo dmesg | grep -i "killed"
```

### Create Swap (If Low on RAM)
Create a 24GB swap file:
```bash
sudo fallocate -l 24G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
free -h  # Verify swap
```

---

## Project Directory Structure
```
LightRAG/
├── .env                      # Environment variable configuration file
├── src/                      # Source code
│   ├── automate_update_data.py  # Script for automated crawling and updating
│   ├── lightrag_ollama_api.py   # LightRAG API
│   ├── crawl_tiki_data/         # Crawling module
│   │   ├── get_books.py
│   │   ├── get_categories.py
│   │   └── categories.json
│   ├── compare_data/            # Comparison module
│   │   └── compare_data.py
│   └── preprocess_data/         # Data processing module
│       └── process_tiki_books.py
├── data/                     # Output data
│   ├── crawl_tiki_data/                # Crawled files
│   │   ├── books_data_*.csv
│   └── compare_data/              # Comparison files
│       └── changes_*.csv
├── logs/                     # Log files
│   ├── api_logs.log
│   └── update_data.log
└── README.md                 # This guide
```

---

## Notes
- Ensure Ollama is running before starting the API or crawling scripts.
- If you encounter a "Redirected (302)" error while crawling, check the logs and adjust the delay in `get_books.py`.
- The log file (`logs/update_data.log`) will record details of the crawling, comparison, and data insertion processes.