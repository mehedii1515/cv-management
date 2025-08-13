'use client'

import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileUploadZone } from '@/components/FileUploadZone'
import { useResumes } from '@/hooks/useResumes'

export default function UploadPage() {
  const { uploadResume, batchUploadResumes } = useResumes()

  return (
    <div className="bg-background min-h-screen">
      <div className="container mx-auto px-6 py-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Upload Resumes</CardTitle>
              <CardDescription>
                Upload PDF, DOCX, or TXT files for AI-powered parsing. You can upload multiple files at once for batch processing.
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
      </div>
    </div>
  )
} 