import {Link} from 'react-router-dom';

export default function Header() {
  return (
    <header className="sticky top-0 bg-white shadow-[0px_7px_12px_-10px_rgba(0,0,0,0.2)] h-[100px]">
      <div className="mx-auto max-w-[1140px] h-full px-4">
        <div className="flex items-center justify-between h-full">
          <Link
            to="/"
            className="font-['M_PLUS_Code_Latin'] text-black text-[20px] font-normal"
          >
            {'{ tech-interview.wiki }'}
          </Link>

          <div className="flex-1 mx-8">
            {/* Filter component will go here */}
          </div>

          <div className="w-[300px]">
            {/* Search component will go here */}
          </div>
        </div>
      </div>
    </header>
  );
}