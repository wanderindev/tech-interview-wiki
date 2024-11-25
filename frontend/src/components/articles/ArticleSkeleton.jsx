export default function ArticleSkeleton() {
  return (
    <div className="w-full p-6 bg-[#fcfcfc] shadow-[0px_7px_12px_-10px_rgba(0,0,0,0.2)] rounded-lg animate-pulse">
      {/* Title placeholder */}
      <div className="h-7 bg-gray-200 rounded w-3/4 mb-3"/>

      {/* Excerpt placeholder: two lines */}
      <div className="space-y-2 mb-4">
        <div className="h-4 bg-gray-100 rounded w-full"/>
        <div className="h-4 bg-gray-100 rounded w-5/6"/>
      </div>

      {/* Tags placeholder */}
      <div className="flex flex-wrap gap-2">
        <div className="h-6 w-20 bg-purple-50 rounded-full"/>
        <div className="h-6 w-24 bg-blue-50 rounded-full"/>
        <div className="h-6 w-16 bg-green-50 rounded-full"/>
        <div className="h-6 w-32 bg-gray-100 rounded-full"/>
      </div>
    </div>
  );
}