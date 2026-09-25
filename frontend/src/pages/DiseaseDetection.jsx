import { useState } from "react";
import { detectDisease } from "../services/diseases";
import FormField from "../components/FormField";
import Card from "../components/Card";

const inputClass =
  "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";

export default function DiseaseDetection() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [cropHint, setCropHint] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleFileChange(e) {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) {
      setError("Please choose a leaf/plant image first.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await detectDisease(file, cropHint);
      setResult(data);
    } catch (err) {
      setError(
        err.response?.data?.image?.[0] ||
          "Couldn't process that image. Try a smaller JPEG or PNG file."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Plant Disease Detection</h1>
        <p className="text-gray-500 text-sm mt-1">
          Upload a photo of an affected leaf or plant.
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <FormField label="Crop (optional)">
            <input
              className={inputClass}
              value={cropHint}
              onChange={(e) => setCropHint(e.target.value)}
              placeholder="e.g. cotton, rice"
            />
          </FormField>

          <label className="block mb-4">
            <span className="block text-sm font-medium text-green-400 mb-1">Leaf/plant photo</span>
            <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleFileChange}
              className="block w-full text-sm text-gray-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:bg-leaf-100 file:text-green-400 file:font-medium" />
          </label>

          {preview && (
            <img src={preview} alt="Preview" className="w-40 h-40 object-cover rounded-lg border border-leaf-100 mb-4" />
          )}

          {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

          <button type="submit" disabled={loading}
            className="rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {loading ? "Analyzing…" : "Detect Disease"}
          </button>
        </form>
      </Card>

      {result && (
        <Card>
          {result.status === "unavailable" && (
            <div className="text-sm text-gray-400 space-y-2">
              <p className="font-medium text-amber-700">
                🔬 Automatic disease detection isn't available yet.
              </p>
              <p>
                Your photo was saved to your history. This feature needs a trained image-recognition
                model, which hasn't been built yet — we're not going to guess a diagnosis and risk
                giving you wrong advice.
              </p>
              <p>
                In the meantime, browse the{" "}
                <a href="/diseases/reference" className="text-green-500 underline">
                  known disease reference guide
                </a>{" "}
                to compare symptoms yourself, or contact your local agriculture extension officer.
              </p>
            </div>
          )}
          {result.status === "success" && (
            <div>
              <h3 className="font-bold text-gray-100">{result.predicted_disease}</h3>
              <p className="text-sm text-gray-500 mt-1">
                Confidence: {Math.round(result.confidence * 100)}%
              </p>
            </div>
          )}
          {result.status === "failed" && (
            <p className="text-sm text-red-600">
              Something went wrong processing that image. Please try again.
            </p>
          )}
        </Card>
      )}
    </div>
  );
}
