# WorkSpace
WorkSpace 2026

Dans le terminal, tapper ceci :

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```



Pour lancer Python en local :

```
source .venv/bin/activate
uvicorn app.main:app --reload
```