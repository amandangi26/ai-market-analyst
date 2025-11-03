import React, { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

function SummaryTool({ autonomous = true }) {
  const [text, setText] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!text.trim()) {
      toast.error('Please enter text to summarize')
      return
    }

    setLoading(true)
    setSummary('')

    try {
      const endpoint = autonomous ? '/api/v1/auto' : '/api/v1/summary'
      const payload = autonomous ? { text } : { text: text, max_length: 500 }
      const response = await axios.post(endpoint, payload)

      if (autonomous) {
        const route = response.data.route
        if (route === 'summary') {
          setSummary(response.data.result.summary)
        } else if (route === 'qa') {
          setSummary(response.data.result.answer)
        } else if (route === 'extract') {
          setSummary(JSON.stringify(response.data.result.data, null, 2))
        } else {
          setSummary('Unknown route response')
        }
      } else {
        setSummary(response.data.summary)
      }
      toast.success('Summary generated successfully!')
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to generate summary'
      toast.error(errorMsg)
      setSummary('Error: ' + errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (!file) return

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      toast.error('File size exceeds 5MB limit')
      return
    }

    const reader = new FileReader()
    reader.onload = (event) => {
      setText(event.target.result)
      toast.success('File loaded successfully!')
    }
    reader.onerror = () => {
      toast.error('Failed to read file')
    }
    reader.readAsText(file)
  }

  const handleClear = () => {
    setText('')
    setSummary('')
    toast.success('Cleared')
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl mb-4 shadow-lg">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Summary Tool</h2>
        <p className="text-gray-600 text-lg">
          Generate concise summaries from long documents using AI
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label htmlFor="text" className="block text-sm font-semibold text-gray-700">
              Text to Summarize
            </label>
            <div className="flex items-center space-x-2">
              <label className="px-4 py-2 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 rounded-lg hover:from-purple-200 hover:to-pink-200 cursor-pointer transition-all duration-200 font-medium text-sm border border-purple-200">
                <input
                  type="file"
                  accept=".txt,.md"
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={loading}
                />
                📁 Upload File
              </label>
              {text && (
                <button
                  type="button"
                  onClick={handleClear}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all duration-200 font-medium text-sm"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your text here or upload a file..."
            className="w-full px-5 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 resize-none text-gray-800 placeholder-gray-400 min-h-[200px]"
            rows="12"
            disabled={loading}
          />
          {text && (
            <p className="text-xs text-gray-500 text-right">
              {text.length.toLocaleString()} characters
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating Summary...
            </span>
          ) : (
            'Generate Summary'
          )}
        </button>
      </form>

      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-8 h-8 bg-purple-100 rounded-full"></div>
            </div>
          </div>
          <p className="text-gray-600 font-medium">Processing your text...</p>
        </div>
      )}

      {summary && !loading && (
        <div className="mt-8 animate-fade-in">
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border-2 border-purple-100">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900">Summary</h3>
              <span className="ml-auto px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
                {summary.split(' ').length} words
              </span>
            </div>
            <div className="bg-white rounded-xl p-5 border border-gray-200">
              <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{summary}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SummaryTool
