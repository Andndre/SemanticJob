from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

# Konfigurasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi GraphDB
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT") 

# Fungsi untuk mengambil data lowongan pekerjaan dari GraphDB
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

# Route utama untuk menampilkan semua lowongan pekerjaan
@app.route("/")
def home():
    jobs = get_jobs()
    return render_template("index.html", jobs=jobs)

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)

