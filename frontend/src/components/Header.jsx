import { Link, useNavigate } from 'react-router-dom'
import { FileText, LogOut } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Header() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <FileText className="w-8 h-8 text-blue-600" />
          <span className="text-2xl font-bold text-gray-900">AI Resume Analyzer</span>
        </Link>
        <nav className="flex items-center gap-6">
          <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">Home</Link>
          {isAuthenticated ? (
            <>
              <Link to="/analyze" className="text-gray-700 hover:text-blue-600 font-medium">Analyze</Link>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1 text-gray-700 hover:text-red-600 font-medium"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-700 hover:text-blue-600 font-medium">Sign In</Link>
              <Link
                to="/register"
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition-colors"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
