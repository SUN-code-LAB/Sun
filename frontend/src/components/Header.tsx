import React from 'react';
import { Search, User, Bell } from 'lucide-react';

export const Header = () => {
  return (
    <header className="bg-card border-b border-card-border py-4 px-6 flex justify-between items-center">
      <div>
        <h2 className="text-xl font-semibold text-white">Welcome to MaternalSafe AI X</h2>
        <p className="text-sm text-gray-400 mt-1">AI-Powered Maternal Chemical Safety Platform</p>
      </div>

      <div className="flex items-center gap-6">
        <div className="relative">
          <input
            type="text"
            placeholder="Search PubChem CID / Compound Name"
            className="w-80 bg-gray-900 border border-card-border rounded-lg pl-10 pr-4 py-2 text-sm text-gray-200 focus:outline-none focus:border-ai-blue focus:ring-1 focus:ring-ai-blue transition-colors"
          />
          <Search className="absolute left-3 top-2.5 text-gray-500" size={16} />
        </div>

        <div className="flex items-center gap-3 border-l border-card-border pl-6">
          <button className="text-gray-400 hover:text-white transition-colors">
            <Bell size={20} />
          </button>
          <div className="w-8 h-8 rounded-full bg-ai-blue/20 flex items-center justify-center text-ai-blue">
            <User size={18} />
          </div>
        </div>
      </div>
    </header>
  );
};
