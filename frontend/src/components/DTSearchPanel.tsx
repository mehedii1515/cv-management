'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { 
  Search, 
  Zap, 
  Clock, 
  Target, 
  BookOpen, 
  X, 
  Loader2,
  CheckCircle,
  AlertCircle,
  Info,
  ChevronLeft,
  ChevronRight,
  Database,
  Activity,
  TrendingUp,
  Eye
} from 'lucide-react'
import { useDTSearch } from '@/hooks/useDTSearch'
import { ResumeCard } from '@/components/ResumeCard'

interface DTSearchPanelProps {
  className?: string
}

export function DTSearchPanel({ className = '' }: DTSearchPanelProps) {
  const {
    // Search State
    results,
    totalHits,
    maxScore,
    searchTime,
    query,
    searchMode,
    suggestions,
    
    // Pagination
    currentPage,
    pageSize,
    hasNext,
    hasPrevious,
    
    // Status
    loading,
    error,
    systemStatus,
    searchHistory,
    
    // Functions
    search,
    booleanSearch,
    smartSearch,
    getSuggestions,
    clearSearch,
    clearHistory,
    nextPage,
    prevPage,
    setPageSize,
    
    // Computed
    hasResults,
    isEmpty,
    isConnected,
    indexedCount
  } = useDTSearch()

  // Local State
  const [searchInput, setSearchInput] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedMode, setSelectedMode] = useState<'smart' | 'basic' | 'boolean'>('smart')
  const [showHelp, setShowHelp] = useState(false)
  const [selectedResult, setSelectedResult] = useState<any>(null) // For showing resume details dialog
  const [loadingDetails, setLoadingDetails] = useState(false) // For loading state when fetching full resume

  // Function to handle viewing resume details
  const handleViewDetails = async (result: any) => {
    setLoadingDetails(true)
    try {
      // Fetch the complete resume details using the resume ID
      const response = await fetch(`http://localhost:8000/api/resumes/${result.id}/`)
      if (response.ok) {
        const fullResumeData = await response.json()
        setSelectedResult(fullResumeData)
      } else {
        // Fallback to limited DTSearch data if API call fails
        console.warn('Failed to fetch full resume details, using DTSearch data')
        const resumeData = {
          id: result.id,
          full_name: result.name,
          email: result.email,
          phone: result.phone,
          location: result.location,
          current_employer: result.current_employer,
          years_of_experience: result.years_of_experience || 0,
          total_experience_months: result.years_of_experience ? result.years_of_experience * 12 : 0,
          experience_display: `${result.years_of_experience || 0} years`,
          summary: result.summary,
          skills: result.skills,
          skill_keywords: result.skills ? result.skills.split(',').map((s: string) => s.trim()) : [],
          processing_status: 'completed',
          file_path: result.file_path,
          work_experience: result.experience || '',
          extracted_text: result.text_content || '',
          upload_date: new Date().toISOString().split('T')[0], // Fallback date
        }
        setSelectedResult(resumeData)
      }
    } catch (error) {
      console.error('Error fetching resume details:', error)
      // Use DTSearch data as fallback
      const resumeData = {
        id: result.id,
        full_name: result.name,
        email: result.email,
        phone: result.phone,
        location: result.location,
        current_employer: result.current_employer,
        years_of_experience: result.years_of_experience || 0,
        total_experience_months: result.years_of_experience ? result.years_of_experience * 12 : 0,
        experience_display: `${result.years_of_experience || 0} years`,
        summary: result.summary,
        skills: result.skills,
        skill_keywords: result.skills ? result.skills.split(',').map((s: string) => s.trim()) : [],
        processing_status: 'completed',
        file_path: result.file_path,
        work_experience: result.experience || '',
        extracted_text: result.text_content || '',
        upload_date: new Date().toISOString().split('T')[0], // Fallback date
      }
      setSelectedResult(resumeData)
    } finally {
      setLoadingDetails(false)
    }
  }

  // Handle input change and get suggestions
  useEffect(() => {
    if (searchInput.length >= 2) {
      const timer = setTimeout(() => {
        getSuggestions(searchInput)
        setShowSuggestions(true)
      }, 300)
      return () => clearTimeout(timer)
    } else {
      setShowSuggestions(false)
    }
  }, [searchInput, getSuggestions])

  // Handle search submission
  const handleSearch = async () => {
    if (!searchInput.trim()) return

    setShowSuggestions(false)
    
    switch (selectedMode) {
      case 'smart':
        await smartSearch(searchInput)
        break
      case 'boolean':
        await booleanSearch(searchInput)
        break
      case 'basic':
      default:
        await search(searchInput)
        break
    }
  }

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  // Select suggestion
  const selectSuggestion = (suggestion: string) => {
    setSearchInput(suggestion)
    setShowSuggestions(false)
    // Auto-search when suggestion is selected
    setTimeout(() => {
      if (selectedMode === 'smart') {
        smartSearch(suggestion)
      } else if (selectedMode === 'boolean') {
        booleanSearch(suggestion)
      } else {
        search(suggestion)
      }
    }, 100)
  }

  // Format search time
  const formatSearchTime = (ms: number) => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(2)}s`
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Zap className="h-6 w-6 text-primary" />
                <CardTitle className="text-xl">Database Index Search</CardTitle>
              </div>
              {isConnected && (
                <Badge variant="secondary" className="gap-1">
                  <CheckCircle className="h-3 w-3" />
                  Connected
                </Badge>
              )}
            </div>
            
            {systemStatus && (
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Database className="h-4 w-4" />
                  {indexedCount.toLocaleString()} documents
                </div>
                {hasResults && (
                  <div className="flex items-center gap-1">
                    <TrendingUp className="h-4 w-4" />
                    {totalHits.toLocaleString()} results
                  </div>
                )}
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Search Input */}
          <div className="relative">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Enter search query... (e.g., 'python developer', 'Java AND Spring', 'manager OR lead')"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="pl-10 h-12 text-base"
                  disabled={loading}
                />
                
                {/* Suggestions Dropdown */}
                {showSuggestions && suggestions.length > 0 && (
                  <div className="absolute top-full left-0 right-0 z-50 mt-1 bg-background border rounded-md shadow-lg max-h-48 overflow-auto">
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        className="w-full text-left px-3 py-2 hover:bg-accent text-sm"
                        onClick={() => selectSuggestion(suggestion)}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <Select value={selectedMode} onValueChange={(value: any) => setSelectedMode(value)}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="smart">Smart</SelectItem>
                  <SelectItem value="basic">Basic</SelectItem>
                  <SelectItem value="boolean">Boolean</SelectItem>
                </SelectContent>
              </Select>

              <Button onClick={handleSearch} disabled={loading || !searchInput.trim()}>
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
                Search
              </Button>
            </div>

            {/* Search Mode Help */}
            <div className="flex items-center justify-between mt-2">
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                {selectedMode === 'smart' && (
                  <span>🤖 Smart mode: Automatically detects boolean operators</span>
                )}
                {selectedMode === 'basic' && (
                  <span>📝 Basic mode: Full-text search with relevance scoring</span>
                )}
                {selectedMode === 'boolean' && (
                  <span>🔧 Boolean mode: Use AND, OR, NOT operators</span>
                )}
              </div>
              
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => setShowHelp(!showHelp)}
                className="text-xs"
              >
                <Info className="h-3 w-3 mr-1" />
                Help
              </Button>
            </div>

            {/* Help Section */}
            {showHelp && (
              <Card className="mt-2 p-3 text-sm">
                <div className="space-y-2">
                  <div><strong>Smart Mode:</strong> Automatically chooses the best search method</div>
                  <div><strong>Basic Search:</strong> "python developer" → finds documents containing these terms</div>
                  <div><strong>Boolean Search:</strong> "Python AND Django", "Manager OR Lead", "Java NOT JavaScript"</div>
                  <div><strong>Tips:</strong> Use quotes for exact phrases, * for wildcards</div>
                </div>
              </Card>
            )}
          </div>

          {/* Search History */}
          {searchHistory.length > 0 && (
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs text-muted-foreground">Recent:</span>
              {searchHistory.slice(0, 5).map((historyItem, index) => (
                <Badge
                  key={index}
                  variant="outline"
                  className="cursor-pointer text-xs"
                  onClick={() => {
                    setSearchInput(historyItem)
                    if (selectedMode === 'smart') {
                      smartSearch(historyItem)
                    } else if (selectedMode === 'boolean') {
                      booleanSearch(historyItem)
                    } else {
                      search(historyItem)
                    }
                  }}
                >
                  {historyItem}
                </Badge>
              ))}
              {searchHistory.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearHistory}
                  className="text-xs h-6"
                >
                  <X className="h-3 w-3" />
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Error Display */}
      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 text-destructive">
              <AlertCircle className="h-4 w-4" />
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Search Results */}
      {query && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <CardTitle className="text-lg">Search Results</CardTitle>
                {hasResults && (
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Target className="h-4 w-4" />
                      {totalHits.toLocaleString()} total
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {formatSearchTime(searchTime)}
                    </div>
                    <div className="flex items-center gap-1">
                      <Activity className="h-4 w-4" />
                      Score: {maxScore.toFixed(2)}
                    </div>
                  </div>
                )}
              </div>
              
              {hasResults && (
                <div className="flex items-center gap-2">
                  <Select value={pageSize.toString()} onValueChange={(value) => setPageSize(parseInt(value))}>
                    <SelectTrigger className="w-20">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="10">10</SelectItem>
                      <SelectItem value="20">20</SelectItem>
                      <SelectItem value="50">50</SelectItem>
                    </SelectContent>
                  </Select>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={clearSearch}
                  >
                    Clear
                  </Button>
                </div>
              )}
            </div>
          </CardHeader>

          <CardContent>
            {loading && (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin mr-2" />
                <span>Searching...</span>
              </div>
            )}

            {isEmpty && (
              <div className="text-center py-8 text-muted-foreground">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No results found for "{query}"</p>
                <p className="text-sm mt-1">Try different keywords or check your spelling</p>
              </div>
            )}

            {hasResults && (
              <div className="space-y-4">
                {results.map((result, index) => (
                  <Card 
                    key={`dt-result-${result.id}-${index}-${result.name?.replace(/\s+/g, '-')}`} 
                    className="hover:shadow-md transition-shadow"
                    style={{ cursor: 'default' }}
                    onClick={(e) => e.preventDefault()}
                  >
                    <CardContent className="pt-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg">
                            {result.name || 'Unknown'}
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            {result.current_employer && `${result.current_employer} • `}
                            {result.location}
                          </p>
                        </div>
                        <Badge variant="secondary" className="ml-2">
                          Score: {result.score.toFixed(2)}
                        </Badge>
                      </div>

                      {result.summary && (
                        <p className="text-sm mb-2 line-clamp-2">{result.summary}</p>
                      )}

                      {result.skills && (
                        <div className="flex flex-wrap gap-1 mb-2">
                          {result.skills.split(',').slice(0, 5).map((skill, skillIndex) => (
                            <Badge key={skillIndex} variant="outline" className="text-xs">
                              {skill.trim()}
                            </Badge>
                          ))}
                          {result.skills.split(',').length > 5 && (
                            <Badge variant="outline" className="text-xs">
                              +{result.skills.split(',').length - 5} more
                            </Badge>
                          )}
                        </div>
                      )}

                      {/* Highlights */}
                      {result.highlights && Object.keys(result.highlights).length > 0 && (
                        <div className="mt-2 p-2 bg-accent/50 rounded text-xs">
                          <div className="font-medium mb-1">Matches:</div>
                          {Object.entries(result.highlights).map(([field, highlights]) => (
                            <div key={field} className="mb-1">
                              <span className="font-medium capitalize">{field}:</span>{' '}
                              <span dangerouslySetInnerHTML={{ 
                                __html: highlights.join(' ... ') 
                              }} />
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between text-xs text-muted-foreground mt-2">
                        <span>{result.email}</span>
                        <span>{result.phone}</span>
                        <span>{result.years_of_experience} years exp.</span>
                      </div>

                      {/* Details Button */}
                      <div className="flex justify-end mt-3 pt-2 border-t">
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => handleViewDetails(result)}
                          disabled={loadingDetails}
                          className="text-xs"
                        >
                          {loadingDetails ? (
                            <>
                              <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                              Loading...
                            </>
                          ) : (
                            <>
                              <Eye className="h-3 w-3 mr-1" />
                              View Details
                            </>
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Pagination */}
            {hasResults && (hasPrevious || hasNext) && (
              <div className="flex items-center justify-between mt-6">
                <div className="text-sm text-muted-foreground">
                  Page {currentPage} • {totalHits.toLocaleString()} total results
                </div>
                
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={prevPage}
                    disabled={!hasPrevious || loading}
                  >
                    <ChevronLeft className="h-4 w-4 mr-1" />
                    Previous
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={nextPage}
                    disabled={!hasNext || loading}
                  >
                    Next
                    <ChevronRight className="h-4 w-4 ml-1" />
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Resume Details Dialog */}
      {selectedResult && (
        <ResumeCard 
          resume={selectedResult} 
          autoOpenDetails={true}
          onCloseDetails={() => setSelectedResult(null)}
        />
      )}
    </div>
  )
}

// Compact DTSearch widget for integration into existing components
export function DTSearchWidget({ onSearch, className = '' }: { 
  onSearch?: (results: any[]) => void
  className?: string 
}) {
  const { search, smartSearch, loading, results } = useDTSearch()
  const [query, setQuery] = useState('')

  const handleSearch = async () => {
    if (!query.trim()) return
    const result = await smartSearch(query)
    if (result && onSearch) {
      onSearch(result.hits)
    }
  }

  return (
    <div className={`flex gap-2 ${className}`}>
      <div className="relative flex-1">
        <Zap className="absolute left-3 top-2.5 h-4 w-4 text-primary" />
        <Input
          placeholder="DTSearch: Try 'Python AND Django' or 'Manager OR Lead'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          className="pl-10"
        />
      </div>
      <Button onClick={handleSearch} disabled={loading} size="sm">
        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
      </Button>
    </div>
  )
}

export default DTSearchPanel
