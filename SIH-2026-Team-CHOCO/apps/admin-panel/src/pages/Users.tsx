import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge } from '@sih/ui-kit';
import { Search, UserPlus, X } from 'lucide-react';

const INITIAL_USERS = [
  { id: '1', name: 'Ramesh Sharma', rank: 'BGL-4491-C (Constable)', station: 'Indiranagar Unit 4', status: 'Active' },
  { id: '2', name: 'Anita Singh', rank: 'BGL-2033-I (Inspector)', station: 'Indiranagar HQ', status: 'Active' },
  { id: '3', name: 'K. Patel', rank: 'BGL-1102-C (Constable)', station: 'Koramangala Unit 2', status: 'Off Duty' }
];

export function Users() {
  const [users, setUsers] = useState(() => {
    const saved = localStorage.getItem('adminUsers');
    return saved ? JSON.parse(saved) : INITIAL_USERS;
  });
  
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);
  const [formData, setFormData] = useState({ name: '', rank: '', station: '', status: 'Active' });

  useEffect(() => {
    localStorage.setItem('adminUsers', JSON.stringify(users));
  }, [users]);

  const filteredUsers = users.filter((u: any) => 
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    u.rank.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.station.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleOpenModal = (user: any = null) => {
    if (user) {
      setEditingUser(user);
      setFormData(user);
    } else {
      setEditingUser(null);
      setFormData({ name: '', rank: '', station: '', status: 'Active' });
    }
    setIsModalOpen(true);
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingUser) {
      setUsers(users.map((u: any) => u.id === editingUser.id ? { ...formData, id: u.id } : u));
    } else {
      setUsers([...users, { ...formData, id: Math.random().toString(36).substr(2, 9) }]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="max-w-[1400px] mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight">User Management</h1>
        <Button className="bg-accent hover:bg-accent-2 text-white transition-all" onClick={() => handleOpenModal()}>
          <UserPlus className="w-4 h-4 mr-2" /> Add Officer
        </Button>
      </div>

      <Card className="shadow-sm border border-line">
        <CardHeader className="border-b border-line bg-surface-2/95 backdrop-blur-md py-4">
          <div className="flex justify-between items-center">
            <CardTitle>Directory</CardTitle>
            <div className="flex items-center bg-surface border border-line px-3 py-1.5 rounded-md w-64 focus-within:ring-2 focus-within:ring-accent-soft focus-within:border-accent transition-all shadow-sm">
              <Search className="w-4 h-4 text-muted mr-2" />
              <input 
                type="text" 
                placeholder="Search officers..." 
                className="bg-transparent border-none outline-none text-sm w-full text-ink" 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {filteredUsers.length === 0 ? (
            <div className="p-8 text-center text-muted">No officers found matching your search.</div>
          ) : (
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-muted uppercase bg-surface border-b border-line">
                <tr>
                  <th className="px-6 py-4">Officer Name</th>
                  <th className="px-6 py-4">ID / Rank</th>
                  <th className="px-6 py-4">Station</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line bg-surface">
                {filteredUsers.map((user: any) => (
                  <tr key={user.id} className="hover:bg-surface-2 transition-colors">
                    <td className="px-6 py-4 font-medium text-ink">{user.name}</td>
                    <td className="px-6 py-4 text-muted">{user.rank}</td>
                    <td className="px-6 py-4 text-ink">{user.station}</td>
                    <td className="px-6 py-4">
                      <Badge variant={user.status === 'Active' ? 'good' : 'warn'}>{user.status}</Badge>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleOpenModal(user)}
                      >
                        Edit
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </CardContent>
      </Card>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
          <Card className="w-full max-w-md shadow-2xl border-line">
            <CardHeader className="flex flex-row justify-between items-center border-b border-line bg-surface-2">
              <CardTitle>{editingUser ? 'Edit Officer' : 'Add New Officer'}</CardTitle>
              <button onClick={() => setIsModalOpen(false)} className="text-muted hover:text-ink transition-colors">
                <X className="w-5 h-5" />
              </button>
            </CardHeader>
            <CardContent className="pt-6">
              <form onSubmit={handleSave} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">Full Name</label>
                  <input required type="text" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">ID / Rank</label>
                  <input required type="text" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.rank} onChange={e => setFormData({...formData, rank: e.target.value})} placeholder="e.g. BGL-1102-C (Constable)" />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">Station Assignment</label>
                  <input required type="text" className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.station} onChange={e => setFormData({...formData, station: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">Status</label>
                  <select className="w-full border border-line rounded-md p-2 text-sm focus:ring-2 focus:ring-accent-soft outline-none bg-surface" value={formData.status} onChange={e => setFormData({...formData, status: e.target.value})}>
                    <option value="Active">Active</option>
                    <option value="Off Duty">Off Duty</option>
                    <option value="Suspended">Suspended</option>
                  </select>
                </div>
                <div className="pt-4 flex space-x-3">
                  <Button type="button" variant="outline" className="flex-1" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" className="flex-1 bg-accent text-white">{editingUser ? 'Save Changes' : 'Create Officer'}</Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
