import React from 'react';
import {
  LayoutDashboard,
  Search,
  Dna,
  Activity,
  ShieldAlert,
  Baby,
  Network,
  Milk,
  AlertTriangle,
  Microscope,
  BrainCircuit,
  BookOpen,
  Share2,
  Users,
  FileText,
  History,
  Settings,
  MessageSquare
} from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard' },
  { icon: Search, label: 'Compound Explorer' },
  { icon: Dna, label: 'Molecular Analysis' },
  { icon: Activity, label: 'Physicochemical Properties' },
  { icon: ShieldAlert, label: 'ADMET Intelligence' },
  { icon: Baby, label: 'Pregnancy Safety' },
  { icon: Network, label: 'Placental Transfer AI' },
  { icon: Milk, label: 'Breast Milk Prediction' },
  { icon: AlertTriangle, label: 'Toxicity Analysis' },
  { icon: Microscope, label: 'Molecular Mechanism' },
  { icon: BrainCircuit, label: 'Explainable AI' },
  { icon: BookOpen, label: 'Literature Intelligence' },
  { icon: Share2, label: 'Knowledge Graph' },
  { icon: Users, label: 'Digital Twin' },
  { icon: FileText, label: 'Scientific Reports' },
  { icon: History, label: 'Research History' },
];

export const Navigation = () => {
  return (
    <nav className="w-64 bg-card border-r border-card-border h-screen flex flex-col">
      <div className="p-4 border-b border-card-border flex items-center gap-3">
        <Dna className="text-ai-blue" size={28} />
        <h1 className="font-bold text-lg text-white">MaternalSafe AI X</h1>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {navItems.map((item, idx) => (
            <li key={idx}>
              <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-ai-blue hover:bg-gray-800/50 rounded-md transition-colors">
                <item.icon size={18} />
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="p-4 border-t border-card-border">
        <ul className="space-y-1">
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-ai-blue hover:text-blue-300 hover:bg-gray-800/50 rounded-md transition-colors">
              <Settings size={18} />
              Settings
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-scientific-purple hover:text-purple-300 hover:bg-gray-800/50 rounded-md transition-colors">
              <MessageSquare size={18} />
              AI Assistant
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};
