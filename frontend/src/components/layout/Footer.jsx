export default function Footer() {
  return (
    <footer className="mt-[50px] border-t">
      <div className="mx-auto max-w-[1140px] h-[100px] px-4 flex items-center justify-center">
        <p>
          Made with <span className="text-red-500">❤</span> by{' '}
          <a
            href="https://github.com/wanderindev/tech-interview-wiki/tree/main"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 underline"
          >
            Javier Feliu
          </a>
        </p>
      </div>
    </footer>
  );
}