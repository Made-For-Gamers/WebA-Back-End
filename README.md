# WebA-Back-End

A Python FastAPI back-end for the MFG WebAggregator Nexus project.

Steps to run the project:

```bash
python -m venv myenv
```

```bash
Linux: source myenv/bin/activate
Windows: myenv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

create .env file that replicates the variables in app-example.yaml

Start the uvicorn server:

```bash
uvicorn main:app
```
 
To deploy to gcloud:

```bash
gcloud app deploy
```

Useful commands:

```bash
Update requirements: pur -r requirements.txt
```
