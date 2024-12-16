import React, { useState, useEffect } from 'react';
import { Job } from './types';
import { AppSidebar } from './components/custom/AppSidebar';
import { SidebarTrigger } from './components/ui/sidebar';

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [query, setQuery] = useState('');

  const fetchJobs = async (keyword = '') => {
    const response = await fetch(`http://localhost:5000/api/search?keyword=${keyword}`);
    const data: Job[] = await response.json();
    setJobs(data);
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchJobs(query);
  };

  return (
    <>
      <AppSidebar />
      <main>
        <SidebarTrigger />
      </main>
    </>
    // <div className="min-h-screen bg-gray-100">
    //   <nav className="bg-blue-500 text-white p-4 flex justify-between items-center">
    //     <div className="text-lg font-bold">Job Portal</div>
    //     <div>
    //       <a href="#home" className="mx-2">Home</a>
    //       <a href="#jobs" className="mx-2">Jobs</a>
    //       <a href="#about" className="mx-2">About</a>
    //     </div>
    //   </nav>

    //   <div id="jobs" className="container mx-auto p-4 bg-white mt-4 rounded shadow">
    //     <h1 className="text-2xl font-bold text-center mb-4">Job Listings</h1>
    //     <form className="text-center mb-4" onSubmit={handleSearch}>
    //       <input
    //         type="text"
    //         name="query"
    //         placeholder="Search jobs by title, company, or location..."
    //         className="w-3/4 p-2 border border-gray-300 rounded mr-2"
    //         value={query}
    //         onChange={(e) => setQuery(e.target.value)}
    //       />
    //       <button type="submit" className="p-2 bg-blue-500 text-white rounded">Search</button>
    //     </form>
    //     {jobs.map((job, index) => (
    //       <div key={index} className="job-listing mb-4 p-4 border-b border-gray-200">
    //         <a href={job.job_url || '#'} target="_blank" rel="noopener noreferrer" className="job-title text-lg font-bold text-blue-600">
    //           {job.title}
    //         </a>
    //         <p className="job-company text-gray-700">Company: {job.company}</p>
    //         <p className="job-location text-gray-700">Location: {job.location}</p>
    //         {job.salary && <p className="job-salary text-gray-700">Salary: {job.salary}</p>}
    //       </div>
    //     ))}
    //   </div>
    // </div>
  );
}

export default App;
