'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Progress } from '@/components/ui/progress'
import { CountryExperienceView } from './CountryExperienceView'
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { useToast } from '@/hooks/use-toast'
import { normalizeUrl } from '@/lib/utils'
import { 
  User, 
  MapPin, 
  Building, 
  Mail, 
  Phone, 
  Calendar, 
  MoreHorizontal,
  Download,
  Eye,
  ExternalLink,
  Briefcase,
  GraduationCap,
  Award,
  Languages,
  FileText,
  StickyNote,
  Linkedin,
  Globe,
  Clock,
  Users,
  ClipboardList,
  Loader2,
  Info
} from 'lucide-react'
import { Resume } from '@/types/resume'

interface ResumeCardProps {
  resume: Resume
  autoOpenDetails?: boolean
  onCloseDetails?: () => void
}

interface ExpertiseDetails {
  work_experience?: string
  projects?: string
  other_related_info?: string
  message?: string
  error?: string
}

export function ResumeCard({ resume, autoOpenDetails = false, onCloseDetails }: ResumeCardProps) {
  const { toast } = useToast()
  const [isDetailsOpen, setIsDetailsOpen] = useState(false) // Always start with false
  const [selectedExpertise, setSelectedExpertise] = useState<string>('')
  const [expertiseDetails, setExpertiseDetails] = useState<ExpertiseDetails | null>(null)
  const [isExpertiseModalOpen, setIsExpertiseModalOpen] = useState(false)
  const [isLoadingExpertise, setIsLoadingExpertise] = useState(false)
  
  // Country experience modal state
  const [isCountryModalOpen, setIsCountryModalOpen] = useState(false)
  const [selectedCountry, setSelectedCountry] = useState('')
  const [countryExperiences, setCountryExperiences] = useState<any[]>([])

  // Debug log
  console.log('ResumeCard rendered:', resume.full_name, 'autoOpenDetails:', autoOpenDetails)
  
  // Effect to update isDetailsOpen when autoOpenDetails changes
  // This ensures the dialog opens correctly when a new resume is selected  
  useEffect(() => {
    console.log('ResumeCard useEffect triggered:', autoOpenDetails)
    if (autoOpenDetails) {
      // Force the dialog to open with a small delay to ensure state is fresh
      setTimeout(() => {
        console.log('Opening dialog for:', resume.full_name)
        setIsDetailsOpen(true)
      }, 10)
    } else {
      setIsDetailsOpen(false)
    }
  }, [autoOpenDetails])

  const handleViewResume = () => {
    setIsDetailsOpen(true)
  }

  const handleViewResumeFile = async () => {
    if (!resume.file_path) {
      toast({
        title: "File Not Available",
        description: "Resume file is not available for viewing",
        variant: "destructive"
      })
      return
    }

    try {
      // First try to get the file through the download endpoint
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
      const response = await fetch(`${API_URL}/resumes/${resume.id}/download/`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
      
        // Open the blob URL in a new tab
        window.open(url, '_blank', 'noopener,noreferrer')
        
        // Clean up the blob URL after a delay
        setTimeout(() => window.URL.revokeObjectURL(url), 1000)
      
      toast({
        title: "Opening Resume",
        description: "Resume file is opening in a new tab",
          variant: "default" as const
      })
      } else {
        throw new Error('Could not retrieve file')
      }
    } catch (error) {
      toast({
        title: "View Failed",
        description: "Could not open the resume file",
        variant: "destructive" as const
      })
      console.error('Error viewing file:', error)
    }
  }

  const handleDownload = async () => {
    if (!resume.file_path) {
      toast({
        title: "File Not Available",
        description: "Resume file is not available for download",
        variant: "destructive" as const
      })
      return
    }

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
      const response = await fetch(`${API_URL}/resumes/${resume.id}/download/`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = resume.original_filename || `${resume.full_name}_resume.pdf`
        document.body.appendChild(a)
        a.click()
        
        // Clean up
        setTimeout(() => {
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        }, 1000)
        
        toast({
          title: "Download Complete",
          description: `Downloaded ${resume.full_name}'s resume`,
          variant: "default" as const
        })
      } else {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || 'Download failed')
      }
    } catch (error) {
      toast({
        title: "Download Failed",
        description: error instanceof Error ? error.message : "Could not download the resume file",
        variant: "destructive" as const
      })
      console.error('Download error:', error)
    }
  }



  const handleReparse = async () => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
      const response = await fetch(`${API_URL}/resumes/${resume.id}/reparse/`, {
        method: 'POST'
      })
      
      if (response.ok) {
        toast({
          title: "Reparse Started",
          description: "Resume is being re-parsed with AI",
        })
        // Refresh the page or update the data
        setTimeout(() => window.location.reload(), 2000)
      } else {
        throw new Error('Reparse failed')
      }
    } catch (error) {
      toast({
        title: "Reparse Failed",
        description: "Could not reparse the resume",
        variant: "destructive"
      })
    }
  }

  const fetchExpertiseDetails = async (expertiseArea: string) => {
    setIsLoadingExpertise(true)
    setSelectedExpertise(expertiseArea)

    console.log('Resume object:', resume);
    console.log('Expertise areas:', resume.expertise_areas);
    console.log('Expertise details object:', resume.expertise_details);
    console.log('Looking for expertise area:', expertiseArea);

    // Only use stored details from database
    const storedDetails = resume.expertise_details && resume.expertise_details[expertiseArea]
    if (storedDetails) {
      console.log('Stored expertise details:', storedDetails);
      
      // Handle the new structure with work_experience, projects, and other_related_info
      const filteredDetails: ExpertiseDetails = {
        work_experience: '',
        projects: '',
        other_related_info: '',
      }
      
      // Handle work_experience - could be string or object
      if (storedDetails.work_experience) {
        if (typeof storedDetails.work_experience === 'string') {
          filteredDetails.work_experience = storedDetails.work_experience;
        } else if (typeof storedDetails.work_experience === 'object') {
          // Convert object to formatted string
          try {
            filteredDetails.work_experience = JSON.stringify(storedDetails.work_experience, null, 2);
          } catch (e) {
            filteredDetails.work_experience = 'Error formatting work experience data';
          }
        }
      }
      
      // Handle projects - could be string or object
      if (storedDetails.projects) {
        if (typeof storedDetails.projects === 'string') {
          filteredDetails.projects = storedDetails.projects;
        } else if (typeof storedDetails.projects === 'object') {
          // Convert object to formatted string
          try {
            filteredDetails.projects = JSON.stringify(storedDetails.projects, null, 2);
          } catch (e) {
            filteredDetails.projects = 'Error formatting projects data';
          }
        }
      }

      // Handle other_related_info - new field with additional expertise evidence
      if (storedDetails.other_related_info) {
        if (typeof storedDetails.other_related_info === 'string') {
          filteredDetails.other_related_info = storedDetails.other_related_info;
        } else if (typeof storedDetails.other_related_info === 'object') {
          // Convert object to formatted string
          try {
            filteredDetails.other_related_info = JSON.stringify(storedDetails.other_related_info, null, 2);
          } catch (e) {
            filteredDetails.other_related_info = 'Error formatting other related info data';
          }
        }
      }
      
      // Add error/message if they exist
      if ('error' in storedDetails && storedDetails.error) {
        filteredDetails.error = String(storedDetails.error);
      }
      
      if ('message' in storedDetails && storedDetails.message) {
        filteredDetails.message = String(storedDetails.message);
      }
      
      console.log('Filtered expertise details:', filteredDetails);
      setExpertiseDetails(filteredDetails)
      setIsExpertiseModalOpen(true)
    } else {
      console.log('No stored details found for expertise area:', expertiseArea);
      setExpertiseDetails({
        error: 'No details available',
        message: 'No stored details are available for this expertise area. Please re-upload or re-parse the resume to extract details.'
      })
      setIsExpertiseModalOpen(true)
    }
    setIsLoadingExpertise(false)
  }

  const closeExpertiseModal = () => {
    setIsExpertiseModalOpen(false)
    setSelectedExpertise('')
    setExpertiseDetails(null)
  }
  
  // Function to handle country experience popup
  const showCountryExperience = (country: string, experiences: any[]) => {
    setSelectedCountry(country)
    setCountryExperiences(experiences)
    setIsCountryModalOpen(true)
  }
  
  // Function to close country modal
  const closeCountryModal = () => {
    setIsCountryModalOpen(false)
    setSelectedCountry('')
    setCountryExperiences([])
  }

  const getInitials = (name: string) => {
    if (!name || name.trim() === '') return 'UN'
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }

  const getExperienceProgress = (years: number | null) => {
    if (!years) return 0
    // Assuming max 20 years for progress calculation
    return Math.min((years / 20) * 100, 100)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500'
      case 'processing': return 'bg-yellow-500'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const knownKeys = [
    'work_experience',
    'projects',
    'error',
    'message'
  ]

  const formatKey = (key: string) => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (l) => l.toUpperCase())
  }

  // Function to format structured text with highlighting
  const formatStructuredText = (text: string) => {
    if (!text || typeof text !== 'string') return null;
    
    // Check if the text is a JSON string
    if (text.trim().startsWith('{') || text.trim().startsWith('[')) {
      try {
        // Try to parse JSON
        const jsonData = JSON.parse(text);
        
        // Handle array of work experience or projects
        if (Array.isArray(jsonData)) {
          return (
            <div className="space-y-4">
              {jsonData.map((item, index) => (
                <div key={index} className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 hover:shadow-md transition-shadow">
                  {/* Time Period */}
                  {item["Time Period"] && (
                    <div className="flex items-center mb-2">
                      <Clock className="h-4 w-4 text-primary mr-2" />
                      <span className="font-semibold text-primary">{item["Time Period"]}</span>
                    </div>
                  )}
                  
                  {/* Role/Title */}
                  {item["Role/Title"] && (
                    <div className="text-lg font-bold mb-2 text-gray-800">{item["Role/Title"]}</div>
                  )}
                  
                  {/* Project Name */}
                  {item["Project Name"] && (
                    <div className="text-lg font-bold mb-2 text-gray-800">{item["Project Name"]}</div>
                  )}
                  
                  {/* Organization */}
                  {item["Organization"] && (
                    <div className="flex items-center mb-2">
                      <Building className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700 font-medium">{item["Organization"]}</span>
                    </div>
                  )}
                  
                  {/* Client/Organization */}
                  {item["Client/Organization"] && (
                    <div className="flex items-center mb-2">
                      <Users className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700 font-medium">{item["Client/Organization"]}</span>
                    </div>
                  )}
                  
                  {/* Location */}
                  {item["Location"] && (
                    <div className="flex items-center mb-3">
                      <MapPin className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{item["Location"].replace(/^Location:\s*/i, "")}</span>
                    </div>
                  )}
                  
                  {/* Responsibilities */}
                  {item["Responsibilities"] && item["Responsibilities"].length > 0 && (
                    <div className="mt-3 p-3 bg-gray-50 rounded-md">
                      <div className="font-semibold mb-2 text-gray-800 flex items-center">
                        <ClipboardList className="h-4 w-4 mr-1" />
                        Responsibilities:
                      </div>
                      <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                        {Array.isArray(item["Responsibilities"]) ? (
                          item["Responsibilities"].map((resp: string, idx: number) => (
                            <li key={idx} className="leading-relaxed">{resp}</li>
                          ))
                        ) : (
                          <li className="leading-relaxed">{String(item["Responsibilities"])}</li>
                        )}
                      </ul>
                    </div>
                  )}
                  
                  {/* Description */}
                  {item["Description"] && item["Description"].length > 0 && (
                    <div className="mt-3 p-3 bg-blue-50 rounded-md">
                      <div className="font-semibold mb-2 text-gray-800 flex items-center">
                        <FileText className="h-4 w-4 mr-1" />
                        Description:
                      </div>
                      <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                        {Array.isArray(item["Description"]) ? (
                          item["Description"].map((desc: string, idx: number) => (
                            <li key={idx} className="leading-relaxed">{desc}</li>
                          ))
                        ) : (
                          <li className="leading-relaxed">{String(item["Description"])}</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          );
        }
        
        // Handle single object (not an array)
        return (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
            {Object.entries(jsonData).map(([key, value]) => (
              <div key={key} className="mb-3">
                <div className="font-semibold text-gray-800 mb-1">{key}</div>
                <div className="text-gray-700 ml-4 whitespace-pre-wrap text-sm leading-relaxed">
                  {typeof value === 'string' ? value : JSON.stringify(value, null, 2)}
                </div>
              </div>
            ))}
          </div>
        );
      } catch (e) {
        console.log('Failed to parse as JSON, using enhanced text formatting');
      }
    }
    
    // Enhanced text parsing for non-JSON content
    const parseTextContent = (content: string) => {
      // Split by double newlines to separate entries
      const entries = content.split(/\n\s*\n/).filter(entry => entry.trim());
      
      if (entries.length > 1) {
        return (
          <div className="space-y-4">
            {entries.map((entry, index) => (
              <div key={index} className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 hover:shadow-md transition-shadow">
                {formatSingleEntry(entry)}
              </div>
            ))}
          </div>
        );
      } else {
        return (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
            {formatSingleEntry(content)}
          </div>
        );
      }
    };
    
    const formatSingleEntry = (entry: string) => {
      const lines = entry.split('\n').map(line => line.trim()).filter(line => line);
      let formattedContent: JSX.Element[] = [];
      
      lines.forEach((line, index) => {
        // Check if line contains a colon (likely a field)
        if (line.includes(':') && !line.startsWith('-')) {
          const [key, ...valueParts] = line.split(':');
          const value = valueParts.join(':').trim();
          
          // Special formatting for different field types
          if (key.toLowerCase().includes('time') || key.toLowerCase().includes('period') || key.toLowerCase().includes('duration')) {
            formattedContent.push(
              <div key={index} className="flex items-center mb-2">
                <Clock className="h-4 w-4 text-primary mr-2" />
                <span className="font-semibold text-primary">{value}</span>
              </div>
            );
          } else if (key.toLowerCase().includes('role') || key.toLowerCase().includes('title') || key.toLowerCase().includes('position')) {
            formattedContent.push(
              <div key={index} className="text-lg font-bold mb-2 text-gray-800">{value}</div>
            );
          } else if (key.toLowerCase().includes('organization') || key.toLowerCase().includes('company') || key.toLowerCase().includes('client')) {
            formattedContent.push(
              <div key={index} className="flex items-center mb-2">
                <Building className="h-4 w-4 text-gray-600 mr-2" />
                <span className="text-gray-700 font-medium">{value}</span>
              </div>
            );
          } else if (key.toLowerCase().includes('location')) {
            formattedContent.push(
              <div key={index} className="flex items-center mb-3">
                <MapPin className="h-4 w-4 text-gray-600 mr-2" />
                <span className="text-gray-700">{value}</span>
              </div>
            );
          } else {
            formattedContent.push(
              <div key={index} className="mb-2">
                <span className="font-semibold text-gray-800">{key.trim()}:</span>
                <span className="text-gray-700 ml-2">{value}</span>
              </div>
            );
          }
        } else if (line.startsWith('-') || line.startsWith('•')) {
          // Handle bullet points
          const bulletText = line.replace(/^[-•]\s*/, '');
          formattedContent.push(
            <div key={index} className="flex items-start mb-1">
              <span className="text-primary mr-2">•</span>
              <span className="text-gray-700 text-sm leading-relaxed">{bulletText}</span>
            </div>
          );
        } else {
          // Regular text line
          if (line.trim()) {
            formattedContent.push(
              <div key={index} className="text-gray-700 mb-1 leading-relaxed">
                {line}
              </div>
            );
          }
        }
      });
      
      return <div className="space-y-1">{formattedContent}</div>;
    };
    
    return parseTextContent(text);
  };

  const renderExpertiseModal = () => {
    if (!expertiseDetails || !selectedExpertise) return null

    return (
      <Dialog open={isExpertiseModalOpen} onOpenChange={closeExpertiseModal}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <ClipboardList className="h-5 w-5" />
              {selectedExpertise} - Expertise Details
            </DialogTitle>
            <DialogDescription>
              Information extracted directly from {resume.full_name}'s resume
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6">
            {expertiseDetails.error ? (
              <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-700">{expertiseDetails.error}</p>
              </div>
            ) : expertiseDetails.message ? (
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="text-yellow-700">{expertiseDetails.message}</p>
              </div>
            ) : (
              <>
                {expertiseDetails.work_experience && expertiseDetails.work_experience !== "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <Briefcase className="h-4 w-4" />
                      Work Experience
                    </h4>
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
                      {formatStructuredText(expertiseDetails.work_experience)}
                    </div>
                  </div>
                ) : expertiseDetails.work_experience === "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <Briefcase className="h-4 w-4" />
                      Work Experience
                    </h4>
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-yellow-700">No information found for {selectedExpertise} work experience.</p>
                    </div>
                  </div>
                ) : null}
                
                {expertiseDetails.projects && expertiseDetails.projects !== "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <FileText className="h-4 w-4" />
                      Projects
                    </h4>
                    <div className="p-4 bg-purple-50 border border-purple-200 rounded-md">
                      {formatStructuredText(expertiseDetails.projects)}
                    </div>
                  </div>
                ) : expertiseDetails.projects === "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <FileText className="h-4 w-4" />
                      Projects
                    </h4>
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-yellow-700">No information found for {selectedExpertise} projects.</p>
                    </div>
                  </div>
                ) : null}

                {expertiseDetails.other_related_info && expertiseDetails.other_related_info !== "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <Award className="h-4 w-4" />
                      Additional Evidence & Qualifications
                    </h4>
                    <div className="p-4 bg-green-50 border border-green-200 rounded-md">
                      {formatStructuredText(expertiseDetails.other_related_info)}
                    </div>
                  </div>
                ) : expertiseDetails.other_related_info === "No information found" ? (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-2">
                      <Award className="h-4 w-4" />
                      Additional Evidence & Qualifications
                    </h4>
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-yellow-700">No additional evidence found for {selectedExpertise}.</p>
                    </div>
                  </div>
                ) : null}

                {/* Enhanced informational message when all sections are empty */}
                {expertiseDetails.work_experience === "No information found" && 
                 expertiseDetails.projects === "No information found" && 
                 expertiseDetails.other_related_info === "No information found" && (
                  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                    <div className="flex flex-col gap-3">
                      <p className="text-yellow-700 font-medium">
                        No detailed evidence found for {selectedExpertise}.
                      </p>
                      <p className="text-yellow-700 text-sm">
                        This expertise area may be listed but lacks specific supporting information in the resume such as:
                      </p>
                      <ul className="list-disc pl-5 text-yellow-700 text-sm">
                        <li>Relevant work experience or job roles</li>
                        <li>Projects demonstrating this expertise</li>
                        <li>Certifications, education, or skills in this area</li>
                        <li>Tools, technologies, or achievements related to this field</li>
                      </ul>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
          
          <div className="flex justify-end pt-4">
            <Button onClick={closeExpertiseModal} variant="outline">
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    )
  }
  
  // Render country experience modal
  const renderCountryModal = () => {
    if (!countryExperiences.length || !selectedCountry) return null
    
    return (
      <Dialog open={isCountryModalOpen} onOpenChange={closeCountryModal}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              Experience in {selectedCountry}
            </DialogTitle>
            <DialogDescription>
              Information extracted from {resume.full_name}'s resume
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6">
            {countryExperiences.map((exp, idx) => (
              <Card key={idx} className="mb-4">
                <CardContent className="pt-6">
                  {/* Time Period */}
                  {exp["Time Period"] && (
                    <div className="flex items-center mb-2">
                      <Clock className="h-4 w-4 text-primary mr-2" />
                      <span className="font-medium text-primary">{exp["Time Period"]}</span>
                    </div>
                  )}
                  
                  {/* Role/Title */}
                  {exp["Role/Title"] && (
                    <div className="text-lg font-bold mb-1">{exp["Role/Title"]}</div>
                  )}
                  
                  {/* Organization */}
                  {exp["Organization"] && (
                    <div className="flex items-center mb-2">
                      <Building className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{exp["Organization"]}</span>
                    </div>
                  )}
                  
                  {/* Location */}
                  {exp["Location"] && (
                    <div className="flex items-center mb-3">
                      <MapPin className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{exp["Location"].replace(/^Location:\s*/i, "")}</span>
                    </div>
                  )}
                  
                  {/* Expertise Area Badge */}
                  {exp["Expertise Area"] && (
                    <Badge className="mb-3" variant="secondary">
                      {exp["Expertise Area"]}
                    </Badge>
                  )}
                  
                  {/* Responsibilities */}
                  {exp["Responsibilities"] && (
                    <div className="mt-2">
                      <div className="font-medium mb-1">Responsibilities:</div>
                      <ul className="list-disc pl-5 space-y-1 text-gray-700">
                        {Array.isArray(exp["Responsibilities"]) ? (
                          exp["Responsibilities"].map((resp: string, respIdx: number) => (
                            <li key={respIdx}>{resp}</li>
                          ))
                        ) : (
                          <li>{String(exp["Responsibilities"])}</li>
                        )}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="flex justify-end pt-4">
            <Button onClick={closeCountryModal} variant="outline">
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <>
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Avatar className="h-12 w-12">
                  <AvatarImage src="" alt={resume.full_name || 'Unknown'} />
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    {getInitials(resume.full_name)}
                  </AvatarFallback>
                </Avatar>
                <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${getStatusColor(resume.processing_status)}`} 
                     title={`Status: ${resume.processing_status}`} />
              </div>
              <div>
                <CardTitle className="text-lg">{resume.full_name || 'Unknown Name'}</CardTitle>
                <CardDescription className="flex items-center mt-1">
                  <Building className="h-3 w-3 mr-1" />
                  {resume.current_employer || 'Not specified'}
                </CardDescription>
              </div>
            </div>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={handleViewResume}>
                  <Eye className="mr-2 h-4 w-4" />
                  View Details
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleViewResumeFile}>
                  <Eye className="mr-2 h-4 w-4" />
                  View Resume
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleDownload}>
                  <Download className="mr-2 h-4 w-4" />
                  Download
                </DropdownMenuItem>
                {resume.processing_status === 'failed' && (
                  <DropdownMenuItem onClick={handleReparse}>
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Reparse
                  </DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Experience Level Progress */}
          {(resume.years_of_experience || resume.total_experience_months) && (
            <div className="mt-3">
              <div className="flex justify-between text-sm mb-1">
                <span>Experience Level</span>
                <span>{resume.experience_display}</span>
              </div>
              <Progress value={getExperienceProgress(resume.years_of_experience || Math.floor((resume.total_experience_months || 0) / 12))} className="h-2" />
            </div>
          )}
        </CardHeader>

        <CardContent className="space-y-3">
          {/* Contact Information */}
          <div className="space-y-2 text-sm">
            {resume.email && (
              <div className="flex items-center text-muted-foreground">
                <Mail className="h-3 w-3 mr-2" />
                {resume.email}
              </div>
            )}
            {resume.phone_number && (
              <div className="flex items-center text-muted-foreground">
                <Phone className="h-3 w-3 mr-2" />
                {resume.phone_number}
              </div>
            )}
            {resume.location && (
              <div className="flex items-center text-muted-foreground">
                <MapPin className="h-3 w-3 mr-2" />
                {resume.location}
              </div>
            )}
            {resume.age && (
              <div className="flex items-center text-muted-foreground">
                <User className="h-3 w-3 mr-2" />
                {resume.age} years old
              </div>
            )}
          </div>

          <Separator />

          {/* Skills */}
          {resume.skill_keywords && Array.isArray(resume.skill_keywords) && resume.skill_keywords.length > 0 ? (
            <div>
              <h4 className="text-sm font-medium mb-2">Top Skills</h4>
              <div className="flex flex-wrap gap-1">
                {resume.skill_keywords.slice(0, 6).map((skill, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
                {resume.skill_keywords.length > 6 && (
                  <Badge variant="outline" className="text-xs">
                    +{resume.skill_keywords.length - 6} more
                  </Badge>
                )}
              </div>
            </div>
          ) : (
            <div className="text-sm text-muted-foreground">
              No skills extracted yet
            </div>
          )}

          {/* Expertise Areas */}
          {resume.expertise_areas && resume.expertise_areas.length > 0 && (
            <div>
              <h4 className="text-sm font-medium mb-2">Expertise Areas</h4>
              <div className="flex flex-wrap gap-2">
                {resume.expertise_areas
                  .filter(area => {
                    // Check if this expertise area has details
                    const hasDetails = resume.expertise_details && 
                      resume.expertise_details[area] && 
                      Object.keys(resume.expertise_details[area]).length > 0;
                    
                    // Special handling for areas with empty arrays
                    if (hasDetails) {
                      const details = resume.expertise_details[area];
                      
                      // Check if it has work_experience, projects, or other_related_info keys
                      if ('work_experience' in details || 'projects' in details || 'other_related_info' in details) {
                        return true;
                      }
                      
                      return Object.keys(details).length > 0;
                    }
                    
                    return false;
                  })
                  .slice(0, 3)
                  .map((area, index) => {
                    const details = resume.expertise_details?.[area];
                    const hasWorkExp = details?.work_experience && details.work_experience !== "No information found";
                    const hasProjects = details?.projects && details.projects !== "No information found";
                    const hasOtherInfo = details?.other_related_info && details.other_related_info !== "No information found";
                    
                    const evidenceCount = [hasWorkExp, hasProjects, hasOtherInfo].filter(Boolean).length;
                    
                    return (
                      <div key={index} className="group relative">
                        <Badge 
                          variant="default" 
                          className="text-xs cursor-pointer hover:bg-primary/80 transition-colors pr-8"
                          onClick={() => fetchExpertiseDetails(area)}
                        >
                          <span className="flex items-center gap-1">
                            {area}
                            {evidenceCount > 0 && (
                              <span className="bg-white/20 rounded-full px-1 text-[10px] font-medium">
                                {evidenceCount}
                              </span>
                            )}
                          </span>
                          {isLoadingExpertise && selectedExpertise === area && (
                            <Loader2 className="h-2 w-2 ml-1 animate-spin absolute right-1" />
                          )}
                        </Badge>
                        
                        {/* Evidence indicators - show on hover */}
                        <div className="absolute -top-1 -right-1 flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                          {hasWorkExp && <div className="w-1.5 h-1.5 bg-blue-600 rounded-full" title="Work Experience"></div>}
                          {hasProjects && <div className="w-1.5 h-1.5 bg-purple-600 rounded-full" title="Projects"></div>}
                          {hasOtherInfo && <div className="w-1.5 h-1.5 bg-green-600 rounded-full" title="Additional Evidence"></div>}
                        </div>
                      </div>
                    )
                  })}
                {resume.expertise_areas
                  .filter(area => {
                    // Check if this expertise area has details
                    const hasDetails = resume.expertise_details && 
                      resume.expertise_details[area] && 
                      Object.keys(resume.expertise_details[area]).length > 0;
                    
                    // Special handling for areas with empty arrays
                    if (hasDetails) {
                      const details = resume.expertise_details[area];
                      
                      // Check if it has work_experience, projects, or other_related_info keys
                      if ('work_experience' in details || 'projects' in details || 'other_related_info' in details) {
                        return true;
                      }
                      
                      return Object.keys(details).length > 0;
                    }
                    
                    return false;
                  }).length > 3 && (
                  <Badge variant="outline" className="text-xs">
                    +{resume.expertise_areas
                      .filter(area => {
                        // Check if this expertise area has details
                        const hasDetails = resume.expertise_details && 
                          resume.expertise_details[area] && 
                          Object.keys(resume.expertise_details[area]).length > 0;
                        
                        // Special handling for areas with empty arrays
                        if (hasDetails) {
                          const details = resume.expertise_details[area];
                          
                          // Check if it has work_experience, projects, or other_related_info keys
                          if ('work_experience' in details || 'projects' in details || 'other_related_info' in details) {
                            return true;
                          }
                          
                          return Object.keys(details).length > 0;
                        }
                        
                        return false;
                      }).length - 3} more
                  </Badge>
                )}
              </div>
            </div>
          )}

          <Separator />

          {/* Action Buttons */}
          <div className="flex gap-2 pt-2">
            <Button size="sm" className="flex-1" onClick={handleViewResume}>
              <Eye className="h-3 w-3 mr-1" />
              Details
            </Button>
            <Button size="sm" variant="outline" onClick={handleViewResumeFile}>
              <FileText className="h-3 w-3 mr-1" />
              View Resume
            </Button>
            <Button size="sm" variant="outline" onClick={handleDownload}>
              <Download className="h-3 w-3 mr-1" />
              Download
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Resume Details Dialog */}
      <Dialog open={isDetailsOpen} onOpenChange={(open) => {
        setIsDetailsOpen(open)
        if (!open && onCloseDetails) {
          onCloseDetails()
        }
      }}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Avatar className="h-8 w-8">
                <AvatarFallback>{getInitials(resume.full_name)}</AvatarFallback>
              </Avatar>
              {resume.full_name || 'Unknown Name'}
            </DialogTitle>
            <DialogDescription>
              Complete resume details and information
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6">
            {/* Personal Information */}
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <User className="h-5 w-5" />
                Personal Information
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Email:</span>
                  <p className="text-muted-foreground">{resume.email || 'Not provided'}</p>
                </div>
                <div>
                  <span className="font-medium">Phone:</span>
                  <p className="text-muted-foreground">{resume.phone_number || 'Not provided'}</p>
                </div>
                <div>
                  <span className="font-medium">Location:</span>
                  <p className="text-muted-foreground">{resume.location || 'Not provided'}</p>
                </div>
                <div>
                  <span className="font-medium">Age:</span>
                  <p className="text-muted-foreground">{resume.age ? `${resume.age} years old` : 'Not provided'}</p>
                </div>
                <div>
                  <span className="font-medium">Total Experience:</span>
                  <p className="text-muted-foreground">
                    {resume.experience_display}
                  </p>
                </div>
                {resume.date_of_birth && (
                  <div>
                    <span className="font-medium">Date of Birth:</span>
                    <p className="text-muted-foreground">
                      {new Date(resume.date_of_birth).toLocaleDateString()}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Online Presence */}
            {(resume.linkedin_profile || resume.website_portfolio) && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <ExternalLink className="h-5 w-5" />
                  Online Presence
                </h3>
                <div className="flex flex-wrap gap-2">
                  {resume.linkedin_profile && (
                    <a 
                      href={normalizeUrl(resume.linkedin_profile) || '#'}
                      target="_blank"  
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
                    >
                      <Linkedin className="h-4 w-4" />
                      LinkedIn
                    </a>
                  )}
                  {resume.website_portfolio && (
                    <a 
                      href={normalizeUrl(resume.website_portfolio) || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-sm text-green-600 hover:text-green-800"
                    >
                      <Globe className="h-4 w-4" />
                      Portfolio
                    </a>
                  )}
                </div>
              </div>
            )}

            {/* Professional Information */}
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Professional Information
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Current Employer:</span>
                  <p className="text-muted-foreground">{resume.current_employer || 'Not provided'}</p>
                </div>
                <div>
                  <span className="font-medium">Experience Level:</span>
                  <p className="text-muted-foreground">{resume.experience_level}</p>
                </div>
                {resume.availability && (
                  <div>
                    <span className="font-medium">Availability:</span>
                    <p className="text-muted-foreground">{resume.availability}</p>
                  </div>
                )}
                {resume.preferred_contract_type && (
                  <div>
                    <span className="font-medium">Contract Type:</span>
                    <p className="text-muted-foreground">{resume.preferred_contract_type}</p>
                  </div>
                )}
                {resume.preferred_work_arrangement && (
                  <div>
                    <span className="font-medium">Work Arrangement:</span>
                    <p className="text-muted-foreground">{resume.preferred_work_arrangement}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Skills and Expertise */}
            {(Array.isArray(resume.skill_keywords) && resume.skill_keywords.length > 0 || resume.expertise_areas?.length > 0 || resume.sectors?.length > 0) && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Skills & Expertise
                </h3>
                {resume.expertise_areas?.length > 0 && (
                  <div className="mb-3">
                    <span className="font-medium text-sm">Expertise Areas:</span>
                    <div className="space-y-1 mt-2">
                      {resume.expertise_areas.map((area, index) => {
                        const details = resume.expertise_details?.[area];
                        const hasWorkExp = details?.work_experience && details.work_experience !== "No information found";
                        const hasProjects = details?.projects && details.projects !== "No information found";
                        const hasOtherInfo = details?.other_related_info && details.other_related_info !== "No information found";
                        
                        const evidenceCount = [hasWorkExp, hasProjects, hasOtherInfo].filter(Boolean).length;
                        
                        return (
                          <div key={index} className="group">
                            <div 
                              className="flex items-center justify-between p-2 rounded-md border hover:bg-muted/30 cursor-pointer transition-colors"
                              onClick={() => fetchExpertiseDetails(area)}
                            >
                              <div className="flex items-center gap-2">
                                <Badge 
                                  variant="default" 
                                  className="text-xs"
                                >
                                  {area}
                                </Badge>
                                {evidenceCount > 0 && (
                                  <div className="text-xs text-muted-foreground">
                                    {evidenceCount} source{evidenceCount > 1 ? 's' : ''} of evidence
                                  </div>
                                )}
                              </div>
                              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                {hasWorkExp && <div title="Work Experience"><Briefcase className="h-3 w-3 text-blue-600" /></div>}
                                {hasProjects && <div title="Projects"><FileText className="h-3 w-3 text-purple-600" /></div>}
                                {hasOtherInfo && <div title="Additional Evidence"><Award className="h-3 w-3 text-green-600" /></div>}
                                <ClipboardList className="h-3 w-3 text-muted-foreground ml-1" />
                                {isLoadingExpertise && selectedExpertise === area && (
                                  <Loader2 className="h-3 w-3 ml-1 animate-spin" />
                                )}
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
                {resume.sectors?.length > 0 && (
                  <div className="mb-3">
                    <span className="font-medium text-sm">Industry Sectors:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {resume.sectors.map((sector, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {sector}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
                {Array.isArray(resume.skill_keywords) && resume.skill_keywords.length > 0 && (
                  <div>
                    <span className="font-medium text-sm">Skills:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {resume.skill_keywords.map((skill, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Country-wise Experience */}
            <CountryExperienceView resume={resume} onShowCountryExperience={showCountryExperience} />

            {/* Languages */}
            {resume.languages_spoken && resume.languages_spoken.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Languages className="h-5 w-5" />
                  Languages
                </h3>
                <div className="flex flex-wrap gap-2">
                  {resume.languages_spoken.map((lang, index) => (
                    <Badge key={index} variant="secondary" className="text-sm">
                      {typeof lang === 'string' ? lang : lang.language}
                      {typeof lang === 'object' && lang.proficiency && ` (${lang.proficiency})`}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Certifications */}
            {resume.professional_certifications && resume.professional_certifications.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Professional Certifications
                </h3>
                <div className="space-y-1">
                  {resume.professional_certifications.map((cert, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm">
                      <Award className="h-3 w-3 text-yellow-600" />
                      <span>{cert}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Professional Associations */}
            {resume.professional_associations && resume.professional_associations.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Professional Associations
                </h3>
                <div className="space-y-1">
                  {resume.professional_associations.map((association, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm">
                      <Users className="h-3 w-3 text-blue-600" />
                      <span>{association}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Publications */}
            {resume.publications && resume.publications.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Publications
                </h3>
                <div className="space-y-2">
                  {resume.publications.map((pub, index) => (
                    <div key={index} className="p-2 border rounded bg-muted/50 text-sm italic">
                      {pub}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* References */}
            {resume.references && resume.references.trim() && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  References
                </h3>
                <div className="p-3 border rounded bg-muted/30 text-sm whitespace-pre-wrap">
                  {resume.references}
                </div>
              </div>
            )}

            {/* Notes */}
            {resume.notes && resume.notes.trim() && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <StickyNote className="h-5 w-5" />
                  Additional Notes
                </h3>
                <div className="p-3 border rounded bg-yellow-50 text-sm whitespace-pre-wrap">
                  {resume.notes}
                </div>
              </div>
            )}

            {/* File Information */}
            <div>
              <h3 className="text-lg font-semibold mb-3">File Information</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Filename:</span>
                  <p className="text-muted-foreground">{resume.original_filename}</p>
                </div>
                <div>
                  <span className="font-medium">File Type:</span>
                  <p className="text-muted-foreground">{resume.file_type?.toUpperCase()}</p>
                </div>
                <div>
                  <span className="font-medium">Status:</span>
                  <p className="text-muted-foreground capitalize">{resume.processing_status}</p>
                </div>
                <div>
                  <span className="font-medium">Uploaded:</span>
                  <p className="text-muted-foreground">
                    {new Date(resume.timestamp).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 pt-4 border-t">
              <Button onClick={handleDownload} className="flex-1">
                <Download className="h-4 w-4 mr-2" />
                Download Resume
              </Button>
              {resume.processing_status === 'failed' && (
                <Button onClick={handleReparse} variant="secondary">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Reparse
                </Button>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Expertise Details Modal */}
      {renderExpertiseModal()}

      {/* Country Experience Modal */}
      {renderCountryModal()}
    </>
  )
}