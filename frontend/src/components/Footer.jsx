export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-white mb-4">AI Resume Analyzer</h3>
            <p className="text-sm">Analyze resumes against job descriptions with AI-powered insights.</p>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Features</h4>
            <ul className="text-sm space-y-2">
              <li><a href="#" className="hover:text-blue-400">ATS Score Analysis</a></li>
              <li><a href="#" className="hover:text-blue-400">Skill Gap Detection</a></li>
              <li><a href="#" className="hover:text-blue-400">AI Recommendations</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Contact</h4>
            <p className="text-sm">Email: support@airesume.com</p>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 text-center text-sm">
          <p>&copy; 2024 AI Resume Analyzer. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
