import {PrismLight as SyntaxHighlighter} from 'react-syntax-highlighter';
import {oneDark} from 'react-syntax-highlighter/dist/esm/styles/prism';
import {useState} from 'react';

export default function CodeBlock({node, inline, className, children, ...props}) {
  const [copied, setCopied] = useState(false);
  const code = String(children).replace(/\n$/, '');
  const match = /language-(\w+)/.exec(className || '');

  const copyCode = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!inline && match) {
    return (
      <div className="relative">
        <button
          onClick={copyCode}
          className="absolute right-2 top-2 p-2 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
          aria-label="Copy code"
        >
          {copied ? (
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                 stroke="white" strokeWidth="2">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                 stroke="white" strokeWidth="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          )}
        </button>
        <SyntaxHighlighter
          style={oneDark}
          language={match[1]}
          PreTag="div"
          className="rounded-lg my-4"
          {...props}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    );
  }

  return <code className={className} {...props}>{children}</code>;
}