import Header from './Header';
import Footer from './Footer';

export default function Layout({children}) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header/>
      <main className="mx-auto max-w-[1140px] px-4 flex-1">
        {children}
      </main>
      <Footer/>
    </div>
  );
}