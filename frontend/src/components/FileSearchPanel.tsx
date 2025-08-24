'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Slider } from '@/components/ui/slider'
import { Separator } from '@/components/ui/separator'
import { Calendar } from '@/components/ui/calendar'
import { EnhancedFileViewer } from '@/components/EnhancedFileViewer'
import { format } from 'date-fns'
import { 
  Search, 
  File, 
  FileText, 
  HardDrive,
  X,
  Loader2,
  FileX,
  FileCheck,
  Info,
  Folder,
  Clock,
  Filter,
  Calendar as CalendarIcon,
  Languages
} from 'lucide-react'

export interface FileSearchResult {
  file_id: string
  filename: string
  file_path: string
  relative_path: string
  file_extension: string
  file_size: number
  file_size_formatted: string
  file_category: string
  created_date: string
  modified_date: string
  indexed_date: string
  page_count: number
  word_count: number
  language: string
  directory: string
  content_preview: string
  highlights: Record<string, string[]>
  score: number
}

interface FileSearchFilters {
  file_extension: string
  min_size: number | null
  max_size: number | null
  date_from: string | null
  date_to: string | null
  directory: string | null
}

interface FileSearchResponse {
  files: FileSearchResult[]
  total_files: number
  max_score: number
  took: number
  search_info: {
    query: string
    search_type: string
    index_name: string
    total_indexed_files: number
    file_extensions_found: string[]
    categories_found: string[]
    search_time_ms: number
  }
}

interface FileSearchPanelProps {
  onSelectResult?: (result: FileSearchResult) => void
  className?: string
}

