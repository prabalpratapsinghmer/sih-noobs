import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge } from '@sih/ui-kit';
import { Building2, X } from 'lucide-react';

const INITIAL_STATIONS = [
  { id: 'KA-BGL-01', name: 'Indiranagar PS', active: 45, vehicles: 12 },
  { id: 'KA-BGL-02', name: 'Koramangala PS', active: 38, vehicles: 9 },
  { id: 'KA-BGL-03', name: 'Whitefield PS', active: 62, vehicles: 15 },
];

export function Stations() {
  const [stations, setStations] = useState(() => {
    const saved = localStorage.getItem('adminStations');
    return saved ? JSON.parse(saved) : INITIAL_STATIONS;
  });

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingStation, setEditingStation] = useState<any>(null);
  const [formData, setFormData] = useState({ id: '', name: '', active: 0, vehicles: 0 });

  useEffect(() => {
    localStorage.setItem('adminStations', JSON.stringify(stations));
  }, [stations]);

  const handleOpenModal = (station: any = null) => {
    if (station) {
      setEditingStation(station);
      setFormData(station);
    } else {
      setEditingStation(null);
      setFormData({ id: '', name: '', active: 0, vehicles: 0 });
    }
    setIsModalOpen(true);
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingStation) {
      setStations(stations.map((s: any) => s.id === editingStation.id ? { ...formData } : s));
    } else {
      setStations([...stations, { ...formData }]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="max-w-[1400px] mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight">Station Assignments</h1>
        <Button className="bg-accent hover:bg-accent-2 text-white transition-all" onClick={() => handleOpenModal()}>
          Add Station
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stations.map((station: any) => (
          <Card key={station.id} className="shadow-sm border border-line hover:border-accent transition-all hover:-translate-y-1">
            <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center text-ink">
                  <Building2 className="w-5 h-5 mr-2 text-muted" />
                  {station.name}
                </CardTitle>
                <Badge variant="default" className="bg-surface">{station.id}</Badge>
              </div>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted">Active Officers</span>
                <span className="font-bold text-ink">{station.active}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted">Patrol Vehicles</span>
                <span className="font-bold text-ink">{station.vehicles}</span>
              </div>
              <Button 
                variant="default" 
                className="w-full mt-2 transition-all"
                onClick={() => handleOpenModal(station)}
              >
                Manage Assignment
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
          <Card className="w-full max-w-md shadow-2xl border-line">
            <CardHeader className="flex flex-row justify-between items-center border-b border-line bg-surface-2">
              <CardTitle>{editingStation ? 'Manage Station' : 'Add New Station'}</CardTitle>
              <button onClick={() => setIsModalOpen(false)} className="text-muted hover:text-ink transition-colors">
                <X className="w-5 h-5" />
              </button>
            </CardHeader>
            <CardContent className="pt-6">
              <form onSubmit={handleSave} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">Station Name</label>
                  <input required type="text" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">Station ID</label>
                  <input required type="text" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.id} onChange={e => setFormData({...formData, id: e.target.value})} placeholder="e.g. KA-BGL-04" disabled={!!editingStation} />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-ink mb-1">Active Officers</label>
                    <input required type="number" min="0" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.active} onChange={e => setFormData({...formData, active: parseInt(e.target.value) || 0})} />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-ink mb-1">Patrol Vehicles</label>
                    <input required type="number" min="0" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.vehicles} onChange={e => setFormData({...formData, vehicles: parseInt(e.target.value) || 0})} />
                  </div>
                </div>
                <div className="pt-4 flex space-x-3">
                  <Button type="button" variant="default" className="flex-1" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" className="flex-1 bg-accent text-white">{editingStation ? 'Save Assignment' : 'Create Station'}</Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
