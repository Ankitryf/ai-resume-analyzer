import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import AnalyzeResume from './pages/AnalyzeResume'
import Results from './pages/Results'
import Header from './components/Header'
import Footer from './components/Footer'

export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <Header />
        <main className="flex-1 container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<AnalyzeResume />} />
            <Route path="/results/:analysisId" element={<Results />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}
