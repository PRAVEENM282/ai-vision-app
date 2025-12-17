"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ResultsView from "@/components/ResultsView";
import Toast from "@/components/Toast";

export default function UploadPage() {
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">
        AI Vision App
      </h1>

      <UploadForm
        onResult={setResult}
        onError={setError}
      />

      {result && (
        <ResultsView
          imageUrl={result.imageUrl}
          caption={result.caption}
        />
      )}

      <Toast
        message={error}
        onClose={() => setError("")}
      />
    </main>
  );
}
