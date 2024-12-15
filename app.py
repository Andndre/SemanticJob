from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from save import scrape_kemnaker, scrape_kitalulus, delete_all_jobs_and_companies, upload_to_graphdb_via_sparql, rdf_graph

# Konfigurasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi GraphDB
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT")

def get_jobs():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = """
    PREFIX ex: <http://example.org/ontology/>
    SELECT DISTINCT ?title ?salary ?companyName ?location ?job_url WHERE {
        ?job a ex:Job ;
             ex:title ?title ;
             ex:salary ?salary ;
             ex:company ?company ;
             ex:job_url ?job_url .
        ?company ex:name ?companyName ;
                 ex:location ?location .
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    jobs = []
    for result in results["results"]["bindings"]:
        job = {
            "title": result["title"]["value"],
            "salary": result["salary"]["value"],
            "companyName": result["companyName"]["value"],
            "location": result["location"]["value"],
            "job_url": result["job_url"]["value"]
        }
        jobs.append(job)
        
    return jobs

# Fungsi untuk mencari lowongan pekerjaan berdasarkan kata kunci
def search_jobs(keyword):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = f"""
    PREFIX ex: <http://example.org/ontology/>
    SELECT DISTINCT ?title ?salary ?companyName ?location ?job_url WHERE {{
        ?job a ex:Job ;
             ex:title ?title ;
             ex:salary ?salary ;
             ex:company ?company ;
             ex:job_url ?job_url .
        ?company ex:name ?companyName ;
                 ex:location ?location .
        FILTER (
            CONTAINS(LCASE(?title), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?companyName), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?location), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?salary), LCASE("{keyword}"))
        )
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
            "salary": result["salary"]["value"],
            "company": result["companyName"]["value"],
            "location": result["location"]["value"],
            "job_url": result["job_url"]["value"]
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

# Route untuk melakukan scraping dan mengunggah data ke GraphDB
@app.route("/scrape", methods=["GET"])
def scrape():
    scrape_kemnaker()
    scrape_kitalulus()
    delete_all_jobs_and_companies(GRAPHDB_ENDPOINT + "/statements")
    upload_to_graphdb_via_sparql(rdf_graph, GRAPHDB_ENDPOINT + "/statements")
    return jsonify({'message': 'Scraping completed'}), 200

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
