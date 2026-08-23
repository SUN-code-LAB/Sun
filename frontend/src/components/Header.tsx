import React from 'react';
import { Search, Bell, User } from 'lucide-react';

export const Header = () => {
  return (
    <header className="h-16 bg-navy-900 border-b border-navy-800 flex items-center justify-between px-6">
      <div>
        <h2 className="text-xl font-bold text-white">RENAL ADMET AI</h2>
        <p className="text-xs text-gray-400">AI-Powered Molecular Safety Intelligence Platform</p>
      </div>

      <div className="flex items-center gap-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
          <input
            type="text"
            placeholder="Search PubChem CID or Name"
            className="bg-navy-800 text-sm text-white rounded-full pl-10 pr-4 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary w-64 border border-navy-800"
          />
        </div>

        <div className="flex items-center gap-4 text-gray-400">
          <button className="hover:text-white transition-colors">
            <Bell size={20} />
          </button>
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white">
            <User size={16} />
          </div>
        </div>
      </div>
    </header>
  );
};
