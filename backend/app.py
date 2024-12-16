from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS, cross_origin
from save import scrape_kemnaker, scrape_kitalulus, delete_all_jobs_and_companies, upload_to_graphdb_via_sparql, rdf_graph, scrape_kemnaker_with_keyword, scrape_kitalulus_with_keyword

# Konfigurasi aplikasi Flask
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Konfigurasi GraphDB
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT") + '/repositories/lokerku'

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
    jobs_kemnaker = scrape_kemnaker_with_keyword(keyword)
    jobs_kitalulus = scrape_kitalulus_with_keyword(keyword)
    return jobs_kemnaker + jobs_kitalulus

# Route utama untuk menampilkan semua lowongan pekerjaan
@app.route("/", methods=["GET"])
def home():
    keyword = request.args.get("query", "").strip()
    if keyword:
        jobs = search_jobs(keyword)
    else:
        jobs = get_jobs()
    return render_template("index.html", jobs=jobs)

@app.route("/api/jobs", methods=["GET"])
def api_home():
    page = int(request.args.get("page", 1))
    total_per_page = int(request.args.get("total_per_page", 10))
    jobs = get_jobs()
    start = (page - 1) * total_per_page
    end = start + total_per_page
    paginated_jobs = jobs[start:end]
    return jsonify(paginated_jobs)

# Route REST API untuk mencari lowongan pekerjaan berdasarkan kata kunci
@app.route("/api/search", methods=["GET"])
def api_search():
    keyword = request.args.get("keyword", "").strip()
    if keyword:
        jobs = search_jobs(keyword)
        return jsonify(jobs)
    else:
        return jsonify([])

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    scrape_kemnaker()
    scrape_kitalulus()
    # delete_all_jobs_and_companies(GRAPHDB_ENDPOINT + "/statements")
    upload_to_graphdb_via_sparql(rdf_graph, GRAPHDB_ENDPOINT + "/statements")
    app.run(host='0.0.0.0', port=5000, debug=True)
