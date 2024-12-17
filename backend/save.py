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

class Company:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def to_rdf(self):
        company_uri = URIRef(f"http://example.org/company/{quote(self.name.replace(' ', '_'))}")
        rdf_graph.add((company_uri, RDF.type, EX.Company))
        rdf_graph.add((company_uri, EX.name, Literal(self.name)))
        rdf_graph.add((company_uri, EX.location, Literal(self.location)))
        return company_uri

class Job:
    def __init__(self, title, company, job_url, source, salary="No salary"):
        self.title = title
        self.company = company
        self.salary = salary
        self.job_url = job_url
        self.source = source

    def to_rdf(self):
        job_uri = URIRef(f"http://example.org/job/{quote(self.title.replace(' ', '_'))}")
        rdf_graph.add((job_uri, RDF.type, EX.Job))
        rdf_graph.add((job_uri, EX.title, Literal(self.title)))
        rdf_graph.add((job_uri, EX.salary, Literal(self.salary)))
        rdf_graph.add((job_uri, EX.company, self.company.to_rdf()))
        rdf_graph.add((job_uri, EX.job_url, Literal(self.job_url)))
        rdf_graph.add((job_uri, EX.source, Literal(self.source)))
        return job_uri

# def scrape_kemnaker(keyword=None):
#     base_url = "https://karirhub.kemnaker.go.id/lowongan-dalam-negeri/lowongan"
#     url = f"{base_url}?filters=keyword:{quote(keyword)}%23{quote(keyword)}" if keyword else base_url
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")

#     job_elements = soup.find_all("sisnaker-element-karirhub-domestic-vacancy-card-web")
#     print(url)
#     jobs = []
#     for job_element in job_elements:
#         try:
#             job_title_element = job_element.find("div", class_="text-sm font-bold text-grey-700")
#             job_title = extract_text(job_title_element)
#             company_element = job_element.find("div", class_="text-sm text-grey-700")
#             location_element = job_element.find("div", class_="text-xs text-grey-500")
#             salary_element = job_element.find("div", class_="font-medium text-grey-700")

#             company_name = extract_text(company_element, "No company")
#             location = extract_text(location_element, "No location")
#             salary = extract_text(salary_element, "No salary")
#             if "IDR" not in salary:
#                 salary = "No salary"

#             company = Company(company_name, location)
#             job = Job(job_title, company, url, "Kemnaker", salary)
#             job.to_rdf()

#             jobs.append({
#                 "title": job_title,
#                 "salary": salary,
#                 "company": company_name,
#                 "location": location,
#                 "job_url": url,
#                 "source": "Kemnaker"
#             })
#         except Exception:
#             continue

#     return jobs

def scrape_kitalulus(keyword=None):
    base_url = "https://www.kitalulus.com/lowongan"
    url = f"{base_url}?keyword={quote(keyword)}" if keyword else base_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    job_elements = soup.find_all("div", class_="CardRectangleStyled__Container-sc-1lom4v1-0 iwlPnJ")
    
    jobs = []
    for job_element in job_elements:
        try:
            job_title_element = job_element.find("h3", class_="TextStyled__H3-sc-18vo2dc-3 eHZQKp")
            job_title = extract_text(job_title_element)
            
            a_tag = job_element.find("a", href=True)
            job_url = "https://www.kitalulus.com" + a_tag["href"] if a_tag else "No URL"

            company_element = job_element.find("p", class_="TextStyled__Text-sc-18vo2dc-0 kaIrsv")
            location_element = job_element.find("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb")
            qualification_element = location_element.find_next("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb") if location_element else None
            salary_element = qualification_element.find_next("p", class_="CardRectangleStyled__Text-sc-1lom4v1-8 drzZmb") if qualification_element else None

            company_name = extract_text(company_element, "No company")
            location = extract_text(location_element, "No location")
            salary = extract_text(salary_element, "No salary")
            if "Rp" not in salary:
                salary = "No salary"
            
            print(job_title, company_name, location, salary, job_url)

            company = Company(company_name, location)
            job = Job(job_title, company, job_url, "KitaLulus", salary)
            job.to_rdf()

            jobs.append({
                "title": job_title,
                "salary": salary,
                "company": company_name,
                "location": location,
                "job_url": job_url,
                "source": "KitaLulus"
            })
        except Exception:
            continue

    return jobs

