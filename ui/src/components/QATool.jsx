import React, { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

function QATool() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sourceDocs, setSourceDocs] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!question.trim()) {
      toast.error('Please enter a question')
      return
    }

    setLoading(true)
    setAnswer('')
    setSourceDocs([])

    try {
      const response = await axios.post('/api/v1/qa', {
        question: question
      })

      setAnswer(response.data.answer)
      setSourceDocs(response.data.source_documents || [])
      toast.success('Question answered successfully!')
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to get answer'
      toast.error(errorMsg)
      setAnswer('Error: ' + errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl mb-4 shadow-lg">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Q&A Tool</h2>
        <p className="text-gray-600 text-lg">
          Ask questions about your documents using advanced RAG pipeline
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <label htmlFor="question" className="block text-sm font-semibold text-gray-700">
            Your Question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What is the company name? What are the key revenue figures?"
            className="w-full px-5 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 resize-none text-gray-800 placeholder-gray-400"
            rows="4"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : (
            'Ask Question'
          )}
        </button>
      </form>

      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-8 h-8 bg-blue-100 rounded-full"></div>
            </div>
          </div>
          <p className="text-gray-600 font-medium">Analyzing documents and generating answer...</p>
        </div>
      )}

      {answer && !loading && (
        <div className="mt-8 space-y-6 animate-fade-in">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-100">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900">Answer</h3>
            </div>
            <div className="bg-white rounded-xl p-5 border border-gray-200">
              <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{answer}</p>
            </div>
          </div>

          {sourceDocs.length > 0 && (
            <div className="bg-gray-50 rounded-2xl p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">
                  Source Documents
                </h3>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                  {sourceDocs.length} {sourceDocs.length === 1 ? 'source' : 'sources'}
                </span>
              </div>
              <div className="space-y-3">
                {sourceDocs.map((doc, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-xl border border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <span className="text-indigo-600 font-bold text-sm">{idx + 1}</span>
                      </div>
                      <p className="text-gray-700 text-sm leading-relaxed flex-1">{doc.page_content}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default QATool