export function FileSearchPanel({ onSelectResult, className = '' }: FileSearchPanelProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState<'basic' | 'boolean'>('basic')
  const [searchResults, setSearchResults] = useState<FileSearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [showFilters, setShowFilters] = useState(false)
  
  // Filter states
  const [filters, setFilters] = useState<FileSearchFilters>({
    file_extension: '',
    min_size: null,
    max_size: null,
    date_from: null,
    date_to: null,
    directory: null,
  })

  // Get suggestions when user types
  useEffect(() => {
    const getSuggestions = async () => {
      if (searchQuery.length >= 2) {
        try {
          const response = await fetch(`/api/search/files/suggestions?q=${encodeURIComponent(searchQuery)}&limit=5`)
          if (response.ok) {
            const data = await response.json()
            setSuggestions(data.suggestions || [])
            setShowSuggestions(true)
          }
        } catch (error) {
          console.error('Failed to get suggestions:', error)
        }
      } else {
        setSuggestions([])
        setShowSuggestions(false)
      }
    }

    const timeoutId = setTimeout(getSuggestions, 300)
    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  // Handle file search
  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setLoading(true)
    setError(null)
    setShowSuggestions(false)

    try {
      const searchData = {
        query: searchQuery,
        search_type: searchType,
        page: 1,
        page_size: 20,
        ...filters
      }

      const response = await fetch('/api/search/files/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData)
      })
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`)
      }

      const data: FileSearchResponse = await response.json()
      setSearchResults(data)
    } catch (error) {
      setError(error instanceof Error ? error.message : 'File search failed')
      setSearchResults(null)
    } finally {
      setLoading(false)
    }
  }

  // Clear all filters
  const clearFilters = () => {
    setFilters({
      file_extension: '',
      min_size: null,
      max_size: null,
      date_from: null,
      date_to: null,
      directory: null,
    })
  }

  // Get file type icon
  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case '.pdf':
        return <FileText className="h-4 w-4 text-red-500" />
      case '.docx':
      case '.doc':
        return <File className="h-4 w-4 text-blue-500" />
      case '.txt':
        return <FileX className="h-4 w-4 text-gray-500" />
      case '.rtf':
        return <FileCheck className="h-4 w-4 text-purple-500" />
      default:
        return <File className="h-4 w-4 text-gray-500" />
    }
  }

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string) => {
    setSearchQuery(suggestion)
    setShowSuggestions(false)
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* File Search Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <HardDrive className="h-5 w-5 text-primary" />
              <CardTitle>File Index Search</CardTitle>
              {searchResults && (
                <Badge variant="secondary" className="ml-2">
                  {searchResults.search_info.total_indexed_files} files indexed
                </Badge>
              )}
            </div>
            
            <div className="flex gap-2">
              <Select value={searchType} onValueChange={(value: 'basic' | 'boolean') => setSearchType(value)}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="basic">Basic</SelectItem>
                  <SelectItem value="boolean">Boolean</SelectItem>
                </SelectContent>
              </Select>
              
              {/* Temporarily commented out Filter button */}
              {/* <Button 
                variant={showFilters ? "secondary" : "outline"} 
                size="icon" 
                onClick={() => setShowFilters(!showFilters)}
                title="Toggle filters"
              >
                <Filter className="h-4 w-4" />
              </Button> */}
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Search Input with Suggestions */}
          <div className="relative">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Input
                  placeholder={
                    searchType === 'boolean' 
                      ? "Boolean search: python AND (developer OR programmer) NOT java"
                      : "Search file contents... (e.g., 'machine learning', 'project manager')"
                  }
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  onFocus={() => setShowSuggestions(suggestions.length > 0)}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                  className="pr-10"
                />
                
                {/* Search suggestions */}
                {showSuggestions && suggestions.length > 0 && (
                  <Card className="absolute top-full left-0 right-0 z-10 mt-1 max-h-48 overflow-y-auto">
                    <CardContent className="p-0">
                      {suggestions.map((suggestion, index) => (
                        <div
                          key={index}
                          className="px-3 py-2 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                          onClick={() => handleSuggestionClick(suggestion)}
                        >
                          <span className="text-sm">{suggestion}</span>
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                )}
              </div>
              
              <Button onClick={handleSearch} disabled={loading}>
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
                Search
              </Button>
            </div>
          </div>

          {/* Temporarily commented out Filters Panel */}
          {/* {showFilters && (
            <div className="bg-gray-50 p-4 rounded-lg space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Search Filters</h3>
                <Button variant="ghost" size="sm" onClick={clearFilters}>
                  Clear All
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>File Type</Label>
                  <Select
                    value={filters.file_extension}
                    onValueChange={(value) => setFilters({ ...filters, file_extension: value === 'all' ? '' : value })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Any type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Any type</SelectItem>
                      <SelectItem value=".pdf">PDF</SelectItem>
                      <SelectItem value=".docx">DOCX</SelectItem>
                      <SelectItem value=".doc">DOC</SelectItem>
                      <SelectItem value=".txt">TXT</SelectItem>
                      <SelectItem value=".rtf">RTF</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                
                <div className="space-y-2">
                  <Label>Min Size (KB)</Label>
                  <Input 
                    type="number" 
                    placeholder="Min size" 
                    value={filters.min_size !== null ? String(filters.min_size) : ''}
                    onChange={(e) => setFilters({
                      ...filters, 
                      min_size: e.target.value ? Number(e.target.value) : null
                    })}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label>Max Size (KB)</Label>
                  <Input 
                    type="number" 
                    placeholder="Max size" 
                    value={filters.max_size !== null ? String(filters.max_size) : ''}
                    onChange={(e) => setFilters({
                      ...filters, 
                      max_size: e.target.value ? Number(e.target.value) : null
                    })}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label>Modified Date</Label>
                  <div className="flex gap-2">
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button variant="outline" size="sm" className="flex-1 justify-start text-left font-normal">
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {filters.date_from ? format(new Date(filters.date_from), 'PP') : 'From date'}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar
                          mode="single"
                          selected={filters.date_from ? new Date(filters.date_from) : undefined}
                          onSelect={(date) => setFilters({
                            ...filters,
                            date_from: date ? date.toISOString() : null
                          })}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                    
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button variant="outline" size="sm" className="flex-1 justify-start text-left font-normal">
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {filters.date_to ? format(new Date(filters.date_to), 'PP') : 'To date'}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar
                          mode="single"
                          selected={filters.date_to ? new Date(filters.date_to) : undefined}
                          onSelect={(date) => setFilters({
                            ...filters,
                            date_to: date ? date.toISOString() : null
                          })}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                </div>
              </div>
            </div>
          )} */}
          
          {/* Search Type Info */}
          {searchType === 'boolean' && (
            <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
              <div className="font-medium mb-1">Boolean Search Tips:</div>
              <div>• Use AND, OR, NOT operators</div>
              <div>• Quotes for exact phrases: "machine learning"</div>
              <div>• Parentheses for grouping: (python OR java) AND developer</div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="flex items-center gap-2 text-red-700">
              <X className="h-4 w-4" />
              <span>Search Error: {error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {searchResults && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <FileCheck className="h-5 w-5" />
                Search Results
                <Badge variant="outline" className="ml-2">
                  {searchResults.total_files} files found
                </Badge>
              </CardTitle>
              
              <div className="text-sm text-gray-500">
                Search took {searchResults.took}ms
              </div>
            </div>
            
            {/* Search Info */}
            <div className="text-sm text-gray-600">
              <div className="flex flex-wrap gap-4">
                <span>Query: "{searchResults.search_info.query}"</span>
                <span>Type: {searchResults.search_info.search_type}</span>
                {searchResults.search_info.file_extensions_found.length > 0 && (
                  <span>
                    Extensions: {searchResults.search_info.file_extensions_found.join(', ')}
                  </span>
                )}
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            {searchResults.files.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileX className="h-8 w-8 mx-auto mb-2" />
                <p>No files found matching your search criteria.</p>
                <p className="text-sm mt-1">Try different keywords or adjust your filters.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {searchResults.files.map((file, index) => (
                  <Card 
                    key={file.file_id} 
                    className="hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => onSelectResult?.(file)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start gap-3">
                        {/* File Icon */}
                        <div className="flex-shrink-0 mt-1">
                          {getFileIcon(file.file_extension)}
                        </div>

                        {/* File Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-medium text-lg truncate pr-2">
                              {file.filename}
                            </h3>
                            <div className="flex items-center gap-2 flex-shrink-0">
                              <Badge variant="secondary" className="text-xs">
                                Score: {file.score.toFixed(2)}
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {file.file_extension.toUpperCase()}
                              </Badge>
                            </div>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600 mb-3">
                            <div className="flex items-center gap-1">
                              <Folder className="h-3 w-3" />
                              <span className="truncate">{file.relative_path}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <HardDrive className="h-3 w-3" />
                              <span>{file.file_size_formatted}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              <span>Modified: {new Date(file.modified_date).toLocaleDateString()}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <FileText className="h-3 w-3" />
                              <span>{file.word_count} words</span>
                              {file.page_count > 1 && <span>, {file.page_count} pages</span>}
                            </div>
                          </div>

                          {/* Content Preview */}
                          {file.content_preview && (
                            <div className="bg-gray-50 rounded p-3 mb-3">
                              <div className="text-sm text-gray-700">
                                <div 
                                  dangerouslySetInnerHTML={{ 
                                    __html: file.content_preview.replace(
                                      new RegExp(searchResults.search_info.query, 'gi'), 
                                      `<mark class="bg-yellow-200 px-1 rounded">$&</mark>`
                                    )
                                  }} 
                                />
                              </div>
                            </div>
                          )}

                          {/* Highlights */}
                          {file.highlights && Object.keys(file.highlights).length > 0 && (
                            <div className="space-y-1">
                              {Object.entries(file.highlights).map(([field, highlights], idx) => (
                                <div key={idx} className="text-sm">
                                  <span className="font-medium text-gray-600 capitalize">
                                    {field}:
                                  </span>
                                  {highlights.map((highlight, hidx) => (
                                    <div 
                                      key={hidx} 
                                      className="ml-2 text-gray-700"
                                      dangerouslySetInnerHTML={{ __html: highlight }}
                                    />
                                  ))}
                                </div>
                              ))}
                            </div>
                          )}

                          {/* File Category and Language */}
                          <div className="flex gap-2 mt-3">
                            {file.file_category && (
                              <Badge variant="outline" className="text-xs">
                                {file.file_category.replace('_', ' ').toUpperCase()}
                              </Badge>
                            )}
                            {file.language && (
                              <Badge variant="outline" className="text-xs">
                                {file.language}
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Information Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="h-5 w-5" />
            File Search System
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-gray-600 space-y-2">
            <p>
              <strong>Pure File Search:</strong> This searches through indexed files directly, 
              not database records. Results show actual files from your file system.
            </p>
            <p>
              <strong>Supported Formats:</strong> PDF, Word (DOCX/DOC), Text (TXT), RTF
            </p>
            <p>
              <strong>Search Features:</strong> Full-text content search, boolean operators, 
              file metadata filtering, and intelligent suggestions.
            </p>
            <p>
              <strong>Advanced Filters:</strong> Filter by file type, category, language, size, and date range 
              to narrow down your search results and find exactly what you need.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default FileSearchPanel
