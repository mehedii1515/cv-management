'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { FileUploadZone } from '@/components/FileUploadZone'
import { ResumeCard } from '@/components/ResumeCard'
import { StatsCards } from '@/components/StatsCards'
import { SearchFilters } from '@/components/SearchFilters'
import { DTSearchPanel } from '@/components/DTSearchPanel'
import { FileSearchPanel } from '@/components/FileSearchPanel'
import { EnhancedFileViewer } from '@/components/EnhancedFileViewer'
import { Breadcrumb } from '@/components/Breadcrumb'
import { PageHeader } from '@/components/PageHeader'
import { useResumes } from '@/hooks/useResumes'
import { Search, Upload, Users, Activity, Zap, File, ChevronLeft, ChevronRight } from 'lucide-react'
import type { SelectedFilters } from '@/types/filters'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Separator } from '@/components/ui/separator'
import type { FileSearchResult } from '@/components/FileSearchPanel'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('resumes')
  const [selectedResume, setSelectedResume] = useState<any>(null)
  const [selectedFile, setSelectedFile] = useState<any>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFilters, setSelectedFilters] = useState<SelectedFilters>({
    expertise: [],
    location: [],
    sectors: [],
    skills: [],
    experience_level: [],
    availability: []
  })
  
  const { 
    resumes, 
    stats, 
    loading, 
    pagination,
    uploadResume, 
    batchUploadResumes, 
    getFilterOptions,
    fetchResumes,
    refetch
  } = useResumes()

  // Handle hash-based navigation
  useEffect(() => {
    // Only run on client side
    if (typeof window !== 'undefined') {
      const handleHashChange = () => {
        const hash = window.location.hash.replace('#', '')
        if (hash === 'resumes' || hash === 'upload' || hash === 'dtsearch' || hash === 'filesearch') {
          setActiveTab(hash)
        } else if (!hash) {
          // Default to resumes tab if no hash
          setActiveTab('resumes')
          window.history.replaceState(null, '', '#resumes')
        }
      }

      // Set initial tab based on hash immediately
      handleHashChange()
      
      // Listen for hash changes
      window.addEventListener('hashchange', handleHashChange)
      
      return () => {
        window.removeEventListener('hashchange', handleHashChange)
      }
    }
  }, []) // Remove dependencies to run only once on mount

  const handleTabChange = (value: string) => {
    setActiveTab(value)
    // Clear selected resume and file when changing tabs
    setSelectedResume(null)
    setSelectedFile(null)
    if (typeof window !== 'undefined') {
      window.history.pushState(null, '', `#${value}`)
    }
  }

  const handleFilterChange = (filterType: string, value: string) => {
    setSelectedFilters(prev => {
      const currentValues = prev[filterType as keyof typeof prev] || []
      const isSelected = currentValues.includes(value)
      
      const newFilters = {
        ...prev,
        [filterType]: isSelected 
          ? currentValues.filter((v: string) => v !== value)
          : [...currentValues, value]
      }
      
      // Trigger backend search with new filters (reset to page 1)
      fetchResumes(searchTerm, newFilters, 1)
      
      return newFilters
    })
  }

  const handleClearFilters = () => {
    const emptyFilters = {
      expertise: [],
      location: [],
      sectors: [],
      skills: [],
      experience_level: [],
      availability: []
    }
    setSelectedFilters(emptyFilters)
    setSearchTerm('')
    // Don't fetch resumes when clearing - just reset to empty state
    // fetchResumes('', emptyFilters)
  }

  const handleSearchChange = (term: string) => {
    setSearchTerm(term)
    // Trigger backend search with current filters (reset to page 1)
    fetchResumes(term, selectedFilters, 1)
  }

  const availableFilters = getFilterOptions()

  // Pagination handlers
  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      fetchResumes(searchTerm, selectedFilters, newPage)
    }
  }

  const handlePreviousPage = () => {
    if (pagination.currentPage > 1) {
      handlePageChange(pagination.currentPage - 1)
    }
  }

  const handleNextPage = () => {
    if (pagination.currentPage < pagination.totalPages) {
      handlePageChange(pagination.currentPage + 1)
    }
  }

  // Don't fetch initial data - only fetch when there's a search or filter
  // useEffect(() => {
  //   if (typeof window !== 'undefined') {
  //     fetchResumes()
  //   }
  // }, [fetchResumes])
    
  // Backend handles all filtering and search - no client-side filtering needed
  // Only show resumes when there's an active search or filter
  const hasActiveSearch = searchTerm.trim() || Object.values(selectedFilters).some(arr => arr.length > 0)
  const filteredResumes = hasActiveSearch ? (resumes || []) : []

  return (
    <div className="bg-background min-h-screen">
      <div className="w-full px-4 md:px-6 py-6 md:py-8">
        <div className="mb-6">
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            AI-powered resume parsing and candidate analysis
          </p>
        </div>
        
        {/* Stats Cards */}
        <StatsCards stats={stats} />

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={handleTabChange} className="mt-6">
          <TabsList className="grid w-full max-w-4xl grid-cols-2 md:grid-cols-4 gap-1">
            <TabsTrigger value="resumes" className="text-xs md:text-sm">
              <Search className="mr-1 md:mr-2 h-3 md:h-4 w-3 md:w-4" />
              <span className="hidden sm:inline">Regular Search</span>
              <span className="sm:hidden">Search</span>
            </TabsTrigger>
            <TabsTrigger value="dtsearch" className="text-xs md:text-sm">
              <Zap className="mr-1 md:mr-2 h-3 md:h-4 w-3 md:w-4" />
              <span className="hidden sm:inline">Database Index Search</span>
              <span className="sm:hidden">DTSearch</span>
            </TabsTrigger>
            <TabsTrigger value="filesearch" className="text-xs md:text-sm">
              <File className="mr-1 md:mr-2 h-3 md:h-4 w-3 md:w-4" />
              <span className="hidden sm:inline">File Index Search</span>
              <span className="sm:hidden">Files</span>
            </TabsTrigger>
            <TabsTrigger value="upload" className="text-xs md:text-sm">
              <Upload className="mr-1 md:mr-2 h-3 md:h-4 w-3 md:w-4" />
              <span className="hidden sm:inline">Upload Resume</span>
              <span className="sm:hidden">Upload</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="resumes" className="mt-6">
            <div className="space-y-6">
              {/* Horizontal Search and Filters */}
                <SearchFilters
                  searchTerm={searchTerm}
                  onSearchChange={handleSearchChange}
                  selectedFilters={selectedFilters}
                  onFilterChange={handleFilterChange}
                  onClearFilters={handleClearFilters}
                  availableFilters={availableFilters}
                />

              {/* Resume List */}
              <div>
                <Card>
                  <CardHeader>
                    <CardTitle>Resume Database</CardTitle>
                    <CardDescription>
                      {hasActiveSearch
                        ? (() => {
                            const totalResults = pagination.count || 0;
                            const currentPage = pagination.currentPage || 1;
                            const pageSize = pagination.pageSize || 10;
                            const startResult = totalResults > 0 ? (currentPage - 1) * pageSize + 1 : 0;
                            const endResult = Math.min(currentPage * pageSize, totalResults);
                            
                            return totalResults > 0 
                              ? `Showing ${startResult} to ${endResult} of ${totalResults} results`
                              : 'No results found';
                          })()
                        : 'Enter search terms or apply filters to find resumes'
                      }
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Resume Grid - 2 Profiles Per Row */}
                    {loading ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        {[...Array(6)].map((_, i) => (
                          <Card key={i} className="animate-pulse">
                            <CardHeader>
                              <div className="h-4 bg-muted rounded w-3/4"></div>
                              <div className="h-3 bg-muted rounded w-1/2"></div>
                            </CardHeader>
                            <CardContent>
                              <div className="space-y-2">
                                <div className="h-3 bg-muted rounded"></div>
                                <div className="h-3 bg-muted rounded w-2/3"></div>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    ) : (filteredResumes && filteredResumes.length > 0) ? (
                      <>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                          {filteredResumes.map((resume) => (
                            <ResumeCard key={resume.id} resume={resume} />
                          ))}
                        </div>
                        
                        {/* Pagination Controls */}
                        {pagination.totalPages > 1 && (
                          <div className="flex items-center justify-between mt-8 pt-6 border-t">
                            <div className="text-sm text-muted-foreground">
                              Showing {((pagination.currentPage - 1) * pagination.pageSize) + 1} to {Math.min(pagination.currentPage * pagination.pageSize, pagination.count)} of {pagination.count} results
                            </div>
                            
                            <div className="flex items-center space-x-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={handlePreviousPage}
                                disabled={pagination.currentPage === 1}
                                className="flex items-center gap-1"
                              >
                                <ChevronLeft className="h-4 w-4" />
                                Previous
                              </Button>
                              
                              <div className="flex items-center space-x-1">
                                {/* Page numbers */}
                                {Array.from({ length: Math.min(5, pagination.totalPages) }, (_, i) => {
                                  let pageNum;
                                  if (pagination.totalPages <= 5) {
                                    pageNum = i + 1;
                                  } else if (pagination.currentPage <= 3) {
                                    pageNum = i + 1;
                                  } else if (pagination.currentPage >= pagination.totalPages - 2) {
                                    pageNum = pagination.totalPages - 4 + i;
                                  } else {
                                    pageNum = pagination.currentPage - 2 + i;
                                  }
                                  
                                  return (
                                    <Button
                                      key={pageNum}
                                      variant={pageNum === pagination.currentPage ? "default" : "outline"}
                                      size="sm"
                                      onClick={() => handlePageChange(pageNum)}
                                      className="w-8 h-8 p-0"
                                    >
                                      {pageNum}
                                    </Button>
                                  );
                                })}
                              </div>
                              
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={handleNextPage}
                                disabled={pagination.currentPage === pagination.totalPages}
                                className="flex items-center gap-1"
                              >
                                Next
                                <ChevronRight className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="text-center py-12">
                        <Search className="mx-auto h-12 w-12 text-muted-foreground" />
                        <h3 className="mt-4 text-lg font-semibold">
                          {hasActiveSearch ? 'No resumes found' : 'Ready to search'}
                        </h3>
                        <p className="text-muted-foreground">
                          {hasActiveSearch
                            ? 'Try adjusting your search criteria or filters'
                            : 'Use the search bar or filters above to find resumes'
                          }
                        </p>
                        {hasActiveSearch && (
                          <Button 
                            variant="outline" 
                            onClick={handleClearFilters}
                            className="mt-4"
                          >
                            Clear search and filters
                          </Button>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="dtsearch" className="mt-6">
            <DTSearchPanel />
          </TabsContent>

          <TabsContent value="filesearch" className="mt-6">
            <FileSearchPanel 
              onSelectResult={(result) => {
                // Open the file directly in a new tab/window
                if (result.file_path) {
                  // Set the selected file to display in the FileViewer
                  setSelectedFile(result);
                }
              }}
            />
          </TabsContent>

          <TabsContent value="upload" className="mt-6">
            <div className="max-w-4xl mx-auto">
              <Card>
                <CardHeader>
                  <CardTitle>Upload Resume</CardTitle>
                  <CardDescription>
                    Upload PDF, DOCX, or TXT files for AI-powered parsing
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <FileUploadZone 
                    onUpload={uploadResume} 
                    onBatchUpload={batchUploadResumes}
                  />
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* File Viewer Dialog */}
      {selectedFile && (
        <EnhancedFileViewer 
          filePath={selectedFile.file_path}
          fileName={selectedFile.filename}
          onClose={() => setSelectedFile(null)}
        />
      )}

      {/* DTSearch Result Dialog - Using proper Dialog component */}
    </div>
  )
}