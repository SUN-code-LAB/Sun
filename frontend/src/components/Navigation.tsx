import React from 'react';
import {
  Dna,
  LayoutDashboard,
  Search,
  Activity,
  ShieldAlert,
  Network,
  Baby,
  Milk,
  BrainCircuit,
  MessageSquare,
  Settings
} from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard' },
  { icon: Search, label: 'Compound Explorer' },
  { icon: Dna, label: 'Molecular Analysis' },
  { icon: Activity, label: 'Physicochemical Properties' },
  { icon: ShieldAlert, label: 'ADMET Prediction' },
  { icon: Network, label: 'Placental Transfer' },
  { icon: Milk, label: 'Breast Milk Prediction' },
  { icon: Baby, label: 'Toxicity Analysis' },
  { icon: BrainCircuit, label: 'Explainable AI' },
  { icon: Dna, label: 'Scientific Reports' },
];

export const Navigation = () => {
  return (
    <nav className="w-64 bg-gray-900 border-r border-gray-800 h-screen flex flex-col">
      <div className="p-4 border-b border-gray-800 flex items-center gap-3">
        <Dna className="text-blue-500" size={28} />
        <h1 className="font-bold text-lg text-white">MaternalSafe AI</h1>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {navItems.map((item, idx) => (
            <li key={idx}>
              <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
                <item.icon size={18} />
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="p-4 border-t border-gray-800">
        <ul className="space-y-1">
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-blue-400 hover:text-blue-300 hover:bg-gray-800 rounded-md transition-colors">
              <MessageSquare size={18} />
              AI Assistant
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
              <Settings size={18} />
              Settings
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};
