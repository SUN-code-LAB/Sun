import React from 'react';

const StatusDot = ({ status }: { status: string }) => {
  const colorClass = status === 'High' ? 'bg-red-500' : status === 'Moderate' ? 'bg-yellow-500' : 'bg-green-500';
  return <div className={`w-2.5 h-2.5 rounded-full ${colorClass}`} />;
};

export const ADMETPanel = ({ data }: { data: any }) => {
  if (!data) return <div className="p-4 bg-navy-900 rounded-lg border border-navy-800 animate-pulse h-64"></div>;

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">ADMET PREDICTION</h3>

      <div className="space-y-3">
        {Object.entries(data.admet).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between bg-navy-800/30 p-2.5 rounded border border-navy-800/50">
            <span className="text-sm text-gray-300">{key}</span>
            <div className="flex items-center gap-2">
              <StatusDot status={value as string} />
              <span className="text-xs text-gray-400 w-16 text-right">{value as string}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const MolecularInfoPanel = ({ data }: { data: any }) => {
  if (!data) return null;
  const info = data.molecular_info;

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">MOLECULAR INFORMATION</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-500 mb-1">Atoms</p>
          <p className="text-sm font-semibold text-gray-200">{info.atoms}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Bonds</p>
          <p className="text-sm font-semibold text-gray-200">{info.bonds}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Rings</p>
          <p className="text-sm font-semibold text-gray-200">{info.rings}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">HBD</p>
          <p className="text-sm font-semibold text-gray-200">{info.hbd}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">HBA</p>
          <p className="text-sm font-semibold text-gray-200">{info.hba}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">TPSA</p>
          <p className="text-sm font-semibold text-gray-200">{info.tpsa}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">LogP</p>
          <p className="text-sm font-semibold text-gray-200">{info.logp}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Solubility</p>
          <p className="text-sm font-semibold text-gray-200">{info.solubility}</p>
        </div>
      </div>
    </div>
  );
};

export const DrugLikenessPanel = ({ data }: { data: any }) => {
  if (!data) return null;
  const lipinski = data.molecular_info.lipinski;

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">DRUG LIKENESS</h3>
      <p className="text-xs text-gray-400 mb-4 uppercase">Lipinski Rule of 5</p>

      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <span className={`text-sm ${lipinski.mw ? 'text-green-400' : 'text-red-400'}`}>{lipinski.mw ? '✓' : '✗'}</span>
          <span className="text-sm text-gray-300">MW &lt; 500</span>
        </div>
        <div className="flex items-center gap-3">
          <span className={`text-sm ${lipinski.logp ? 'text-green-400' : 'text-red-400'}`}>{lipinski.logp ? '✓' : '✗'}</span>
          <span className="text-sm text-gray-300">LogP &lt; 5</span>
        </div>
        <div className="flex items-center gap-3">
          <span className={`text-sm ${lipinski.hbd ? 'text-green-400' : 'text-red-400'}`}>{lipinski.hbd ? '✓' : '✗'}</span>
          <span className="text-sm text-gray-300">HBD &lt; 5</span>
        </div>
        <div className="flex items-center gap-3">
          <span className={`text-sm ${lipinski.hba ? 'text-green-400' : 'text-red-400'}`}>{lipinski.hba ? '✓' : '✗'}</span>
          <span className="text-sm text-gray-300">HBA &lt; 10</span>
        </div>
      </div>
    </div>
  );
};
