import React, { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

function ExtractTool({ autonomous = true }) {
  const [text, setText] = useState('')
  const [schema, setSchema] = useState('')
  const [extracted, setExtracted] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const exampleSchema = {
    "company": "string",
    "revenue": "number",
    "period": "string",
    "competitors": "array"
  }

  const marketResearchSchema = {
    "company": "string",
    "revenue": "number",
    "period": "string",
    "competitors": "array",
    "market_share": "string"
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    
    if (!text.trim()) {
      toast.error('Please enter text to extract from')
      setError('Text field is required')
      return
    }

    if (!schema.trim()) {
      toast.error('Please enter a JSON schema')
      setError('JSON schema is required')
      return
    }

    let parsedSchema
    try {
      parsedSchema = JSON.parse(schema)
      
      // Validate schema is an object
      if (typeof parsedSchema !== 'object' || Array.isArray(parsedSchema)) {
        throw new Error('Schema must be a JSON object')
      }
    } catch (error) {
      const errorMsg = error.message || 'Invalid JSON schema'
      toast.error(errorMsg)
      setError(errorMsg)
      return
    }

    setLoading(true)
    setExtracted(null)
    setError(null)

    try {
      const endpoint = autonomous ? '/api/v1/auto' : '/api/v1/extract'
      const payload = autonomous ? { text: text, schema: parsedSchema } : { text: text, schema: parsedSchema }
      const response = await axios.post(endpoint, payload)

      if (autonomous) {
        if (response.data && response.data.result && response.data.result.data) {
          setExtracted(response.data.result.data)
          toast.success('Data extracted successfully!')
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        if (response.data && response.data.data) {
          setExtracted(response.data.data)
          toast.success('Data extracted successfully!')
        } else {
          throw new Error('Invalid response format')
        }
      }
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to extract data'
      toast.error(errorMsg)
      setError(errorMsg)
      setExtracted({ error: errorMsg })
    } finally {
      setLoading(false)
    }
  }

  const handleLoadExample = (type = 'basic') => {
    const schemaToLoad = type === 'market' ? marketResearchSchema : exampleSchema
    setSchema(JSON.stringify(schemaToLoad, null, 2))
    if (type === 'market') {
      setText('Innovate Inc. reported $12 million in revenue for Q3 2025. Competitors include FutureFlow and Synergy Systems. Innovate Inc. holds a 12% market share.')
    }
    toast.success('Example loaded')
  }

  const handleClear = () => {
    setText('')
    setSchema('')
    setExtracted(null)
    setError(null)
    toast.success('Cleared')
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl mb-4 shadow-lg">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Extract Tool</h2>
        <p className="text-gray-600 text-lg">
          Extract structured JSON data from unstructured text using AI
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <label htmlFor="text" className="block text-sm font-semibold text-gray-700">
            Text to Extract From
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => {
              setText(e.target.value)
              setError(null)
            }}
            placeholder="Enter unstructured text here..."
            className={`w-full px-5 py-4 border-2 rounded-xl focus:ring-2 focus:ring-emerald-500 transition-all duration-200 resize-none text-gray-800 placeholder-gray-400 font-mono text-sm min-h-[150px] ${
              error && !text.trim() ? 'border-red-300' : 'border-gray-200 focus:border-emerald-500'
            }`}
            rows="6"
            disabled={loading}
          />
          {error && !text.trim() && (
            <p className="text-sm text-red-600 flex items-center space-x-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span>This field is required</span>
            </p>
          )}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between mb-2">
            <label htmlFor="schema" className="block text-sm font-semibold text-gray-700">
              JSON Schema
            </label>
            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => handleLoadExample('basic')}
                className="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-all duration-200 text-xs font-semibold border border-emerald-200"
              >
                Basic Example
              </button>
              <button
                type="button"
                onClick={() => handleLoadExample('market')}
                className="px-3 py-1.5 bg-teal-50 text-teal-700 rounded-lg hover:bg-teal-100 transition-all duration-200 text-xs font-semibold border border-teal-200"
              >
                Market Research
              </button>
              {(text || schema) && (
                <button
                  type="button"
                  onClick={handleClear}
                  className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all duration-200 text-xs font-semibold"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
          <textarea
            id="schema"
            value={schema}
            onChange={(e) => {
              setSchema(e.target.value)
              setError(null)
            }}
            placeholder='{"field1": "string", "field2": "number"}'
            className={`w-full px-5 py-4 border-2 rounded-xl focus:ring-2 focus:ring-emerald-500 transition-all duration-200 resize-none text-gray-800 placeholder-gray-400 font-mono text-sm min-h-[200px] ${
              error && !schema.trim() ? 'border-red-300' : 'border-gray-200 focus:border-emerald-500'
            }`}
            rows="10"
            disabled={loading}
          />
          {error && !schema.trim() && (
            <p className="text-sm text-red-600 flex items-center space-x-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span>This field is required</span>
            </p>
          )}
          {schema && !error && (
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Valid JSON format</span>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-xl hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Extracting Data...
            </span>
          ) : (
            'Extract Structured Data'
          )}
        </button>
      </form>

      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-8 h-8 bg-emerald-100 rounded-full"></div>
            </div>
          </div>
          <p className="text-gray-600 font-medium">Processing extraction with AI...</p>
        </div>
      )}

      {extracted && !loading && (
        <div className="mt-8 animate-fade-in">
          {extracted.error ? (
            <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6">
              <div className="flex items-center space-x-2 mb-2">
                <svg className="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <h3 className="text-xl font-bold text-red-900">Extraction Error</h3>
              </div>
              <p className="text-red-700">{extracted.error}</p>
              {extracted.raw && (
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm text-red-600 font-medium">Show raw response</summary>
                  <pre className="mt-2 p-3 bg-red-100 rounded-lg text-xs overflow-auto max-h-40">{extracted.raw}</pre>
                </details>
              )}
            </div>
          ) : (
            <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-6 border-2 border-emerald-100">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">Extracted Data</h3>
                </div>
                <span className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-semibold">
                  {Object.keys(extracted).length} fields
                </span>
              </div>
              <div className="bg-white rounded-xl p-5 border border-gray-200 overflow-hidden">
                <pre className="text-sm text-gray-800 overflow-x-auto">
                  {JSON.stringify(extracted, null, 2)}
                </pre>
              </div>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(extracted, null, 2))
                  toast.success('Copied to clipboard!')
                }}
                className="mt-4 w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all duration-200 font-medium text-sm"
              >
                📋 Copy JSON to Clipboard
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ExtractTool
