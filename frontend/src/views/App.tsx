// import React, { useState, useEffect } from 'react';
// import { Job } from './types';
import { AppSidebar } from '../components/custom/AppSidebar';
import { SidebarTrigger } from '../components/ui/sidebar';

function App() {
  // const [jobs, setJobs] = useState<Job[]>([]);
  // const [query, setQuery] = useState('');

  // const fetchJobs = async (keyword = '') => {
  //   const response = await fetch(`http://localhost:5000/api/search?keyword=${keyword}`);
  //   const data: Job[] = await response.json();
  //   setJobs(data);
  // };

  // useEffect(() => {
  //   fetchJobs();
  // }, []);

  // const handleSearch = (e: React.FormEvent) => {
  //   e.preventDefault();
  //   fetchJobs(query);
  // };

  return (
    <>
      <AppSidebar />
      <main className='flex-1'>
        <nav className='bg-blue-500 text-white p-4 flex justify-between items-center w-full'>
          <SidebarTrigger />
        </nav>
      </main>
    </>
  );
}

export default App;
