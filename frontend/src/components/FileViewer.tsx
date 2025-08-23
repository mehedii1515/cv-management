'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { X, Download, FileText } from 'lucide-react'

interface FileViewerProps {
  filePath: string | null
  fileName?: string
  onClose: () => void
}

export function FileViewer({ filePath, fileName, onClose }: FileViewerProps) {
  const [fileContent, setFileContent] = useState<string>('')
  const [fileType, setFileType] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [open, setOpen] = useState<boolean>(!!filePath)

  useEffect(() => {
    setOpen(!!filePath)
    if (filePath) {
      fetchFileContent(filePath)
    }
  }, [filePath])

  const fetchFileContent = async (path: string) => {
    setLoading(true)
    setError(null)
    setFileType('')
    try {
      const response = await fetch(`/api/search/files/view?path=${encodeURIComponent(path)}`, {
        method: 'GET',
      })
      
      if (!response.ok) {
        console.error(`Error fetching file: ${response.status} ${response.statusText}`)
        // If we get a 404, provide a more helpful error message
        if (response.status === 404) {
          throw new Error(`File not found: ${path}. The file may have been moved or deleted.`)
        } else {
          throw new Error(`Error fetching file: ${response.statusText}`)
        }
      }
      
      const contentType = response.headers.get('content-type')
      console.log('File content type:', contentType)
      
      // Handle different file types for direct display
      if (contentType?.includes('application/pdf')) {
        // Display PDF using iframe/embed
        setFileType('pdf')
        setFileContent(`/api/search/files/view?path=${encodeURIComponent(path)}`)
      } else if (contentType?.includes('application/vnd.openxmlformats-officedocument.wordprocessingml.document') || 
                 contentType?.includes('application/msword')) {
        // For DOCX/DOC files, we'll extract the text content instead of using external viewers
        setFileType('docx')
        // Try to get the extracted text content from the backend
        try {
          const textResponse = await fetch(`/api/search/files/content?path=${encodeURIComponent(path)}`)
          if (textResponse.ok) {
            const textData = await textResponse.json()
            if (textData.extracted_text) {
              setFileContent(textData.extracted_text)
              return
            }
          }
        } catch (err) {
          console.log('Could not get extracted text, falling back to download option')
        }
        
        // Fallback: set the file URL for download
        setFileContent(`/api/search/files/view?path=${encodeURIComponent(path)}`)
      } else if (contentType?.includes('text/') || contentType?.includes('application/json')) {
        // Handle text files directly
        setFileType('text')
        const text = await response.text()
        setFileContent(text)
      } else if (contentType?.includes('image/')) {
        // For images, display them directly
        setFileType('image')
        setFileContent(`/api/search/files/view?path=${encodeURIComponent(path)}`)
      } else {
        // For other file types, provide download option
        setFileType('other')
        setFileContent(`This file type (${contentType || 'unknown'}) cannot be displayed directly in the browser.`)
      }
    } catch (err) {
      console.error('File fetch error:', err)
      setError(err instanceof Error ? err.message : 'Failed to load file')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setOpen(false)
    onClose()
  }

  const handleDownload = () => {
    if (filePath) {
      window.open(`/api/search/files/view?path=${encodeURIComponent(filePath)}`, '_blank')
    }
  }

  return (
    <Dialog open={open} onOpenChange={(open) => {
      if (!open) handleClose()
    }}>
      <DialogContent className="w-[95vw] max-w-[95vw] h-[90vh] max-h-[90vh] overflow-hidden flex flex-col p-0">
        <DialogHeader className="flex flex-row items-center justify-between px-6 py-4 border-b">
          <DialogTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            {fileName || filePath?.split('/').pop() || 'File Viewer'}
          </DialogTitle>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="icon" onClick={handleDownload}>
              <Download className="h-4 w-4" />
            </Button>
            <DialogClose asChild>
              <Button variant="outline" size="icon" onClick={handleClose}>
                <X className="h-4 w-4" />
              </Button>
            </DialogClose>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-hidden">
          {loading ? (
            <div className="flex justify-center items-center h-full">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                <p>Loading file content...</p>
              </div>
            </div>
          ) : error ? (
            <div className="text-destructive p-4 text-center">
              <p className="mb-2">{error}</p>
              <Button variant="outline" onClick={() => filePath && fetchFileContent(filePath)}>
                Try Again
              </Button>
            </div>
          ) : fileType === 'pdf' ? (
            <div className="w-full h-full">
              <iframe 
                src={fileContent}
                className="w-full h-full border-0"
                title={fileName || 'PDF Document'}
                style={{ minHeight: 'calc(90vh - 80px)' }}
              >
                <p>Your browser does not support PDF display. <a href={fileContent} target="_blank" rel="noopener noreferrer">Click here to view the PDF</a></p>
              </iframe>
            </div>
          ) : fileType === 'docx' ? (
            <div className="w-full h-full p-4">
              {/* Check if we have extracted text content */}
              {fileContent && !fileContent.startsWith('/api/') ? (
                // Display extracted text content
                <div className="h-full">
                  <div className="bg-white p-6 rounded border h-full overflow-auto">
                    <div className="prose max-w-none">
                      <pre className="whitespace-pre-wrap break-words text-sm leading-relaxed font-sans">
                        {fileContent}
                      </pre>
                    </div>
                  </div>
                </div>
              ) : (
                // Fallback: Show download options
                <div className="h-full flex items-center justify-center">
                  <div className="text-center max-w-md">
                    <div className="mb-6">
                      <FileText className="h-16 w-16 mx-auto mb-4 text-blue-500" />
                      <h3 className="text-lg font-medium mb-2">Document Preview Unavailable</h3>
                      <p className="text-gray-600 mb-4">
                        This Word document cannot be previewed directly in the browser. 
                        The document content may be available in the search results, or you can download it to view.
                      </p>
                    </div>
                    
                    <div className="space-y-3">
                      <Button 
                        onClick={handleDownload}
                        className="w-full"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Download & Open File
                      </Button>
                      
                      <div className="text-sm text-gray-500">
                        <p>You can also try these online viewers:</p>
                        <div className="flex gap-2 justify-center mt-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => {
                              const fullUrl = window.location.origin + fileContent
                              const encodedUrl = encodeURIComponent(fullUrl)
                              window.open(`https://docs.google.com/gview?url=${encodedUrl}`, '_blank')
                            }}
                          >
                            Google Docs Viewer
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => {
                              const fullUrl = window.location.origin + fileContent
                              const encodedUrl = encodeURIComponent(fullUrl)
                              window.open(`https://view.officeapps.live.com/op/view.aspx?src=${encodedUrl}`, '_blank')
                            }}
                          >
                            Office Online
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : fileType === 'image' ? (
            <div className="flex justify-center items-center h-full p-4">
              <img 
                src={fileContent} 
                alt={fileName || 'Image'} 
                className="max-w-full max-h-full object-contain rounded"
              />
            </div>
          ) : fileType === 'text' ? (
            <div className="h-full p-4">
              <pre className="whitespace-pre-wrap break-words text-sm font-mono bg-white p-4 rounded border overflow-auto h-full">
                {fileContent}
              </pre>
            </div>
          ) : (
            <div className="text-center p-8 h-full flex items-center justify-center">
              <div className="max-w-md mx-auto">
                <p className="mb-4 text-lg font-medium">Preview Not Available</p>
                <p className="mb-4 text-gray-600">{fileContent}</p>
                <Button onClick={handleDownload}>
                  Download File
                </Button>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}