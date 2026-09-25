import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPost, addComment, toggleLike, reportPost } from "../services/community";
import Card from "../components/Card";

export default function CommunityPostDetail() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [comment, setComment] = useState("");
  const [posting, setPosting] = useState(false);
  const [reported, setReported] = useState(false);

  function load() {
    getPost(id).then(setPost);
  }

  useEffect(() => {
    load();
  }, [id]);

  async function handleComment(e) {
    e.preventDefault();
    if (!comment.trim()) return;
    setPosting(true);
    try {
      await addComment(id, comment);
      setComment("");
      load();
    } finally {
      setPosting(false);
    }
  }

  async function handleLike() {
    setPost((prev) => ({
      ...prev,
      is_liked: !prev.is_liked,
      like_count: prev.like_count + (prev.is_liked ? -1 : 1),
    }));
    await toggleLike(id);
  }

  async function handleReport() {
    await reportPost(id, "Reported by user");
    setReported(true);
  }

  if (!post) return <p className="text-leaf-600">Loading…</p>;

  return (
    <div className="max-w-2xl space-y-4">
      <Card>
        <h1 className="text-xl font-bold text-gray-800">{post.title}</h1>
        <p className="text-sm text-gray-600 mt-2">{post.content}</p>
        <div className="flex items-center gap-4 mt-4 text-sm text-gray-500">
          <button onClick={handleLike} className={post.is_liked ? "text-red-500" : ""}>
            {post.is_liked ? "❤️" : "🤍"} {post.like_count}
          </button>
          <span className="text-gray-400">— {post.username}</span>
          {!reported ? (
            <button onClick={handleReport} className="ml-auto text-xs text-gray-400 hover:text-red-500">
              🚩 Report
            </button>
          ) : (
            <span className="ml-auto text-xs text-gray-400">Reported — thanks</span>
          )}
        </div>
      </Card>

      <Card title={`Comments (${post.comments?.length || 0})`}>
        <div className="space-y-3 mb-4">
          {post.comments?.map((c) => (
            <div key={c.id} className="text-sm">
              <span className="font-medium text-gray-700">{c.username}</span>
              <span className="text-gray-400"> — </span>
              <span className="text-gray-600">{c.content}</span>
            </div>
          ))}
          {(!post.comments || post.comments.length === 0) && (
            <p className="text-sm text-gray-500">No comments yet.</p>
          )}
        </div>
        <form onSubmit={handleComment} className="flex gap-2">
          <input
            className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
            placeholder="Add a comment…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
          <button type="submit" disabled={posting}
            className="rounded-lg bg-leaf-600 text-white px-4 py-2 text-sm font-medium hover:bg-leaf-700 disabled:opacity-60 transition">
            Reply
          </button>
        </form>
      </Card>
    </div>
  );
}
