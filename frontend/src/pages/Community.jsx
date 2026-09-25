import { useEffect, useState } from "react";
import { getPosts, createPost, toggleLike } from "../services/community";
import FormField from "../components/FormField";
import Card from "../components/Card";
import { Spinner, EmptyState, ErrorState } from "../components/StateComponents";

const inputClass =
  "w-full rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500";

const CATEGORIES = [
  { value: "general", label: "General farming" },
  { value: "crops", label: "Crops" },
  { value: "diseases", label: "Diseases" },
  { value: "fertilizers", label: "Fertilizers" },
  { value: "weather", label: "Weather" },
  { value: "markets", label: "Markets" },
  { value: "government_schemes", label: "Government schemes" },
];

export default function Community() {
  const [posts, setPosts] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", content: "", category: "general" });
  const [posting, setPosting] = useState(false);

  function load() {
    setLoading(true);
    setError("");
    getPosts({ search, category })
      .then(setPosts)
      .catch(() => setError("Couldn't load posts. Check your connection."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [category]);

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  async function handleCreatePost(e) {
    e.preventDefault();
    setPosting(true);
    try {
      await createPost(form);
      setForm({ title: "", content: "", category: "general" });
      setShowForm(false);
      load();
    } finally {
      setPosting(false);
    }
  }

  async function handleLike(post) {
    setPosts((prev) =>
      prev.map((p) =>
        p.id === post.id
          ? { ...p, is_liked: !p.is_liked, like_count: p.like_count + (p.is_liked ? -1 : 1) }
          : p
      )
    );
    await toggleLike(post.id);
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-green-400">Farmer Community</h1>
          <p className="text-gray-500 text-sm mt-1">Ask questions, share what's working.</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="rounded-lg bg-green-600 text-white px-4 py-2 text-sm font-medium hover:bg-green-700 transition"
        >
          {showForm ? "Cancel" : "+ New Post"}
        </button>
      </div>

      {showForm && (
        <Card>
          <form onSubmit={handleCreatePost}>
            <FormField label="Title">
              <input required className={inputClass} value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </FormField>
            <FormField label="Category">
              <select className={inputClass} value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
              </select>
            </FormField>
            <FormField label="What's on your mind?">
              <textarea required rows={3} className={inputClass} value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })} />
            </FormField>
            <button type="submit" disabled={posting}
              className="rounded-lg bg-green-600 text-white px-5 py-2 text-sm font-medium hover:bg-green-700 disabled:opacity-60 transition">
              {posting ? "Posting…" : "Post"}
            </button>
          </form>
        </Card>
      )}

      <div className="flex flex-wrap gap-2">
        <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-[200px]">
          <input className={inputClass + " flex-1"} placeholder="Search posts…"
            value={search} onChange={(e) => setSearch(e.target.value)} />
          <button type="submit" className="rounded-lg bg-leaf-100 text-green-400 px-4 py-2 text-sm font-medium hover:bg-leaf-200 transition">
            Search
          </button>
        </form>
        <select value={category} onChange={(e) => setCategory(e.target.value)} className={inputClass + " w-auto"}>
          <option value="">All categories</option>
          {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
      </div>

      {loading ? (
        <Spinner label="Loading posts…" />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : posts.length === 0 ? (
        <EmptyState icon="💬" title="No posts yet" message="Be the first to ask something." />
      ) : (
        posts.map((post) => (
          <Card key={post.id}>
            <a href={`/community/${post.id}`} className="block">
              <h3 className="font-bold text-gray-100">{post.title}</h3>
              <p className="text-sm text-gray-400 mt-1">{post.content}</p>
            </a>
            <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
              <button onClick={() => handleLike(post)} className={post.is_liked ? "text-red-500" : ""}>
                {post.is_liked ? "❤️" : "🤍"} {post.like_count}
              </button>
              <a href={`/community/${post.id}`} className="hover:underline">💬 {post.comment_count}</a>
              <span className="text-gray-400">— {post.username}</span>
            </div>
          </Card>
        ))
      )}
    </div>
  );
}
