from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

# Konfigurasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi GraphDB
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT")

# Fungsi untuk mengambil semua lowongan pekerjaan dari GraphDB
def get_jobs():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = """
    PREFIX ex: <http://example.org/ontology/>
    SELECT ?title ?company ?location ?salary ?source
    WHERE {
        ?job a ex:Job ;
             ex:title ?title ;
             ex:company ?company ;
             ex:location ?location ;
             ex:salary ?salary ;
             ex:source ?source .
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    jobs = []
    for result in results["results"]["bindings"]:
        jobs.append({
            "title": result["title"]["value"],
            "company": result["company"]["value"],
            "location": result["location"]["value"],
            "salary": result["salary"]["value"],
            "source": result["source"]["value"],
        })
    return jobs

# Fungsi untuk mencari lowongan pekerjaan berdasarkan kata kunci
def search_jobs(keyword):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = f"""
    PREFIX ex: <http://example.org/ontology/>
    PREFIX search: <http://www.ontotext.com/owlim/fulltext#>
    SELECT ?title ?company ?location ?salary ?source
    WHERE {{
        ?job a ex:Job ;
             ex:title ?title ;
             ex:company ?company ;
             ex:location ?location ;
             ex:salary ?salary ;
             ex:source ?source .
        {{
            ?title search:matches '{keyword}' .
        }}
        UNION
        {{
            ?company search:matches '{keyword}' .
        }}
        UNION
        {{
            ?location search:matches '{keyword}' .
        }}
        UNION
        {{
            ?salary search:matches '{keyword}' .
        }}
    }}
    LIMIT 50
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    jobs = []
    for result in results["results"]["bindings"]:
        jobs.append({
            "title": result["title"]["value"],
            "company": result["company"]["value"],
            "location": result["location"]["value"],
            "salary": result["salary"]["value"],
            "source": result["source"]["value"],
        })
    return jobs



# Route utama untuk menampilkan semua lowongan pekerjaan
@app.route("/", methods=["GET"])
def home():
    keyword = request.args.get("query", "").strip()
    if keyword:
        jobs = search_jobs(keyword)
    else:
        jobs = get_jobs()
    return render_template("index.html", jobs=jobs)

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
