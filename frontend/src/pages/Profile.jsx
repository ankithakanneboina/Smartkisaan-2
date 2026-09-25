import { useEffect, useState } from "react";
import { getMyProfile, updateMyProfile, uploadProfilePhoto } from "../services/farmers";
import { getNotificationPreferences, updateNotificationPreferences } from "../services/reminders";
import Card from "../components/Card";

const ic = "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";
const SOIL_TYPES = ["alluvial","black","red","laterite","sandy","clay","loamy"];
const IRRIGATION_TYPES = ["rainfed","canal","borewell","drip","sprinkler"];
const NOTIF_FIELDS = [
  {key:"weather_enabled",label:"Weather alerts"},
  {key:"irrigation_enabled",label:"Irrigation reminders"},
  {key:"fertilizer_enabled",label:"Fertilizer reminders"},
  {key:"crop_calendar_enabled",label:"Crop calendar events"},
  {key:"market_enabled",label:"Market price alerts"},
  {key:"disease_enabled",label:"Disease alerts"},
  {key:"scheme_enabled",label:"Government scheme updates"},
];

export default function Profile() {
  const [form, setForm] = useState(null);
  const [prefs, setPrefs] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [photoUploading, setPhotoUploading] = useState(false);

  useEffect(() => {
    Promise.all([getMyProfile(), getNotificationPreferences()])
      .then(([p, pr]) => { setForm(p); setPrefs(pr); })
      .finally(() => setLoading(false));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault(); setSaving(true); setSaved(false);
    try { const u = await updateMyProfile(form); setForm(u); setSaved(true); }
    finally { setSaving(false); }
  }

  async function handlePhotoChange(e) {
    const file = e.target.files?.[0]; if (!file) return;
    setPhotoUploading(true);
    try { const u = await uploadProfilePhoto(file); setForm(p => ({ ...p, profile_photo: u.profile_photo })); }
    finally { setPhotoUploading(false); }
  }

  async function handlePrefToggle(key) {
    const updated = { ...prefs, [key]: !prefs[key] };
    setPrefs(updated);
    await updateNotificationPreferences({ [key]: updated[key] });
  }

  if (loading) return <div className="text-green-400">Loading…</div>;
  if (!form) return <div className="text-red-400">Failed to load profile.</div>;

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-green-400">My Farm Profile</h1>

      <Card>
        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 rounded-full bg-gray-700 overflow-hidden flex items-center justify-center text-2xl">
            {form.profile_photo ? <img src={form.profile_photo} alt="Profile" className="w-full h-full object-cover" /> : "👤"}
          </div>
          <label className="text-sm text-green-400 font-medium cursor-pointer">
            {photoUploading ? "Uploading…" : "Change photo"}
            <input type="file" accept="image/*" className="hidden" disabled={photoUploading} onChange={handlePhotoChange} />
          </label>
        </div>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
          {[["Full name","full_name","text"],["Mobile number","mobile_number","text"],["Location","location","text"],["District","district","text"],["State","state","text"]].map(([label,key,type]) => (
            <label key={key} className="block mb-4">
              <span className="block text-sm font-medium text-gray-300 mb-1">{label}</span>
              <input type={type} className={ic} value={form[key] || ""} onChange={e => setForm({...form,[key]:e.target.value})} />
            </label>
          ))}
          <label className="block mb-4">
            <span className="block text-sm font-medium text-gray-300 mb-1">Land area (acres)</span>
            <input type="number" step="0.01" className={ic} value={form.land_area_acres ?? ""} onChange={e => setForm({...form,land_area_acres:e.target.value})} />
          </label>
          <label className="block mb-4">
            <span className="block text-sm font-medium text-gray-300 mb-1">Soil type</span>
            <select className={ic} value={form.soil_type || ""} onChange={e => setForm({...form,soil_type:e.target.value})}>
              <option value="">Select</option>
              {SOIL_TYPES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block mb-4">
            <span className="block text-sm font-medium text-gray-300 mb-1">Irrigation type</span>
            <select className={ic} value={form.irrigation_type || ""} onChange={e => setForm({...form,irrigation_type:e.target.value})}>
              <option value="">Select</option>
              {IRRIGATION_TYPES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block mb-4">
            <span className="block text-sm font-medium text-gray-300 mb-1">Language</span>
            <select className={ic} value={form.preferred_language || "en"} onChange={e => setForm({...form,preferred_language:e.target.value})}>
              <option value="en">English</option>
              <option value="te">Telugu</option>
            </select>
          </label>
          <div className="sm:col-span-2 mt-2">
            {saved && <p className="text-sm text-green-400 mb-3">Profile saved.</p>}
            <button type="submit" disabled={saving}
              className="rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
              {saving ? "Saving…" : "Save changes"}
            </button>
          </div>
        </form>
      </Card>

      {prefs && (
        <Card title="Notification preferences">
          <div className="space-y-3">
            {NOTIF_FIELDS.map(f => (
              <div key={f.key} className="flex items-center justify-between">
                <span className="text-sm text-gray-300">{f.label}</span>
                <button onClick={() => handlePrefToggle(f.key)}
                  className={`relative w-10 h-5 rounded-full transition ${prefs[f.key] ? "bg-green-600" : "bg-gray-600"}`}>
                  <span className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${prefs[f.key] ? "translate-x-5" : "translate-x-0.5"}`} />
                </button>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
