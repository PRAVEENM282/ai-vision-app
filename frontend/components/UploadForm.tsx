"use client";

import { useState } from "react";
import {
  uploadImage,
  analyzeCaption,
  getAnalysisResult,
} from "@/lib/api";

export default function UploadForm({
  onResult,
  onError,
}: {
  onResult: (data: any) => void;
  onError: (msg: string) => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  }

  async function handleSubmit() {
    if (!file) {
      onError("Please select an image");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      onError("File too large (max 5MB)");
      return;
    }

    try {
      setLoading(true);
      setStatus("Uploading image...");

      const uploadRes = await uploadImage(file);

      onResult({
        imageUrl: uploadRes.image_url,
        caption: "Processing...",
      });

      setStatus("Analyzing image...");
      await analyzeCaption(uploadRes.asset_id);
      let attempts = 0;
      const interval = setInterval(async () => {
        attempts += 1;
        if (attempts > 10) {
          clearInterval(interval);
          onError("AI service  busy please try again later");
            setLoading(false);
            return;
        }
        const res = await getAnalysisResult(
          uploadRes.asset_id,
          "caption"
        );

        if (res.status === "completed") {
          clearInterval(interval);
          onResult({
            imageUrl: uploadRes.image_url,
            caption: res.result.text,
          });
          setLoading(false);
          setStatus("");
        }

        if (res.status === "failed") {
          clearInterval(interval);
          onError(res.error);
          setLoading(false);
          setStatus("");
        }
      }, 10000);
    } catch {
      onError("Unexpected error occurred");
      setLoading(false);
      setStatus("");
    }
  }

  return (
    <div className="border p-6 rounded-lg space-y-4">
      <div
        className="border-dashed border-2 p-6 rounded text-center"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        {file ? file.name : "Drag & drop image here"}
      </div>

      <input
        type="file"
        accept="image/*"
        onChange={(e) =>
          setFile(e.target.files?.[0] || null)
        }
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-black text-white px-4 py-2 rounded"
      >
        Submit
      </button>

      {loading && (
        <p className="text-sm text-gray-600">{status}</p>
      )}
    </div>
  );
}
