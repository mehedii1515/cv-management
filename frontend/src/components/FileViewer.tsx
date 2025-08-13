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
      
      // Handle text files directly
      if (contentType?.includes('text/') || contentType?.includes('application/json')) {
        const text = await response.text()
        setFileContent(text)
      } else if (contentType?.includes('image/')) {
        // For images, display them directly
        setFileContent(`<div class="flex justify-center"><img src="/api/search/files/view?path=${encodeURIComponent(path)}" alt="${fileName || 'Image'}" /></div>`)
      } else {
        // For non-text files, show a download link instead
        setFileContent(
          `<div class="text-center p-4">
            <p class="mb-4">This file type (${contentType || 'unknown'}) cannot be displayed directly in the browser.</p>
            <p>Please use the download button above to open this file.</p>
          </div>`
        )
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
      <DialogContent className="sm:max-w-[80%] max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader className="flex flex-row items-center justify-between">
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
        <div className="flex-1 overflow-auto p-4 border rounded-md bg-muted/50 mt-2">
          {loading ? (
            <div className="flex justify-center items-center h-full">
              <p>Loading file content...</p>
            </div>
          ) : error ? (
            <div className="text-destructive p-4">
              <p>{error}</p>
            </div>
          ) : fileContent.startsWith('<div') ? (
            <div dangerouslySetInnerHTML={{ __html: fileContent }} />
          ) : (
            <pre className="whitespace-pre-wrap break-words text-sm">{fileContent}</pre>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}