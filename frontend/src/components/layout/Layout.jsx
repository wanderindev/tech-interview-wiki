import Navigation from './Navigation';
import Sidebar from './Sidebar';

export default function Layout({children}) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation/>
      <div className="flex">
        <Sidebar/>
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}