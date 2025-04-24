# Hybrid Chess Engine 
My 2019 NEA project: a hybrid chess engine using CNNs as policy and value functions. Trained on Stockfish evaluations from lichess anti-cheat system. Inspired by AlphaZero and Lc0. Three search algorithms implemented - custom **MCTS**, **minimax** and custom '**U-search**' algorithm. 

![image](https://github.com/user-attachments/assets/9ef4b5f8-e941-413b-a786-14552c5e4e01)

**Write-up**: [[Link to writeup]](https://docs.google.com/document/d/134AhJ5AeecNpjOaAat2bdeEU357iWRZi/edit?usp=sharing&ouid=103579644280044030856&rtpof=true&sd=true)

**Setup:**

1.  **Create virtual environment:** `uv venv`
2.  **Activate virtual environment:** `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
3.  **Install dependencies:** `uv sync`

**Run:**

```bash
python main.py
