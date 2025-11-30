'use client'

import React, { useEffect, useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Building, 
  Calendar, 
  Award,
  FileText,
  X 
} from 'lucide-react'

interface DTSearchResult {
  id: string
  name: string
  email: string
  phone: string
  location: string
  current_employer: string
  years_of_experience: number
  skills: string
  experience: string
  summary: string
  score: number
}

interface DTSearchResultDialogProps {
  result: DTSearchResult | null
  onClose: () => void
}

export function DTSearchResultDialog({ result, onClose }: DTSearchResultDialogProps) {
  const [open, setOpen] = useState<boolean>(!!result)

  useEffect(() => {
    setOpen(!!result)
  }, [result])

  const handleClose = () => {
    setOpen(false)
    onClose()
  }

  if (!result) return null

  // Parse skills from comma-separated string
  const skillsList = result.skills 
    ? result.skills.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
    : []

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle className="text-2xl font-bold">{result.name || 'Resume Details'}</DialogTitle>
            <Badge variant="outline" className="text-sm">
              Match Score: {result.score.toFixed(2)}
            </Badge>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          {/* Contact Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {result.email && (
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{result.email}</span>
              </div>
            )}
            {result.phone && (
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{result.phone}</span>
              </div>
            )}
            {result.location && (
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{result.location}</span>
              </div>
            )}
            {result.current_employer && (
              <div className="flex items-center gap-2">
                <Building className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{result.current_employer}</span>
              </div>
            )}
          </div>

          {/* Experience */}
          {result.years_of_experience > 0 && (
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm">
                {result.years_of_experience} years of experience
              </span>
            </div>
          )}

          <Separator />

          {/* Summary */}
          {result.summary && (
            <div>
              <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
                <User className="h-5 w-5" />
                Summary
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {result.summary}
              </p>
            </div>
          )}

          {/* Skills */}
          {skillsList.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Award className="h-5 w-5" />
                Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {skillsList.map((skill, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Experience Details */}
          {result.experience && (
            <div>
              <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Experience
              </h3>
              <div className="bg-muted/50 p-4 rounded-md">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {result.experience}
                </p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end space-x-2 pt-4 border-t">
            <Button variant="outline" onClick={handleClose}>
              Close
            </Button>
            <Button onClick={() => window.open(`mailto:${result.email}`, '_blank')}>
              Contact Candidate
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
