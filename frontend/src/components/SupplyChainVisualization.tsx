'use client';

import { useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';

interface SupplyChainStep {
  id: string;
  name: string;
  type: 'material' | 'process' | 'transport' | 'company';
  location?: string;
  company?: string;
  carbonEmission?: string;
  description?: string;
}

interface SupplyChainVisualizationProps {
  analysisResult: any;
}

export function SupplyChainVisualization({ analysisResult }: SupplyChainVisualizationProps) {
  const steps = useMemo(() => {
    if (!analysisResult?.analysis_result) return [];

    const result = analysisResult.analysis_result;
    const allSteps: SupplyChainStep[] = [];

    // Add materials as starting steps
    result.materials?.forEach((material: any, index: number) => {
      allSteps.push({
        id: `material-${index}`,
        name: material.name,
        type: 'material',
        location: material.source_regions?.[0] || 'Unknown',
        company: getTypicalCompany('material', material.name),
        description: `Raw material from ${material.source_regions?.join(', ') || 'various regions'}`
      });
    });

    // Add processes
    result.processes?.forEach((process: any, index: number) => {
      allSteps.push({
        id: `process-${index}`,
        name: process.name,
        type: 'process',
        location: process.location,
        company: getTypicalCompany('process', process.name),
        carbonEmission: process.carbon_emissions,
        description: process.energy_requirement
      });
    });

    // Add transportation between processes
    result.transportation?.forEach((transport: any, index: number) => {
      allSteps.push({
        id: `transport-${index}`,
        name: `${transport.mode} transport`,
        type: 'transport',
        location: `${transport.from} → ${transport.to}`,
        company: getTypicalCompany('transport', transport.mode),
        carbonEmission: transport.carbon_emissions,
        description: `${transport.distance_km}km via ${transport.mode}`
      });
    });

    // Add final companies
    result.companies?.slice(0, 2).forEach((company: any, index: number) => {
      allSteps.push({
        id: `company-${index}`,
        name: company.name,
        type: 'company',
        location: company.region,
        company: company.name,
        description: `${company.role} in ${company.region}`
      });
    });

    return allSteps;
  }, [analysisResult]);

  function getTypicalCompany(type: string, name: string): string {
    const companies = {
      material: {
        'cotton': 'Cotton Growers Co-op',
        'steel': 'ArcelorMittal',
        'aluminum': 'Alcoa',
        'plastic': 'Dow Chemical',
        'lithium': 'Albemarle Corp',
        'oil': 'ExxonMobil',
        default: 'Material Supplier Inc'
      },
      process: {
        'cultivation': 'AgriCorp Farms',
        'mining': 'Global Mining Ltd',
        'refining': 'ProcessTech Industries',
        'manufacturing': 'Manufacturing Solutions',
        'assembly': 'Assembly Partners',
        'spinning': 'Textile Mills Inc',
        'weaving': 'Fabric Works Ltd',
        'smelting': 'Metal Processing Co',
        default: 'Processing Corp'
      },
      transport: {
        'truck': 'FreightLine Logistics',
        'ship': 'Maersk Shipping',
        'air': 'DHL Cargo',
        'rail': 'Union Pacific',
        default: 'Transport Solutions'
      }
    };

    const category = companies[type as keyof typeof companies];
    if (category) {
      for (const [key, value] of Object.entries(category)) {
        if (name.toLowerCase().includes(key)) {
          return value;
        }
      }
      return category.default;
    }
    return 'Supply Chain Partner';
  }

  function getCardColor(type: string): string {
    switch (type) {
      case 'material': return 'border-green-200 bg-green-50';
      case 'process': return 'border-blue-200 bg-blue-50';
      case 'transport': return 'border-orange-200 bg-orange-50';
      case 'company': return 'border-purple-200 bg-purple-50';
      default: return 'border-gray-200 bg-gray-50';
    }
  }

  function getIconForType(type: string): string {
    switch (type) {
      case 'material': return '🌱';
      case 'process': return '⚙️';
      case 'transport': return '🚛';
      case 'company': return '🏢';
      default: return '📦';
    }
  }

  if (steps.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        No supply chain data available for visualization
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto p-4">
      <div className="relative min-w-max">
        {/* Supply Chain Flow */}
        <div className="flex items-center gap-4 pb-8">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              {/* Card */}
              <Card 
                className={`${getCardColor(step.type)} min-w-[200px] cursor-pointer hover:shadow-md transition-shadow`}
                title="Click for details (coming soon)"
              >
                <CardContent className="p-3">
                  <div className="flex items-start gap-2">
                    <span className="text-lg">{getIconForType(step.type)}</span>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm truncate">{step.name}</h4>
                      <p className="text-xs text-gray-600 truncate">{step.company}</p>
                      {step.location && (
                        <p className="text-xs text-gray-500 truncate">📍 {step.location}</p>
                      )}
                      {step.carbonEmission && (
                        <p className="text-xs text-red-600">💨 {step.carbonEmission} kg CO₂</p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Connecting Arrow */}
              {index < steps.length - 1 && (
                <div className="flex items-center px-2">
                  <div className="h-px bg-gray-300 w-8"></div>
                  <div className="w-0 h-0 border-l-4 border-l-gray-300 border-t-2 border-t-transparent border-b-2 border-b-transparent"></div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-6 text-xs text-gray-600 border-t pt-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-green-200 bg-green-50 border rounded"></div>
            <span>🌱 Materials</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-blue-200 bg-blue-50 border rounded"></div>
            <span>⚙️ Processes</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-orange-200 bg-orange-50 border rounded"></div>
            <span>🚛 Transport</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-purple-200 bg-purple-50 border rounded"></div>
            <span>🏢 Companies</span>
          </div>
        </div>
      </div>
    </div>
  );
}