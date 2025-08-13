# requirements.txt1
# Tea API · Flask Mini Project

A simple educational REST API for working with teas: list, search, get one, create, update, and delete.  
Built to practice Flask and HTTP methods (**CRUD**).

---

## 🚀 Quick Start

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
Server will run at: http://127.0.0.1:5000

By default, a simple Bearer token check is enabled for mutating requests (POST/PUT/PATCH/DELETE).
Token: Authorization: Bearer secret123
Enable/disable in code via ENABLE_AUTH.
 Architecture (simplified)
Data is stored in-memory in the tea_dict dictionary (name -> description).

All responses include the header X-API-Version: 2.

Public endpoints: GET /tea and GET /tea/<name>.
All other methods require a token (if ENABLE_AUTH=True).
