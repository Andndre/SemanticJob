// import React, { useState, useEffect } from 'react';
// import { Job } from './types';
import { AppSidebar } from '@/components/custom/AppSidebar';
import { SidebarTrigger } from '@/components/ui/sidebar';

function App() {
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
