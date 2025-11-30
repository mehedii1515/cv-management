'use client'

import { useState, useEffect, useCallback } from 'react'

// DTSearch API Response Types
export interface DTSearchHit {
  id: string
  score: number
  name: string
  email: string
  phone: string
  location: string
  current_employer: string
  years_of_experience: number
  skills: string
  experience: string
  summary: string
  highlights: {
    [key: string]: string[]
  }
}

export interface DTSearchResult {
  hits: DTSearchHit[]
  total_hits: number
  max_score: number
  took: number
  pagination?: {
    current_page: number
    page_size: number
    has_next: boolean
    has_previous: boolean
  }
  search_info?: {
    query: string
    search_type?: string
    operators_detected?: string[]
    filters_applied?: any
    search_time_ms: number
  }
}

export interface DTSearchFilters {
  location?: string[]
  skills?: string[]
  experience_range?: [number, number]
  current_employer?: string[]
}

interface DTSearchResponse {
  hits: DTSearchHit[]
  total_hits: number
  max_score: number
  took: number
  pagination?: {
    current_page: number
    page_size: number
    has_next: boolean
    has_previous: boolean
  }
  search_info?: {
    query: string
    search_type?: string
    operators_detected?: string[]
    filters_applied?: any
    search_time_ms: number
  }
}

interface DTSearchSuggestion {
  suggestions: string[]
}

interface DTSearchStatus {
  elasticsearch_connected: boolean
  search_service_ready: boolean
  index_name: string
  document_count: number
  index_size: number
}

// Search Options
interface DTSearchOptions {
  searchMode: 'basic' | 'boolean' | 'suggestions'
  page: number
  pageSize: number
  enableHighlighting: boolean
  enableCaching: boolean
}

// Hook State
interface DTSearchState {
  // Search Results
  results: DTSearchHit[]
  totalHits: number
  maxScore: number
  searchTime: number
  
  // Search Info
  query: string
  searchMode: 'basic' | 'boolean' | 'suggestions'
  suggestions: string[]
  
  // Pagination
  currentPage: number
  pageSize: number
  hasNext: boolean
  hasPrevious: boolean
  
  // Status
  loading: boolean
  error: string | null
  systemStatus: DTSearchStatus | null
  
  // Search History
  searchHistory: string[]
}

const API_BASE = '/api/search'

