import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);
  const [total, setTotal] = useState(0);

  const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
  });

  const fetchHistory = async () => {
    const res = await api.get("/api/urls/");
    setHistory(res.data.items);      // not res.data
    setTotal(res.data.total);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;
    try {
      const res = await api.post("/api/urls/", { url });
      setLatest(res.data.latest);    // not res.data
      setTotal(res.data.total);
      setUrl("");
      fetchHistory();
    } catch (err) {
      console.error("POST error", err.response?.status, err.response?.data || err.message);
    }
  };

  const handleSelect = (e) => {
    const id = e.target.value;
    const item = history.find((h) => String(h.id) === id);
    setLatest(item || null);
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", padding: 40 }}>
      <div style={{ display: "grid", gridTemplateColumns: "260px 480px", gap: 40 }}>
        <div style={{ border: "1px solid #ddd", borderRadius: 6, padding: 16 }}>
          <h3>Previous links</h3>
          <select
            style={{ width: "100%", padding: 6, marginTop: 8 }}
            onChange={handleSelect}
          >
            <option value="">Choose…</option>
            {history.map((item) => (
              <option key={item.id} value={item.id}>
                {item.slug} – {item.url.slice(0, 40)}
                {item.url.length > 40 ? "…" : ""}
              </option>
            ))}
          </select>
          <div style={{ marginTop: 12 }}>
            <b>Total shortened:</b> {total}
          </div>
        </div>

        <div style={{ border: "1px solid #ddd", borderRadius: 6, padding: 16 }}>
          <h1 style={{ textAlign: "center" }}>URL Shortener</h1>
          <form onSubmit={handleSubmit}>
            <label>
              Original URL:
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                style={{ width: "100%", padding: 8, margin: "8px 0" }}
                required
              />
            </label>
            <button className="button-shorten" type="submit">Shorten</button>
          </form>

          {latest && (
            <div style={{ marginTop: 16, fontSize: 14 }}>
              <h3>Selected / new link</h3>
              <div><b>Original:</b> {latest.url}</div>
              <div>
                <b>Short:</b>{" "}
                <a href={latest.short_url} target="_blank" rel="noreferrer">
                  {latest.short_url}
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
