import React from 'react';
import {
  Home,
  Search,
  Dna,
  TestTube,
  Pill,
  Network,
  ShieldAlert,
  BrainCircuit,
  BarChart,
  FileText,
  BookOpen,
  Database,
  MessageSquare,
  Settings
} from 'lucide-react';

const navItems = [
  { icon: Home, label: 'Dashboard' },
  { icon: Search, label: 'Compound Explorer' },
  { icon: Dna, label: 'Molecular Analysis' },
  { icon: TestTube, label: 'Physicochemical Properties' },
  { icon: Pill, label: 'ADMET Prediction' },
  { icon: Dna, label: 'CYP450 Metabolism' },
  { icon: Network, label: 'Renal Transport System' },
  { icon: ShieldAlert, label: 'Kidney Toxicity Module' },
  { icon: BrainCircuit, label: 'Explainable AI' },
  { icon: BarChart, label: 'QSAR Model Center' },
  { icon: FileText, label: 'Scientific Report Module' },
  { icon: BookOpen, label: 'Knowledge Base' },
  { icon: Database, label: 'History & Database' },
];

export const Navigation = () => {
  return (
    <nav className="w-64 bg-navy-900 border-r border-navy-800 h-screen flex flex-col">
      <div className="p-4 border-b border-navy-800 flex flex-col items-center justify-center text-center">
        <div className="text-3xl mb-2">🫘 + 🧬</div>
        <h1 className="font-bold text-lg text-white leading-tight">RENAL ADMET AI</h1>
        <p className="text-xs text-primary mt-1">AI-Powered Molecular<br/>Safety Intelligence</p>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {navItems.map((item, idx) => (
            <li key={idx}>
              <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-navy-800 rounded-md transition-colors">
                <item.icon size={18} />
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="p-4 border-t border-navy-800">
        <ul className="space-y-1">
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-primary hover:text-white hover:bg-navy-800 rounded-md transition-colors">
              <MessageSquare size={18} />
              AI Assistant
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-navy-800 rounded-md transition-colors">
              <Settings size={18} />
              Settings
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};
