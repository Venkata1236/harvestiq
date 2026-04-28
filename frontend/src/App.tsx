import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Upload from './pages/Upload'
import Results from './pages/Results'
import History from './pages/History'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Navbar */}
        <nav className="bg-green-700 text-white px-6 py-4 flex items-center gap-8 shadow">
          <span className="text-xl font-bold tracking-tight">🌿 HarvestIQ</span>
          <NavLink to="/" className={({ isActive }) => isActive ? "font-semibold underline" : "hover:underline"}>
            Detect
          </NavLink>
          <NavLink to="/history" className={({ isActive }) => isActive ? "font-semibold underline" : "hover:underline"}>
            History
          </NavLink>
        </nav>

        {/* Pages */}
        <main className="max-w-3xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/results" element={<Results />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}