export function useDTSearch() {
  // State Management
  const [state, setState] = useState<DTSearchState>({
    results: [],
    totalHits: 0,
    maxScore: 0,
    searchTime: 0,
    query: '',
    searchMode: 'basic',
    suggestions: [],
    currentPage: 1,
    pageSize: 20,
    hasNext: false,
    hasPrevious: false,
    loading: false,
    error: null,
    systemStatus: null,
    searchHistory: []
  })

  // Load search history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('dtSearch_history')
    if (savedHistory) {
      try {
        const history = JSON.parse(savedHistory)
        setState(prev => ({ ...prev, searchHistory: history.slice(0, 10) }))
      } catch (e) {
        console.warn('Failed to load search history:', e)
      }
    }
  }, [])

  // Save search history
  const saveToHistory = useCallback((query: string) => {
    if (!query.trim() || query.length < 2) return
    
    setState(prev => {
      const newHistory = [query, ...prev.searchHistory.filter(h => h !== query)].slice(0, 10)
      localStorage.setItem('dtSearch_history', JSON.stringify(newHistory))
      return { ...prev, searchHistory: newHistory }
    })
  }, [])

  // Basic Search Function
  const search = useCallback(async (
    query: string,
    options: Partial<DTSearchOptions> = {}
  ): Promise<DTSearchResponse | null> => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        results: [], 
        totalHits: 0, 
        error: null, 
        query: '' 
      }))
      return null
    }

    setState(prev => ({ 
      ...prev, 
      loading: true, 
      error: null, 
      query,
      searchMode: options.searchMode || 'basic'
    }))

    try {
      const searchParams = new URLSearchParams({
        q: query,
        page: (options.page || state.currentPage).toString(),
        size: (options.pageSize || state.pageSize).toString()
      })

      const response = await fetch(`${API_BASE}?${searchParams}`)
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status} ${response.statusText}`)
      }

      const data: DTSearchResponse = await response.json()
      
      setState(prev => ({
        ...prev,
        results: data.hits,
        totalHits: data.total_hits,
        maxScore: data.max_score,
        searchTime: data.took,
        currentPage: data.pagination?.current_page || 1,
        hasNext: data.pagination?.has_next || false,
        hasPrevious: data.pagination?.has_previous || false,
        loading: false,
        error: null
      }))

      // Save to history
      saveToHistory(query)
      
      return data
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Search failed'
      setState(prev => ({ 
        ...prev, 
        loading: false, 
        error: errorMessage,
        results: [],
        totalHits: 0
      }))
      return null
    }
  }, [state.currentPage, state.pageSize, saveToHistory])

  // Boolean Search Function
  const booleanSearch = useCallback(async (
    query: string,
    options: Partial<DTSearchOptions> = {}
  ): Promise<DTSearchResponse | null> => {
    if (!query.trim()) return null

    setState(prev => ({ 
      ...prev, 
      loading: true, 
      error: null, 
      query,
      searchMode: 'boolean'
    }))

    try {
      const searchParams = new URLSearchParams({ q: query })
      const response = await fetch(`${API_BASE}/boolean?${searchParams}`)
      
      if (!response.ok) {
        throw new Error(`Boolean search failed: ${response.status}`)
      }

      const data: DTSearchResponse = await response.json()
      
      setState(prev => ({
        ...prev,
        results: data.hits,
        totalHits: data.total_hits,
        maxScore: data.max_score,
        searchTime: data.took,
        loading: false,
        error: null
      }))

      saveToHistory(query)
      return data
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Boolean search failed'
      setState(prev => ({ 
        ...prev, 
        loading: false, 
        error: errorMessage,
        results: [],
        totalHits: 0
      }))
      return null
    }
  }, [saveToHistory])

  // Get Search Suggestions
  const getSuggestions = useCallback(async (partial: string): Promise<string[]> => {
    if (!partial.trim() || partial.length < 2) {
      setState(prev => ({ ...prev, suggestions: [] }))
      return []
    }

    try {
      const searchParams = new URLSearchParams({ q: partial, limit: '10' })
      const response = await fetch(`${API_BASE}/suggest?${searchParams}`)
      
      if (!response.ok) return []

      const data: DTSearchSuggestion = await response.json()
      const suggestions = data.suggestions || []
      
      setState(prev => ({ ...prev, suggestions }))
      return suggestions
    } catch (error) {
      console.warn('Suggestions failed:', error)
      return []
    }
  }, [])

  // Get System Status
  const getSystemStatus = useCallback(async (): Promise<DTSearchStatus | null> => {
    try {
      const response = await fetch(`${API_BASE}/status`)
      
      if (!response.ok) return null

      const status: DTSearchStatus = await response.json()
      setState(prev => ({ ...prev, systemStatus: status }))
      return status
    } catch (error) {
      console.warn('System status check failed:', error)
      return null
    }
  }, [])

  // Pagination Functions
  const nextPage = useCallback(() => {
    if (state.hasNext && state.query) {
      search(state.query, { 
        page: state.currentPage + 1,
        searchMode: state.searchMode 
      })
    }
  }, [state.hasNext, state.query, state.currentPage, state.searchMode, search])

  const prevPage = useCallback(() => {
    if (state.hasPrevious && state.query) {
      search(state.query, { 
        page: state.currentPage - 1,
        searchMode: state.searchMode 
      })
    }
  }, [state.hasPrevious, state.query, state.currentPage, state.searchMode, search])

  const goToPage = useCallback((page: number) => {
    if (state.query && page > 0) {
      search(state.query, { 
        page,
        searchMode: state.searchMode 
      })
    }
  }, [state.query, state.searchMode, search])

  // Clear Search
  const clearSearch = useCallback(() => {
    setState(prev => ({
      ...prev,
      results: [],
      totalHits: 0,
      maxScore: 0,
      searchTime: 0,
      query: '',
      suggestions: [],
      currentPage: 1,
      hasNext: false,
      hasPrevious: false,
      error: null
    }))
  }, [])

  // Clear Search History
  const clearHistory = useCallback(() => {
    localStorage.removeItem('dtSearch_history')
    setState(prev => ({ ...prev, searchHistory: [] }))
  }, [])

  // Set Page Size
  const setPageSize = useCallback((size: number) => {
    setState(prev => ({ ...prev, pageSize: size }))
    if (state.query) {
      search(state.query, { pageSize: size, page: 1 })
    }
  }, [state.query, search])

  // Advanced Search with operators detection
  const smartSearch = useCallback(async (query: string): Promise<DTSearchResponse | null> => {
    if (!query.trim()) return null

    // Detect if query contains boolean operators
    const hasBoolean = /\s+(AND|OR|NOT)\s+/i.test(query)
    
    if (hasBoolean) {
      return booleanSearch(query)
    } else {
      return search(query)
    }
  }, [search, booleanSearch])

  // Initialize system status on mount
  useEffect(() => {
    getSystemStatus()
  }, [getSystemStatus])

  // Return all functionality
  return {
    // Search Results
    results: state.results,
    totalHits: state.totalHits,
    maxScore: state.maxScore,
    searchTime: state.searchTime,
    
    // Current Search
    query: state.query,
    searchMode: state.searchMode,
    suggestions: state.suggestions,
    
    // Pagination
    currentPage: state.currentPage,
    pageSize: state.pageSize,
    hasNext: state.hasNext,
    hasPrevious: state.hasPrevious,
    
    // Status
    loading: state.loading,
    error: state.error,
    systemStatus: state.systemStatus,
    
    // History
    searchHistory: state.searchHistory,
    
    // Search Functions
    search,
    booleanSearch,
    smartSearch,
    getSuggestions,
    
    // Utility Functions
    clearSearch,
    clearHistory,
    
    // Pagination Functions
    nextPage,
    prevPage,
    goToPage,
    setPageSize,
    
    // System Functions
    getSystemStatus,
    
    // Computed Properties
    hasResults: state.results.length > 0,
    isEmpty: state.results.length === 0 && !state.loading && state.query !== '',
    isConnected: state.systemStatus?.elasticsearch_connected || false,
    indexedCount: state.systemStatus?.document_count || 0
  }
}
