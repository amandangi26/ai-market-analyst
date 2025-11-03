import React, { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/Navbar'
import QATool from './components/QATool'
import SummaryTool from './components/SummaryTool'
import ExtractTool from './components/ExtractTool'

function App() {
  const [activeTab, setActiveTab] = useState('qa')
  const [autonomous, setAutonomous] = useState(true)

  const tabs = [
    { id: 'qa', name: 'Q&A Tool', icon: '💬', description: 'Ask questions about documents' },
    { id: 'summary', name: 'Summary Tool', icon: '📝', description: 'Summarize long texts' },
    { id: 'extract', name: 'Extract Tool', icon: '🔍', description: 'Extract structured data' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Navbar />
      <Toaster 
        position="top-right" 
        toastOptions={{
          duration: 3000,
          style: {
            background: '#fff',
            color: '#333',
            borderRadius: '12px',
            padding: '16px',
            boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
          },
          success: {
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Enhanced Tabs */}
        <div className="mb-8">
          <div className="glass-effect rounded-2xl p-2 inline-flex gap-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg scale-105'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-3">
            <span className="text-sm font-semibold text-gray-700">Autonomous Mode</span>
            <button
              onClick={() => setAutonomous(!autonomous)}
              className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${
                autonomous ? 'bg-green-500' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-6 w-6 transform rounded-full bg-white shadow transition-transform ${
                  autonomous ? 'translate-x-7' : 'translate-x-1'
                }`}
              />
            </button>
            <span className="text-xs text-gray-500">When on, queries route to /api/v1/auto</span>
          </div>
        </div>

        {/* Content Card */}
        <div className="glass-effect rounded-3xl shadow-2xl p-8 card-hover">
          {activeTab === 'qa' && <QATool autonomous={autonomous} />}
          {activeTab === 'summary' && <SummaryTool autonomous={autonomous} />} 
          {activeTab === 'extract' && <ExtractTool autonomous={autonomous} />}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>AI Market Analyst • Built with ❤️ By Aman</p>
        </div>
      </div>
    </div>
  )
}

export default App
