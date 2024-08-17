import { NavBar } from '../../components/layout/NavBar';
import React from 'react';

export const DashboardPage = () => {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="w-full flex-none md:w-64">
        <NavBar />
      </div>
      <div className="flex-grow p-6 md:overflow-y-auto md:p-12">
        <div>Home Page</div>
      </div>
    </div>
  );
};
