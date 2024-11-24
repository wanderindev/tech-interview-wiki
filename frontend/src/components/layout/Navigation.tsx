import {Link} from 'react-router-dom';

export default function Navigation() {
    return (
        <nav className="bg-white shadow-md">
            <div className="mx-auto max-w-7xl px-4">
                <div className="flex h-16 justify-between">
                    <div className="flex">
                        <Link to="/" className="flex items-center px-2 text-xl font-semibold text-gray-900">
                            Tech Interview Wiki
                        </Link>
                    </div>
                    {/* Add search bar or other navigation items later */}
                </div>
            </div>
        </nav>
    );
}