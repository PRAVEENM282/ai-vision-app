"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ResultsView from "@/components/ResultsView";
import Toast from "@/components/Toast";

export default function UploadPage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">
        AI Vision App
      </h1>

      <UploadForm
        onResult={setData}
        onError={setError}
      />

      {data && (
        <ResultsView
          imageUrl={data.imageUrl}
          result={data.result} 
          mode={data.mode}     
        />
      )}

      <Toast
        message={error}
        onClose={() => setError("")}
      />
    </main>
  );
}