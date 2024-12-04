from rdflib import Graph, Namespace, Literal, RDF, URIRef
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

# Namespace untuk RDF
EX = Namespace("http://example.org/ontology/")

# Membuat graph RDF
rdf_graph = Graph()
rdf_graph.bind("ex", EX)

# Scraping dari KarirHub Kemnaker
def scrape_kemnaker():
    url = "https://karirhub.kemnaker.go.id/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_elements = soup.find_all("a", class_="block font-bold truncate cursor-pointer hover:text-primary text-sm")

    for job_element in job_elements:
        job_title = job_element.text.strip()
        job_url = job_element["title"]
        company_element = job_element.find_next("div", class_="text-sm text-grey-700 truncate")
        location_element = job_element.find_next("div", class_="text-xs text-grey-500 truncate")

        company = company_element.text.strip() if company_element else "No company"
        location = location_element.text.strip() if location_element else "No location"

        # Menambahkan data ke RDF graph
        job_uri = URIRef(f"http://example.org/job/{job_title.replace(' ', '_')}")
        rdf_graph.add((job_uri, RDF.type, EX.Job))
        rdf_graph.add((job_uri, EX.source, Literal("KarirHub Kemnaker")))
        rdf_graph.add((job_uri, EX.title, Literal(job_title)))
        rdf_graph.add((job_uri, EX.company, Literal(company)))
        rdf_graph.add((job_uri, EX.location, Literal(location)))
        rdf_graph.add((job_uri, EX.salary, Literal("No salary")))

# Helper function to extract text or return a default value
def extract_text(element, default="No data"):
    return element.text.strip() if element else default

# Scraping dari KitaLulus
def scrape_kitalulus():
    url = "https://www.kitalulus.com/lowongan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    job_elements = soup.find_all("h3", class_="TextStyled__H3-sc-18vo2dc-3 eHZQKp")
    
    if not job_elements:
        return
    
    for job_element in job_elements:
        job_title = extract_text(job_element)
        company_element = job_element.find_next("p", class_="TextStyled__Text-sc-18vo2dc-0 kaIrsv")
        location_element = job_element.find_next("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb")
        qualification_element = location_element.find_next("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb") if location_element else None
        salary_element = qualification_element.find_next("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb") if qualification_element else None

        company = extract_text(company_element, "No company")
        location = extract_text(location_element, "No location")
        salary = extract_text(salary_element, "No salary")
        if "Rp" not in salary:
            salary = "No salary"

        # Adding data to RDF graph
        job_uri = URIRef(f"http://example.org/job/{quote(job_title.replace(' ', '_'))}")
        rdf_graph.add((job_uri, RDF.type, EX.Job))
        rdf_graph.add((job_uri, EX.source, Literal("KitaLulus")))
        rdf_graph.add((job_uri, EX.title, Literal(job_title)))
        rdf_graph.add((job_uri, EX.company, Literal(company)))
        rdf_graph.add((job_uri, EX.location, Literal(location)))
        rdf_graph.add((job_uri, EX.salary, Literal(salary)))

# Mengirimkan data RDF ke GraphDB
def upload_to_graphdb_via_sparql(graph, sparql_endpoint_url):
    # Serialize graph to Turtle format
    turtle_data = graph.serialize(format="turtle")

    # Define the SPARQL Update query
    sparql_update_query = f"""
    INSERT DATA {{
        {turtle_data}
    }}
    """

    headers = {
        "Content-Type": "application/sparql-update",  # SPARQL Update MIME type
    }

    # Send POST request to SPARQL endpoint
    response = requests.post(sparql_endpoint_url, data=sparql_update_query.encode("utf-8"), headers=headers)
    if response.status_code in (200, 204):  # HTTP 200 or 204 indicates success
        print("Data RDF berhasil diunggah ke GraphDB melalui SPARQL!")
    else:
        print(f"Gagal mengunggah data RDF melalui SPARQL: {response.status_code} {response.text}")

# Menjalankan fungsi scraping dan menyimpan data
scrape_kemnaker()
scrape_kitalulus()

# URL repository GraphDB
graphdb_url = os.getenv("GRAPHDB_ENDPOINT")

# Mengunggah data RDF ke GraphDB
upload_to_graphdb_via_sparql(rdf_graph, graphdb_url)
