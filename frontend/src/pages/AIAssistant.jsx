import { useEffect, useRef, useState } from "react";
import { sendChatMessage, getChatHistory } from "../services/aiAssistant";
import { useVoice } from "../hooks/useVoice";
import Card from "../components/Card";

const LABELS = {
  en: {
    problem: "Problem", possible_cause: "Possible cause", recommended_action: "Recommended action",
    precautions: "Precautions", when_to_contact_expert: "When to contact an expert",
    placeholder: "Ask about crops, fertilizer, watering, leaf problems…",
    send: "Send", listening: "Listening…", mic: "🎤 Speak",
  },
  te: {
    problem: "సమస్య", possible_cause: "సాధ్యమైన కారణం", recommended_action: "సిఫార్సు చేసిన చర్య",
    precautions: "జాగ్రత్తలు", when_to_contact_expert: "నిపుణుడిని ఎప్పుడు సంప్రదించాలి",
    placeholder: "పంటలు, ఎరువులు, నీటిపారుదల గురించి అడగండి…",
    send: "పంపండి", listening: "వింటున్నాం…", mic: "🎤 మాట్లాడండి",
  },
};

export default function AIAssistant() {
  const [language, setLanguage] = useState("en");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const { listening, supported, error: voiceError, startListening, stopListening, speak } = useVoice(language);

  const t = LABELS[language];

  useEffect(() => {
    getChatHistory().then(setMessages);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e) {
    e?.preventDefault();
    if (!input.trim()) return;
    const question = input;
    setInput("");
    setLoading(true);
    try {
      const reply = await sendChatMessage(question, language);
      setMessages((prev) => [...prev, reply]);
      const spoken = [
        reply.structured_response.problem,
        reply.structured_response.recommended_action,
      ].filter(Boolean).join(". ");
      speak(spoken);
    } finally {
      setLoading(false);
    }
  }

  function handleMic() {
    if (listening) {
      stopListening();
      return;
    }
    startListening((transcript) => setInput(transcript));
  }

  return (
    <div className="max-w-2xl flex flex-col h-[calc(100vh-8rem)]">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-green-400">AI Farming Assistant</h1>
          <p className="text-gray-500 text-sm mt-1">Ask a farming question, by text or voice.</p>
        </div>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm"
        >
          <option value="en">English</option>
          <option value="te">తెలుగు</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 mb-4 pr-1">
        {messages.map((m) => (
          <div key={m.id} className="space-y-2">
            <div className="flex justify-end">
              <div className="bg-green-600 text-white rounded-2xl rounded-br-sm px-4 py-2 max-w-[80%] text-sm">
                {m.question}
              </div>
            </div>
            <Card className="max-w-[90%]">
              <dl className="text-sm text-gray-400 space-y-1.5">
                <div><dt className="font-medium text-gray-100">{LABELS[m.language]?.problem}</dt><dd>{m.structured_response.problem}</dd></div>
                <div><dt className="font-medium text-gray-100">{LABELS[m.language]?.possible_cause}</dt><dd>{m.structured_response.possible_cause}</dd></div>
                <div><dt className="font-medium text-gray-100">{LABELS[m.language]?.recommended_action}</dt><dd>{m.structured_response.recommended_action}</dd></div>
                {m.structured_response.precautions && (
                  <div><dt className="font-medium text-amber-700">{LABELS[m.language]?.precautions}</dt><dd className="text-amber-700">{m.structured_response.precautions}</dd></div>
                )}
                <div><dt className="font-medium text-gray-100">{LABELS[m.language]?.when_to_contact_expert}</dt><dd>{m.structured_response.when_to_contact_expert}</dd></div>
              </dl>
            </Card>
          </div>
        ))}
        {loading && <p className="text-sm text-green-500">Thinking…</p>}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSend} className="flex flex-col gap-1">
        {voiceError && <p className="text-xs text-red-600 px-1">{voiceError}</p>}
        <div className="flex gap-2">
          <input
            className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
            placeholder={t.placeholder}
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          {supported && (
            <button
              type="button"
              onClick={handleMic}
              className={`rounded-lg px-3 py-2 text-sm font-medium transition ${
                listening ? "bg-red-100 text-red-700" : "bg-leaf-100 text-green-400 hover:bg-leaf-200"
              }`}
            >
              {listening ? t.listening : t.mic}
            </button>
          )}
          <button
            type="submit"
            disabled={loading}
            className="rounded-lg bg-green-600 text-white px-4 py-2 text-sm font-medium hover:bg-green-700 disabled:opacity-60 transition"
          >
            {t.send}
          </button>
        </div>
        {!supported && (
          <p className="text-xs text-gray-400 px-1">
            Voice input isn't available in this browser — try Chrome, or type your question instead.
          </p>
        )}
      </form>
    </div>
  );
}
