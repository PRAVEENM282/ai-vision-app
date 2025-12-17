const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api";

export async function uploadImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  return res.json();
}

export async function analyzeCaption(assetId: string) {
  const res = await fetch(
    `${API_BASE}/analyze/caption?asset_id=${assetId}`,
    { method: "POST" }
  );

  if (!res.ok) {
    throw new Error("Caption analysis failed");
  }

  return res.json();
}

export async function getAnalysisResult(
  assetId: string,
  featureType: "caption"
) {
  const res = await fetch(
    `${API_BASE}/analyze/result?asset_id=${assetId}&feature_type=${featureType}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch analysis result");
  }

  return res.json();
}
