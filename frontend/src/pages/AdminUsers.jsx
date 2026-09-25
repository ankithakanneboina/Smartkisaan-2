import { useEffect, useState } from "react";
import api from "../services/api";
import Card from "../components/Card";
import { Spinner } from "../components/StateComponents";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [roleFilter, setRoleFilter] = useState("");
  const [loading, setLoading] = useState(true);
  function load() {
    setLoading(true);
    api.get(`/auth/admin/users/${roleFilter ? "?role="+roleFilter : ""}`).then(r => setUsers(r.data.results ?? r.data)).catch(()=>{}).finally(() => setLoading(false));
  }
  useEffect(() => { load(); }, [roleFilter]);
  async function handleDelete(id) { if (!window.confirm("Delete?")) return; await api.delete(`/auth/admin/users/${id}/`); load(); }
  async function handleRoleChange(id, role) { await api.put(`/auth/admin/users/${id}/`, { role }); load(); }
  return (
    <div className="max-w-3xl space-y-4">
      <h1 className="text-2xl font-bold text-green-400">👥 User Management</h1>
      <div className="flex gap-2">
        {["","farmer","buyer","admin"].map(r => (
          <button key={r} onClick={() => setRoleFilter(r)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition ${roleFilter===r?"bg-green-600 text-white":"bg-gray-700 text-gray-300 hover:bg-gray-600"}`}>
            {r||"All"}
          </button>
        ))}
      </div>
      {loading ? <Spinner /> : (
        <Card>
          <table className="w-full text-sm">
            <thead><tr className="text-left text-gray-500 border-b border-gray-700">
              <th className="pb-2">Email</th><th className="pb-2">Role</th><th className="pb-2">Actions</th>
            </tr></thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} className="border-b border-gray-700 last:border-0">
                  <td className="py-2 text-gray-300">{u.email}</td>
                  <td className="py-2">
                    <select value={u.role} onChange={e => handleRoleChange(u.id, e.target.value)}
                      className="text-xs bg-gray-700 border border-gray-600 text-gray-200 rounded px-1 py-0.5">
                      <option value="buyer">buyer</option><option value="farmer">farmer</option><option value="admin">admin</option>
                    </select>
                  </td>
                  <td className="py-2"><button onClick={() => handleDelete(u.id)} className="text-xs text-red-400 hover:underline">Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          {users.length === 0 && <p className="text-sm text-gray-500 py-4">No users found.</p>}
        </Card>
      )}
    </div>
  );
}
