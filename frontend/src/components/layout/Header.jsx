import {Link} from 'react-router-dom';

export default function Header() {
  return (
    <header className="sticky top-0 bg-white shadow-[0px_7px_12px_-10px_rgba(0,0,0,0.2)] h-[100px]">
      <div className="mx-auto max-w-[1140px] h-full px-4 flex items-center justify-center">
        <Link
          to="/"
          className="font-['M_PLUS_Code_Latin'] text-black text-[20px] font-normal whitespace-nowrap"
        >
          {'{ tech-interview.wiki }'}
        </Link>
      </div>
    </header>
  );
}