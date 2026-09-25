import { useEffect, useState } from "react";
import { getDiseaseCatalog } from "../services/diseases";
import Card from "../components/Card";

export default function DiseaseReference() {
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDiseaseCatalog().then(setDiseases).finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Disease Reference Guide</h1>
        <p className="text-gray-500 text-sm mt-1">
          Browse known crop diseases and compare symptoms yourself.
        </p>
      </div>

      {loading && <p className="text-green-500">Loading…</p>}

      {diseases.map((d) => (
        <Card key={d.id} title={`${d.name}${d.crop_name ? ` — ${d.crop_name}` : ""}`}>
          <dl className="text-sm text-gray-400 space-y-2">
            <div><dt className="font-medium text-gray-700">Symptoms</dt><dd>{d.symptoms}</dd></div>
            <div><dt className="font-medium text-gray-700">Possible causes</dt><dd>{d.possible_causes}</dd></div>
            <div><dt className="font-medium text-gray-700">Recommended actions</dt><dd>{d.recommended_actions}</dd></div>
            <div><dt className="font-medium text-gray-700">Prevention</dt><dd>{d.prevention_methods}</dd></div>
          </dl>
        </Card>
      ))}
    </div>
  );
}
