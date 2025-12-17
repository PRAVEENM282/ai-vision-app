export default function ResultsView({
  imageUrl,
  caption,
}: {
  imageUrl: string;
  caption: string;
}) {
  return (
    <div className="space-y-4">
      <img
        src={imageUrl}
        alt="Uploaded"
        className="max-w-md rounded border"
      />

      <div className="bg-gray-100 p-4 rounded">
        <h3 className="font-semibold">Caption</h3>
        <p>{caption}</p>
      </div>
    </div>
  );
}