def scrape_jobstreet(keyword=None):
    base_url = "https://id.jobstreet.com/id"
    url = f"{base_url}/{quote(keyword.replace(' ', '-'))}-jobs" if keyword else f"{base_url}/Programmer-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    for item in soup.find_all('article', class_='_1unphw40 _1unphw41 tcmsgw8n tcmsgw8o tcmsgw7j tcmsgw7k tcmsgwav tcmsgwaw tcmsgw9r tcmsgw9s tcmsgwh tcmsgw67 tcmsgw5f s57onkb s57onk9 s57onka _1siu89c18 _1siu89c1b tcmsgw33 tcmsgw36'):
        try:
            job_url = 'https://id.jobstreet.com' + item.find('a')['href']
            title = extract_text(item.find('a', {'data-automation': 'jobTitle'}), "Invalid")
            company_name = extract_text(item.find('a', {'data-automation': 'jobCompany'}), "Invalid")
            location = extract_text(item.find('span', {'data-automation': 'jobCardLocation'}), "Invalid")
            salary = extract_text(item.find('span', {'data-automation': 'jobSalary'}), "No salary")

            company = Company(name=company_name, location=location)
            job = Job(title=title, company=company, job_url=job_url, source="Jobstreet", salary=salary)
            job.to_rdf()

            jobs.append({
                "title": title,
                "company": company_name,
                "location": location,
                "salary": salary,
                "job_url": job_url,
                "source": "Jobstreet"
            })
        except Exception:
            continue

    return jobs

def search_and_store_jobs(keyword=None):
    jobs = []
    # jobs.extend(scrape_kemnaker(keyword))
    jobs.extend(scrape_kitalulus(keyword))
    jobs.extend(scrape_jobstreet(keyword))
    
    # Serialize and upload to GraphDB
    graphdb_url = os.getenv("GRAPHDB_ENDPOINT") + '/repositories/lokerku' + "/statements"
    upload_to_graphdb_via_sparql(rdf_graph, graphdb_url)
    
    # Clear the RDF graph
    rdf_graph.remove((None, None, None))
    
    return jobs

# Helper function to extract text or return a default value
def extract_text(element, default="No data"):
    return element.text.strip() if element else default

def delete_all_jobs_and_companies(sparql_endpoint_url):
    # Define the SPARQL Update query to delete all instances of Job and Company
    sparql_delete_query = """
    DELETE WHERE {
        ?entity a <http://example.org/ontology/Job> .
        ?entity ?p ?o .
    };
    DELETE WHERE {
        ?entity a <http://example.org/ontology/Company> .
        ?entity ?p ?o .
    }
    """

    headers = {
        "Content-Type": "application/sparql-update",  # Correct MIME type
    }

    # Send POST request to SPARQL endpoint
    response = requests.post(sparql_endpoint_url, data=sparql_delete_query.encode("utf-8"), headers=headers)
    if response.status_code in (200, 204):  # HTTP 200 atau 204 indicates success
        print("Semua instance Job dan Company berhasil dihapus dari GraphDB!")
    else:
        print(f"Gagal menghapus instance Job dan Company dari GraphDB: {response.status_code} {response.text}")

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
    if response.status_code in (200, 204):  # HTTP 200 atau 204 indicates success
        print("Data RDF berhasil diunggah ke GraphDB melalui SPARQL!")
    else:
        print(f"Gagal mengunggah data RDF melalui SPARQL: {response.status_code} {response.text}")

# if __name__ == "__main__":
#     graphdb_url = os.getenv("GRAPHDB_ENDPOINT")  + '/repositories/lokerku' + "/statements"

#     # URL repository GraphDB
#     # Menghapus semua instance Job dan Company dari GraphDB
#     delete_all_jobs_and_companies(graphdb_url)

#     # Mengunggah data RDF ke GraphDB
#     upload_to_graphdb_via_sparql(rdf_graph, graphdb_url)
