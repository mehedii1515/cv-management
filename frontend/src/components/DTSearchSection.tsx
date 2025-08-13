// DTSearch Section for Resume Search
'use client'

import React, { useState, useCallback, useEffect } from 'react'
import { Search, Zap, Settings, Filter, FileText, Clock } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useDTSearch, DTSearchResult, DTSearchHit, DTSearchFilters } from '@/hooks/useDTSearch'
import { useDebounce } from '@/hooks/useDebounce'

interface DTSearchSectionProps {
  onResultsChange?: (results: DTSearchHit[]) => void
  className?: string
}

export default function DTSearchSection({ onResultsChange, className }: DTSearchSectionProps) {
  // Search states
  const [searchMode, setSearchMode] = useState<'simple' | 'boolean' | 'advanced'>('simple')
  const [searchTerm, setSearchTerm] = useState('')
  const [booleanQuery, setBooleanQuery] = useState('')
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  
  // DTSearch hook
  const {
    searchResumes,
    booleanSearch,
    getSuggestions,
    getSearchStatus,
    loading,
    error,
    lastResults,
    clearError
  } = useDTSearch()
  
  // Debounced search term for suggestions
  const debouncedSearchTerm = useDebounce(searchTerm, 300)
  
  // Get suggestions when search term changes
  useEffect(() => {
    if (debouncedSearchTerm && searchMode === 'simple') {
      getSuggestions(debouncedSearchTerm).then(setSuggestions)
    } else {
      setSuggestions([])
    }
  }, [debouncedSearchTerm, searchMode, getSuggestions])
  
  // Handle search execution
  const handleSearch = useCallback(async () => {
    try {
      clearError()
      let results: DTSearchResult
      
      switch (searchMode) {
        case 'boolean':
          if (!booleanQuery.trim()) return
          results = await booleanSearch(booleanQuery)
          break
        case 'simple':
        default:
          if (!searchTerm.trim()) return
          results = await searchResumes(searchTerm)
          break
      }
      
      // Notify parent component of results
      if (onResultsChange) {
        onResultsChange(results.hits)
      }
      
    } catch (err) {
      console.error('Search failed:', err)
    }
  }, [searchMode, searchTerm, booleanQuery, searchResumes, booleanSearch, onResultsChange, clearError])
  
  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
      setShowSuggestions(false)
    }
  }
  
  // Handle suggestion selection
  const handleSuggestionSelect = (suggestion: string) => {
    setSearchTerm(suggestion)
    setShowSuggestions(false)
    // Trigger search with selected suggestion
    setTimeout(() => handleSearch(), 100)
  }
  
  return (
    <div className={className}>
      {/* DTSearch Header */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            DTSearch - Advanced Resume Search
            <Badge variant="secondary" className="ml-2">
              Professional
            </Badge>
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            High-performance full-text search with boolean operators and intelligent ranking
          </p>
        </CardHeader>
        <CardContent>
          {/* Search Mode Tabs */}
          <Tabs value={searchMode} onValueChange={(value) => setSearchMode(value as any)} className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="simple">Simple Search</TabsTrigger>
              <TabsTrigger value="boolean">Boolean Search</TabsTrigger>
              <TabsTrigger value="advanced">Advanced</TabsTrigger>
            </TabsList>
            
            {/* Simple Search */}
            <TabsContent value="simple" className="space-y-4">
              <div className="relative">
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      placeholder="Search resumes... (e.g., 'Python developer with React experience')"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      onKeyPress={handleKeyPress}
                      onFocus={() => setShowSuggestions(true)}
                      onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                      className="pr-10"
                    />
                    <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  </div>
                  <Button onClick={handleSearch} disabled={loading || !searchTerm.trim()}>
                    {loading ? 'Searching...' : 'Search'}
                  </Button>
                </div>
                
                {/* Search Suggestions */}
                {showSuggestions && suggestions.length > 0 && (
                  <div className="absolute top-full left-0 right-0 z-50 bg-background border rounded-md shadow-md mt-1">
                    {suggestions.map((suggestion, index) => (
                      <div
                        key={index}
                        className="px-3 py-2 hover:bg-muted cursor-pointer text-sm"
                        onClick={() => handleSuggestionSelect(suggestion)}
                      >
                        {suggestion}
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
              <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
                <span>Examples:</span>
                <Badge 
                  variant="outline" 
                  className="cursor-pointer" 
                  onClick={() => setSearchTerm('Python Django developer')}
                >
                  Python Django developer
                </Badge>
                <Badge 
                  variant="outline" 
                  className="cursor-pointer" 
                  onClick={() => setSearchTerm('React frontend engineer')}
                >
                  React frontend engineer
                </Badge>
                <Badge 
                  variant="outline" 
                  className="cursor-pointer" 
                  onClick={() => setSearchTerm('data scientist machine learning')}
                >
                  data scientist machine learning
                </Badge>
              </div>
            </TabsContent>
            
            {/* Boolean Search */}
            <TabsContent value="boolean" className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Boolean query... (e.g., 'Python AND (Django OR Flask) NOT PHP')"
                  value={booleanQuery}
                  onChange={(e) => setBooleanQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1"
                />
                <Button onClick={handleSearch} disabled={loading || !booleanQuery.trim()}>
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </div>
              
              <div className="space-y-2 text-xs text-muted-foreground">
                <p className="font-medium">Boolean Operators:</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  <div>
                    <code className="bg-muted px-1 py-0.5 rounded">AND</code> - Both terms required
                  </div>
                  <div>
                    <code className="bg-muted px-1 py-0.5 rounded">OR</code> - Either term acceptable
                  </div>
                  <div>
                    <code className="bg-muted px-1 py-0.5 rounded">NOT</code> - Exclude term
                  </div>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  <Badge 
                    variant="outline" 
                    className="cursor-pointer" 
                    onClick={() => setBooleanQuery('Python AND Django AND PostgreSQL')}
                  >
                    Python AND Django AND PostgreSQL
                  </Badge>
                  <Badge 
                    variant="outline" 
                    className="cursor-pointer" 
                    onClick={() => setBooleanQuery('(React OR Angular) AND TypeScript')}
                  >
                    (React OR Angular) AND TypeScript
                  </Badge>
                  <Badge 
                    variant="outline" 
                    className="cursor-pointer" 
                    onClick={() => setBooleanQuery('developer NOT junior')}
                  >
                    developer NOT junior
                  </Badge>
                </div>
              </div>
            </TabsContent>
            
            {/* Advanced Search */}
            <TabsContent value="advanced" className="space-y-4">
              <div className="text-center text-muted-foreground">
                <Settings className="w-8 h-8 mx-auto mb-2" />
                <p>Advanced filters coming soon...</p>
                <p className="text-xs">Use Boolean search for complex queries</p>
              </div>
            </TabsContent>
          </Tabs>
          
          {/* Error Display */}
          {error && (
            <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}
          
          {/* Search Results Summary */}
          {lastResults && (
            <div className="mt-4 flex items-center justify-between p-3 bg-muted/50 rounded-md">
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-1">
                  <FileText className="w-4 h-4" />
                  <span>{lastResults.total_hits} resumes found</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>{lastResults.took}ms</span>
                </div>
                {lastResults.search_info?.operators_detected?.length && (
                  <div className="flex items-center gap-1">
                    <Filter className="w-4 h-4" />
                    <span>{lastResults.search_info.operators_detected.join(', ')}</span>
                  </div>
                )}
              </div>
              {lastResults.max_score > 0 && (
                <Badge variant="outline">
                  Max Score: {lastResults.max_score.toFixed(2)}
                </Badge>
              )}
            </div>
          )}
        </CardContent>
      </Card>
      
      {/* DTSearch Features Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">DTSearch Features</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
            <div>
              <h4 className="font-medium mb-2">Search Capabilities</h4>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Full-text search across all resume content</li>
                <li>• Intelligent relevance ranking</li>
                <li>• Search result highlighting</li>
                <li>• Real-time search suggestions</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">Boolean Operations</h4>
              <ul className="space-y-1 text-muted-foreground">
                <li>• AND, OR, NOT operators</li>
                <li>• Parentheses for grouping</li>
                <li>• Complex query combinations</li>
                <li>• Phrase searching with quotes</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">Performance</h4>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Sub-second search response</li>
                <li>• Elasticsearch-powered indexing</li>
                <li>• Scalable to millions of documents</li>
                <li>• Real-time index updates</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
