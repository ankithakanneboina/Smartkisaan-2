import { useEffect, useRef, useState } from "react";

// §7: browser Web Speech API only, kept modular so a server-side
// speech API could be swapped in later without touching the chat UI.
const LANG_CODES = { en: "en-IN", te: "te-IN" };

const ERROR_MESSAGES = {
  "not-allowed": "Microphone access was blocked. Allow microphone permission in your browser settings and try again.",
  "no-speech": "Didn't catch that — try speaking again after tapping the mic.",
  "audio-capture": "No microphone found. Check your device's mic is connected.",
  network: "Voice recognition needs an internet connection.",
};

export function useVoice(language) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);
  const [error, setError] = useState("");
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    if (!window.isSecureContext) {
      // Speech APIs only work on https:// or localhost — silently
      // no-op otherwise, so surface that clearly instead of a dead button.
      setSupported(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;
  }, []);

  function startListening(onResult) {
    const recognition = recognitionRef.current;
    if (!recognition) return;
    setError("");
    recognition.lang = LANG_CODES[language] || "en-IN";
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };
    recognition.onerror = (event) => {
      setListening(false);
      setError(ERROR_MESSAGES[event.error] || `Voice input error: ${event.error}`);
    };
    recognition.onend = () => setListening(false);
    try {
      recognition.start();
      setListening(true);
    } catch (err) {
      // Thrown if start() is called while already listening (e.g. a
      // fast double-click) — reset cleanly instead of leaving the
      // button stuck in a broken "listening" state.
      recognition.stop();
      setListening(false);
      setError("Voice input didn't start — try tapping the mic again.");
    }
  }

  function stopListening() {
    recognitionRef.current?.stop();
    setListening(false);
  }

  function speak(text) {
    if (!window.speechSynthesis) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = LANG_CODES[language] || "en-IN";
    window.speechSynthesis.cancel(); // stop anything already playing
    window.speechSynthesis.speak(utterance);
  }

  return { listening, supported, error, startListening, stopListening, speak };
}
