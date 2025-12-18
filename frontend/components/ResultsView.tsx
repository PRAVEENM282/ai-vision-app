export default function ResultsView({
  imageUrl,
  result,
  mode
}: {
  imageUrl: string;
  result: string;
  mode?: string;
}) {
  const getTitle = () => {
    if (mode === "vqa") return "Answer";
    if (mode === "ocr") return "Extracted Text";
    return "Caption";
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
      {/* Image Preview */}
      <div className="border rounded-lg overflow-hidden bg-gray-50 flex items-center justify-center">
        <img
          src={imageUrl}
          alt="Uploaded Analysis"
          className="max-w-full max-h-[400px] object-contain"
        />
      </div>

      {/* Analysis Result */}
      <div className="flex flex-col space-y-3">
        <div className="bg-gray-100 p-5 rounded-lg h-full">
          <h3 className="font-bold text-lg mb-2 text-gray-800 border-b pb-2">
            {getTitle()}
          </h3>
          <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {result}
          </p>
        </div>
      </div>
    </div>
  );
}