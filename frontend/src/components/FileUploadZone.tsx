'use client'

import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react'
import { ProcessedResumeDisplay } from './ProcessedResumeDisplay'
import { Resume } from '@/types/resume'

interface FileUploadZoneProps {
  onUpload: (file: File) => Promise<any>
  onBatchUpload?: (files: File[]) => Promise<any>
}

export function FileUploadZone({ onUpload, onBatchUpload }: FileUploadZoneProps) {
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('')
  const [processedResume, setProcessedResume] = useState<Resume | null>(null)
  const [batchResults, setBatchResults] = useState<BatchUploadResult[] | null>(null)
  const [batchSummary, setBatchSummary] = useState<BatchUploadSummary | null>(null)
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: UploadStatus }>({})
  
  // Batch upload interfaces
  interface UploadStatus {
    status: 'pending' | 'uploading' | 'success' | 'error' | 'duplicate'
    message: string
    resume?: Resume
  }
  
  interface BatchUploadResult {
    filename: string
    status: 'success' | 'duplicate' | 'error'
    resume_id?: string
    message: string
    error_details?: string
    resume_data?: Resume
  }
  
  interface BatchUploadSummary {
    total_files: number
    successful: number
    duplicates: number
    errors: number
    results: BatchUploadResult[]
  }

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    // Reset states
    setMessage('')
    setMessageType('')
    setProcessedResume(null)
    setBatchResults(null)
    setBatchSummary(null)
    setUploadProgress({})

    if (acceptedFiles.length === 1) {
      // Single file upload
      const file = acceptedFiles[0]
      setUploading(true)

      try {
        const result = await onUpload(file)
        
        if (result && result.data) {
          setProcessedResume(result.data)
          setMessage(`Successfully processed ${file.name}`)
          setMessageType('success')
        } else {
          setMessage(`Successfully uploaded ${file.name}`)
          setMessageType('success')
        }
      } catch (error) {
        setMessage(`Failed to upload ${file.name}: ${error}`)
        setMessageType('error')
        setProcessedResume(null)
      } finally {
        setUploading(false)
      }
    } else if (acceptedFiles.length > 1 && onBatchUpload) {
      // Batch upload
      setUploading(true)
      
      // Initialize progress tracking
      const initialProgress: { [key: string]: UploadStatus } = {}
      acceptedFiles.forEach(file => {
        initialProgress[file.name] = {
          status: 'pending',
          message: 'Queued for upload'
        }
      })
      setUploadProgress(initialProgress)

      try {
        const result = await onBatchUpload(acceptedFiles)
        
        if (result) {
          setBatchSummary(result)
          setBatchResults(result.results)
          
          // Update progress with final results
          const finalProgress: { [key: string]: UploadStatus } = {}
          result.results.forEach((fileResult: BatchUploadResult) => {
            finalProgress[fileResult.filename] = {
              status: fileResult.status as 'success' | 'error' | 'duplicate',
              message: fileResult.message,
              resume: fileResult.resume_data
            }
          })
          setUploadProgress(finalProgress)
          
          setMessage(`Batch upload completed: ${result.successful} successful, ${result.duplicates} duplicates, ${result.errors} errors`)
          setMessageType(result.errors === 0 ? 'success' : 'error')
        }
      } catch (error) {
        setMessage(`Batch upload failed: ${error}`)
        setMessageType('error')
        
        // Mark all as error
        const errorProgress: { [key: string]: UploadStatus } = {}
        acceptedFiles.forEach(file => {
          errorProgress[file.name] = {
            status: 'error',
            message: 'Upload failed'
          }
        })
        setUploadProgress(errorProgress)
      } finally {
        setUploading(false)
      }
    } else {
      // Multiple files but no batch upload handler
      setMessage('Multiple files selected but batch upload is not available')
      setMessageType('error')
    }
  }, [onUpload, onBatchUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: onBatchUpload ? 50 : 1, // Allow up to 50 files if batch upload is enabled
    maxSize: 10 * 1024 * 1024, // 10MB per file
    multiple: onBatchUpload ? true : false,
  })

  const handleDownload = async () => {
    if (!processedResume) return
    
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
      const response = await fetch(`${API_URL}/resumes/${processedResume.id}/download/`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = processedResume.original_filename || `${processedResume.full_name}_resume.pdf`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const handleClose = () => {
    setProcessedResume(null)
    setMessage('')
    setMessageType('')
  }

  const handleUploadAnother = () => {
    setProcessedResume(null)
    setBatchResults(null)
    setBatchSummary(null)
    setUploadProgress({})
    setMessage('')
    setMessageType('')
  }

  // Show processed resume if available
  if (processedResume) {
    return (
      <div className="space-y-4">
        <ProcessedResumeDisplay 
          resume={processedResume}
          onDownload={handleDownload}
          onClose={handleClose}
        />
        <div className="flex justify-center">
          <Button onClick={handleUploadAnother} variant="outline">
            Upload Another Resume
          </Button>
        </div>
      </div>
    )
  }

  // Show batch results if available
  if (batchSummary && batchResults) {
    return (
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Upload className="h-5 w-5" />
              <span>Batch Upload Results</span>
            </CardTitle>
            <CardDescription>
              Processed {batchSummary.total_files} files
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* Summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-600">{batchSummary.successful}</div>
                <div className="text-sm text-green-700">Successful</div>
              </div>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-yellow-600">{batchSummary.duplicates}</div>
                <div className="text-sm text-yellow-700">Duplicates</div>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-600">{batchSummary.errors}</div>
                <div className="text-sm text-red-700">Errors</div>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">{batchSummary.total_files}</div>
                <div className="text-sm text-blue-700">Total</div>
              </div>
            </div>

            {/* Individual Results */}
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {batchResults.map((result, index) => (
                <div key={index} className={`flex items-center justify-between p-3 rounded-lg border ${
                  result.status === 'success' ? 'bg-green-50 border-green-200' :
                  result.status === 'duplicate' ? 'bg-yellow-50 border-yellow-200' :
                  'bg-red-50 border-red-200'
                }`}>
                  <div className="flex items-center space-x-3">
                    {result.status === 'success' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : result.status === 'duplicate' ? (
                      <AlertCircle className="h-4 w-4 text-yellow-600" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-red-600" />
                    )}
                    <div>
                      <div className="font-medium text-sm">{result.filename}</div>
                      <div className="text-xs text-muted-foreground">{result.message}</div>
                      {result.error_details && (
                        <div className="text-xs text-red-600 mt-1">{result.error_details}</div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {result.status === 'success' && (
                      <Badge variant="secondary" className="text-green-700 bg-green-100">
                        Success
                      </Badge>
                    )}
                    {result.status === 'duplicate' && (
                      <Badge variant="secondary" className="text-yellow-700 bg-yellow-100">
                        Duplicate
                      </Badge>
                    )}
                    {result.status === 'error' && (
                      <Badge variant="destructive">
                        Error
                      </Badge>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        <div className="flex justify-center">
          <Button onClick={handleUploadAnother} variant="outline">
            Upload More Resumes
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardContent className="p-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary bg-primary/5'
                : 'border-muted-foreground/25 hover:border-primary/50'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">
              {isDragActive ? 
                (onBatchUpload ? 'Drop the files here' : 'Drop the file here') : 
                (onBatchUpload ? 'Upload Resumes (Batch)' : 'Upload Resume')
              }
            </h3>
            <p className="text-muted-foreground mb-4">
              {onBatchUpload ? 
                'Drag and drop resume files here, or click to select (up to 50 files)' :
                'Drag and drop a resume file here, or click to select'
              }
            </p>
            <div className="flex flex-wrap justify-center gap-2 text-sm text-muted-foreground">
              <span className="flex items-center">
                <FileText className="h-4 w-4 mr-1" />
                PDF
              </span>
              <span className="flex items-center">
                <FileText className="h-4 w-4 mr-1" />
                DOCX
              </span>
              <span className="flex items-center">
                <FileText className="h-4 w-4 mr-1" />
                TXT
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Maximum file size: 10MB
            </p>
          </div>
        </CardContent>
      </Card>

      {message && !processedResume && (
        <Card>
          <CardContent className="p-4">
            <div className={`flex items-center space-x-2 ${
              messageType === 'success' ? 'text-green-600' : 'text-red-600'
            }`}>
              {messageType === 'success' ? (
                <CheckCircle className="h-4 w-4" />
              ) : (
                <AlertCircle className="h-4 w-4" />
              )}
              <span className="text-sm">{message}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {uploading && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
              <span className="text-sm">Processing resume with AI...</span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
} 