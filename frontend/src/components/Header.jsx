import { Link } from 'react-router-dom'
import { FileText } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <FileText className="w-8 h-8 text-blue-600" />
          <span className="text-2xl font-bold text-gray-900">AI Resume Analyzer</span>
        </Link>
        <nav className="flex gap-6">
          <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">Dashboard</Link>
          <Link to="/analyze" className="text-gray-700 hover:text-blue-600 font-medium">Analyze</Link>
        </nav>
      </div>
    </header>
  )
}
