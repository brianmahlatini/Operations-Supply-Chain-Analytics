const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8002/api";

export async function getJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}
