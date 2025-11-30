'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { X, Download, FileText, ExternalLink } from 'lucide-react'

interface EnhancedFileViewerProps {
  filePath: string | null
  fileName?: string
  onClose: () => void
}

export function EnhancedFileViewer({ filePath, fileName, onClose }: EnhancedFileViewerProps) {
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [open, setOpen] = useState<boolean>(!!filePath)
  const [fileType, setFileType] = useState<string>('')
  const [fileUrl, setFileUrl] = useState<string>('')

  useEffect(() => {
    setOpen(!!filePath)
    if (filePath) {
      const ext = filePath.split('.').pop()?.toLowerCase() || ''
      setFileType(ext)
      const url = `/api/search/files/view?path=${encodeURIComponent(filePath)}`
      setFileUrl(url)
      validateFileAccess(filePath)
    }
  }, [filePath])

  const validateFileAccess = async (path: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/search/files/view?path=${encodeURIComponent(path)}`, {
        method: 'HEAD', // Just check if file exists
      })
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`File not found: ${path}. The file may have been moved or deleted.`)
        } else {
          throw new Error(`Error accessing file: ${response.statusText}`)
        }
      }
    } catch (err) {
      console.error('File access error:', err)
      setError(err instanceof Error ? err.message : 'Failed to access file')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setOpen(false)
    onClose()
  }

  const openInNewTab = () => {
    window.open(fileUrl, '_blank')
  }

  const renderFileContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading file...</p>
          </div>
        </div>
      )
    }

    if (error) {
      return (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <FileText className="h-16 w-16 mx-auto text-red-400 mb-4" />
            <h3 className="text-lg font-medium text-red-600 mb-2">Error Loading File</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={handleClose} variant="outline">
              Close
            </Button>
          </div>
        </div>
      )
    }

    // PDF Files
    if (fileType === 'pdf') {
      return (
        <iframe 
          src={fileUrl}
          className="w-full h-full border-0"
          style={{ minHeight: '800px' }}
          title={fileName}
        />
      )
    }

    // DOCX and DOC Files - Show download option only
    if (fileType === 'docx' || fileType === 'doc') {
      const fileTypeUpper = fileType.toUpperCase()
      
      return (
        <div className="w-full h-full flex flex-col items-center justify-center text-center p-8">
          <div className="max-w-md space-y-6">
            <div className="flex justify-center">
              <FileText className="w-16 h-16 text-blue-600" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {fileTypeUpper} Document
              </h3>
              <p className="text-gray-600 mb-4">
                {fileName}
              </p>
              <p className="text-sm text-gray-500 mb-6">
                {fileTypeUpper} files cannot be previewed directly in the browser. 
                Please download the file to view it with Microsoft Word or a compatible application.
              </p>
            </div>
            <div className="flex gap-3 justify-center">
              <Button onClick={openInNewTab} className="flex items-center">
                <Download className="w-4 h-4 mr-2" />
                Download {fileTypeUpper} File
              </Button>
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )
    }    // Text Files
    if (fileType === 'txt' || fileType === 'rtf') {
      return (
        <div className="w-full h-full flex flex-col">
          <div className="flex justify-between items-center p-4 bg-gray-50 border-b">
            <span className="text-sm font-medium">{fileName}</span>
            <div className="flex gap-2">
              <Button size="sm" onClick={openInNewTab} variant="outline">
                <ExternalLink className="w-4 h-4 mr-2" />
                Open in New Tab
              </Button>
            </div>
          </div>
          <iframe 
            src={fileUrl}
            className="flex-1 border-0 w-full"
            style={{ minHeight: '500px' }}
            title={fileName}
          />
        </div>
      )
    }

    // Image Files
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(fileType)) {
      return (
        <div className="w-full h-full flex flex-col">
          <div className="flex justify-between items-center p-4 bg-gray-50 border-b">
            <span className="text-sm font-medium">{fileName}</span>
            <div className="flex gap-2">
              <Button size="sm" onClick={openInNewTab} variant="outline">
                <ExternalLink className="w-4 h-4 mr-2" />
                Open in New Tab
              </Button>
            </div>
          </div>
          <div className="flex-1 overflow-auto flex justify-center items-center bg-gray-50">
            <img src={fileUrl} alt={fileName} className="max-w-full h-auto" />
          </div>
        </div>
      )
    }

    // Unsupported file types
    return (
      <div className="text-center p-8">
        <div className="mb-4">
          <FileText className="h-16 w-16 mx-auto text-gray-400" />
        </div>
        <h3 className="text-lg font-medium mb-2">File Preview Not Available</h3>
        <p className="text-gray-600 mb-4">This file type cannot be displayed directly in the browser.</p>
        <div className="flex gap-2 justify-center">
          <Button onClick={openInNewTab} variant="outline">
            <ExternalLink className="w-4 h-4 mr-2" />
            Open in New Tab
          </Button>
          <Button asChild>
            <a href={fileUrl} download>
              <Download className="w-4 h-4 mr-2" />
              Download File
            </a>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="max-w-[95vw] max-h-[90vh] w-full h-full p-0 overflow-hidden">
        <DialogHeader className="p-4 border-b">
          <div className="flex items-center justify-between">
            <DialogTitle className="text-lg font-semibold truncate">
              {fileName || 'File Viewer'}
            </DialogTitle>
            <DialogClose asChild>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={handleClose}
                className="h-8 w-8 p-0"
              >
                <X className="h-4 w-4" />
              </Button>
            </DialogClose>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-hidden">
          {renderFileContent()}
        </div>
      </DialogContent>
    </Dialog>
  )
}
