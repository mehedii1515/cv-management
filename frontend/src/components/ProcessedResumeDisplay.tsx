'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { normalizeUrl } from '@/lib/utils'
import { CountryExperienceView } from './CountryExperienceView'
import { 
  User, 
  MapPin, 
  Building, 
  Mail, 
  Phone, 
  Calendar, 
  Briefcase,
  GraduationCap,
  Award,
  Languages,
  FileText,
  CheckCircle,
  Download,
  Eye,
  Clock,
  Users,
  StickyNote,
  ExternalLink,
  Linkedin,
  Globe,
  ClipboardList,
  Loader2,
  X,
  Info
} from 'lucide-react'
import { Resume } from '@/types/resume'
import { ExpertiseDetailsModal } from './ExpertiseDetailsModal'

interface ProcessedResumeDisplayProps {
  resume: Resume
  onClose?: () => void
  onDownload?: () => void
}

interface ExpertiseDetails {
  work_experience?: string
  projects?: string
  other_related_info?: string
  message?: string
  error?: string
}

export function ProcessedResumeDisplay({ resume, onClose, onDownload }: ProcessedResumeDisplayProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedExpertise, setSelectedExpertise] = useState('')
  const [expertiseDetails, setExpertiseDetails] = useState<ExpertiseDetails | null>(null)
  
  // Country experience modal state
  const [isCountryModalOpen, setIsCountryModalOpen] = useState(false)
  const [selectedCountry, setSelectedCountry] = useState('')
  const [countryExperiences, setCountryExperiences] = useState<any[]>([])

  const getInitials = (name: string) => {
    if (!name || name.trim() === '') return 'UN'
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return null
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  const fetchExpertiseDetails = async (expertiseArea: string) => {
    setIsLoading(true)
    setSelectedExpertise(expertiseArea)

    try {
    // Only use stored details from database
    const storedDetails = resume.expertise_details && resume.expertise_details[expertiseArea]
      
    if (storedDetails) {
        // Create a clean details object
        const filteredDetails: ExpertiseDetails = {}
        
        // Log the structure of the stored details for debugging
        console.log('Stored expertise details for', expertiseArea, ':', storedDetails);
        
        // Handle all possible keys that might contain useful information
        const possibleKeys = [
          'work_experience', 'projects', 'other_related_info',
          'message', 'error'
        ];
        
        // Process each key if it exists
        possibleKeys.forEach(key => {
          if (key in storedDetails && storedDetails[key as keyof typeof storedDetails] !== undefined) {
            // Cast to string - we'll handle parsing in the display function if needed
            filteredDetails[key as keyof ExpertiseDetails] = storedDetails[key as keyof typeof storedDetails] as string;
          }
        });
        
        // Special handling for empty arrays
        if ('work_experience' in storedDetails && Array.isArray(storedDetails.work_experience) && storedDetails.work_experience.length === 0) {
          filteredDetails.message = `No work experience information available for ${expertiseArea}`;
        }
        
        if ('projects' in storedDetails && Array.isArray(storedDetails.projects) && storedDetails.projects.length === 0) {
          if (!filteredDetails.message) {
            filteredDetails.message = `No projects information available for ${expertiseArea}`;
          } else {
            filteredDetails.message += `. No projects information available for ${expertiseArea}`;
          }
        }
        
        // If no standard keys were found, try to use any available key as work_experience
        if (Object.keys(filteredDetails).length === 0 && Object.keys(storedDetails).length > 0) {
          const firstKey = Object.keys(storedDetails)[0];
          if (firstKey && storedDetails[firstKey as keyof typeof storedDetails]) {
            filteredDetails.work_experience = storedDetails[firstKey as keyof typeof storedDetails] as string;
          }
        }
        
        // If we still have nothing, check if the entire object is a string or can be stringified
        if (Object.keys(filteredDetails).length === 0) {
          if (typeof storedDetails === 'string') {
            filteredDetails.work_experience = storedDetails;
          } else {
            try {
              filteredDetails.work_experience = JSON.stringify(storedDetails, null, 2);
            } catch (e) {
              // If all else fails, set an error message
              filteredDetails.error = 'Unable to parse expertise details';
            }
          }
        }
        
        // If we still have no useful information, provide a message
        if (Object.keys(filteredDetails).length === 0 || 
            (Object.keys(filteredDetails).length === 1 && 
             ('message' in filteredDetails || 'error' in filteredDetails))) {
          filteredDetails.message = `No detailed information available for ${expertiseArea}`;
        }
        
        console.log('Filtered expertise details:', filteredDetails);
        setExpertiseDetails(filteredDetails)
      setIsModalOpen(true)
    } else {
        console.log('No stored details found for expertise area:', expertiseArea);
      setExpertiseDetails({
        error: 'No details available',
        message: 'No stored details are available for this expertise area. Please re-upload or re-parse the resume to extract details.'
      })
      setIsModalOpen(true)
    }
    } catch (error) {
      console.error('Error fetching expertise details:', error);
      setExpertiseDetails({
        error: 'Error fetching details',
        message: 'An error occurred while fetching expertise details. Please try again.'
      });
      setIsModalOpen(true);
    } finally {
    setIsLoading(false)
    }
  }

  const closeModal = () => {
    setIsModalOpen(false)
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

  const formatStructuredText = (text: any) => {
    if (!text) return null;
    
    // Handle different data types
    if (typeof text === 'object') {
      try {
        // If it's already an object, format it as JSON
        return (
          <div className="space-y-6">
            {Array.isArray(text) ? (
              // Handle array of work experience or projects
              text.map((item, index) => (
                <div key={index} className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                  {/* Time Period */}
                  {item["Time Period"] && (
                    <div className="flex items-center mb-2">
                      <Clock className="h-4 w-4 text-primary mr-2" />
                      <span className="font-semibold text-primary">{item["Time Period"]}</span>
                    </div>
                  )}
                  
                  {/* Role/Title */}
                  {item["Role/Title"] && (
                    <div className="text-lg font-bold mb-1">{item["Role/Title"]}</div>
                  )}
                  
                  {/* Project Name */}
                  {item["Project Name"] && (
                    <div className="text-lg font-bold mb-1">{item["Project Name"]}</div>
                  )}
                  
                  {/* Organization */}
                  {item["Organization"] && (
                    <div className="flex items-center mb-2">
                      <Building className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{item["Organization"]}</span>
                    </div>
                  )}
                  
                  {/* Client/Organization */}
                  {item["Client/Organization"] && (
                    <div className="flex items-center mb-2">
                      <Users className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{item["Client/Organization"]}</span>
                    </div>
                  )}
                  
                  {/* Location */}
                  {item["Location"] && (
                    <div className="flex items-center mb-3">
                      <MapPin className="h-4 w-4 text-gray-600 mr-2" />
                      <span className="text-gray-700">{item["Location"].replace("Location: ", "")}</span>
                    </div>
                  )}
                  
                  {/* Responsibilities */}
                  {item["Responsibilities"] && (
                    <div className="mt-2">
                      <div className="font-semibold mb-1">Responsibilities:</div>
                      <ul className="list-disc pl-5 space-y-1 text-gray-700">
                        {Array.isArray(item["Responsibilities"]) ? (
                          item["Responsibilities"].map((resp, idx) => (
                            <li key={idx}>{resp}</li>
                          ))
                        ) : (
                          <li>{String(item["Responsibilities"])}</li>
                        )}
                      </ul>
                    </div>
                  )}
                  
                  {/* Description */}
                  {item["Description"] && (
                    <div className="mt-2">
                      <div className="font-semibold mb-1">Description:</div>
                      <ul className="list-disc pl-5 space-y-1 text-gray-700">
                        {Array.isArray(item["Description"]) ? (
                          item["Description"].map((desc, idx) => (
                            <li key={idx}>{desc}</li>
                          ))
                        ) : (
                          <li>{String(item["Description"])}</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            ) : (
              // For non-array objects, display in pretty format
              <pre className="p-4 bg-gray-50 rounded-md overflow-auto text-sm">
                {JSON.stringify(text, null, 2)}
              </pre>
            )}
          </div>
        );
      } catch (e) {
        // In case of error formatting object
        return (
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-gray-700">Error formatting data</p>
          </div>
        );
      }
    }
    
    // If it's a string, try to parse it as JSON
    if (typeof text === 'string') {
      try {
        // Try to parse as JSON
        const parsedJson = JSON.parse(text);
        return formatStructuredText(parsedJson);
      } catch (e) {
        // It's not JSON, check if it's formatted text with section markers
        if (text.includes("[Time Period]:") || text.includes("[Organization]:")) {
          // Try to extract structured data from formatted text
          try {
            // Split into separate entries by double newlines
            const entries = text.split(/\r?\n\r?\n+/).filter(Boolean);
            
            if (entries.length > 0) {
          return (
            <div className="space-y-6">
                  {entries.map((entry, index) => {
                    // Extract information using regex
                    const timeMatch = entry.match(/\[Time Period\]:\s*([^\n]+)/i);
                    const orgMatch = entry.match(/\[Organization\]:\s*([^\n]+)/i);
                    const locMatch = entry.match(/\[Location\]:\s*([^\n]+)/i);
                    const roleMatch = entry.match(/\[Role\/Title\]:\s*([^\n]+)/i);
                    
                    // Extract responsibilities
                    let responsibilities: string[] = [];
                    if (entry.includes("Responsibilities:")) {
                      const respPart = entry.split("Responsibilities:")[1];
                      if (respPart) {
                        responsibilities = respPart.split("\n")
                          .map(line => line.trim())
                          .filter(line => line.startsWith('-'))
                          .map(line => line.substring(1).trim());
                      }
                    }
                
                return (
                  <div key={index} className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                    {timeMatch && (
                      <div className="flex items-center mb-2">
                        <Clock className="h-4 w-4 text-primary mr-2" />
                        <span className="font-semibold text-primary">{timeMatch[1]}</span>
                      </div>
                    )}
                    
                    {roleMatch && (
                      <div className="text-lg font-bold mb-1">{roleMatch[1]}</div>
                    )}
                    
                    {orgMatch && (
                      <div className="flex items-center mb-2">
                        <Building className="h-4 w-4 text-gray-600 mr-2" />
                        <span className="text-gray-700">{orgMatch[1]}</span>
                      </div>
                    )}
                    
                    {locMatch && (
                      <div className="flex items-center mb-3">
                        <MapPin className="h-4 w-4 text-gray-600 mr-2" />
                        <span className="text-gray-700">{locMatch[1]}</span>
                      </div>
                    )}
                    
                        {responsibilities.length > 0 && (
                    <div className="mt-2">
                            <div className="font-semibold mb-1">Responsibilities:</div>
                            <ul className="list-disc pl-5 space-y-1 text-gray-700">
                              {responsibilities.map((resp, idx) => (
                                <li key={idx}>{resp}</li>
                              ))}
                            </ul>
                    </div>
                        )}
                  </div>
                );
              })}
            </div>
          );
            }
          } catch (parseError) {
            console.error("Error parsing formatted text:", parseError);
          }
        }
        
        // Default formatting for string content
          return (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
            <p className="whitespace-pre-wrap text-gray-700">{text}</p>
            </div>
          );
        }
      }
    
    // Fallback for any other types
    return (
      <div className="p-4 bg-gray-50 rounded-md">
        <p className="text-gray-700">Unable to display content</p>
      </div>
    );
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
            <p className="text-sm text-muted-foreground">
              Information extracted from {resume.full_name}'s resume
            </p>
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
    <div className="w-full p-6 space-y-6">
      {/* Success Header */}
      <Card className="border-green-200 bg-green-50">
        <CardHeader>
          <div className="flex items-center gap-3">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div>
              <CardTitle className="text-green-800">Resume Processed Successfully!</CardTitle>
              <CardDescription className="text-green-600">
                AI has extracted and structured the following information from the resume
              </CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Main Resume Information */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Avatar className="h-16 w-16">
                <AvatarImage src="" alt={resume.full_name || 'Unknown'} />
                <AvatarFallback className="bg-primary text-primary-foreground text-lg">
                  {getInitials(resume.full_name)}
                </AvatarFallback>
              </Avatar>
              <div>
                <CardTitle className="text-2xl">{resume.full_name || 'Unknown Name'}</CardTitle>
                <CardDescription className="text-lg">
                  {resume.current_employer && (
                    <span className="flex items-center gap-1">
                      <Building className="h-4 w-4" />
                      {resume.current_employer}
                    </span>
                  )}
                </CardDescription>
              </div>
            </div>
            <div className="flex gap-2">
              {onDownload && (
                <Button onClick={onDownload} variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              )}
              {onClose && (
                <Button onClick={onClose} variant="outline">
                  Close
                </Button>
              )}
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Personal Information */}
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <User className="h-5 w-5" />
              Personal Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resume.email && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{resume.email}</span>
                </div>
              )}
              {resume.phone_number && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{resume.phone_number}</span>
                </div>
              )}
              {resume.location && (
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{resume.location}</span>
                </div>
              )}
              {resume.age && (
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{resume.age} years old</span>
                </div>
              )}
              {resume.date_of_birth && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">Born: {formatDate(resume.date_of_birth)}</span>
                </div>
              )}
            </div>
          </div>

          <Separator />

          {/* Contact & Online Presence */}
          {(resume.linkedin_profile || resume.website_portfolio) && (
            <>
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <ExternalLink className="h-5 w-5" />
                  Online Presence
                </h3>
                <div className="flex flex-wrap gap-4">
                  {resume.linkedin_profile && (
                    <a 
                      href={normalizeUrl(resume.linkedin_profile) || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-3 py-2 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors"
                    >
                      <Linkedin className="h-4 w-4" />
                      LinkedIn Profile
                    </a>
                  )}
                  {resume.website_portfolio && (
                    <a 
                      href={normalizeUrl(resume.website_portfolio) || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-3 py-2 bg-green-50 text-green-700 rounded-md hover:bg-green-100 transition-colors"
                    >
                      <Globe className="h-4 w-4" />
                      Website/Portfolio
                    </a>
                  )}
                </div>
              </div>
              <Separator />
            </>
          )}

          {/* Professional Information */}
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Briefcase className="h-5 w-5" />
              Professional Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="font-medium">Experience Level:</span>
                <p className="text-muted-foreground">{resume.experience_level}</p>
              </div>
              {(resume.total_experience_years || resume.years_of_experience) && (
                <div>
                  <span className="font-medium">Total Experience:</span>
                  <p className="text-muted-foreground">
                    {resume.experience_display}
                  </p>
                </div>
              )}
              {resume.current_employer && (
                <div>
                  <span className="font-medium">Current Employer:</span>
                  <p className="text-muted-foreground">{resume.current_employer}</p>
                </div>
              )}
              {resume.availability && (
                <div>
                  <span className="font-medium">Availability:</span>
                  <p className="text-muted-foreground">{resume.availability}</p>
                </div>
              )}
              {resume.preferred_contract_type && (
                <div>
                  <span className="font-medium">Preferred Contract Type:</span>
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

          <Separator />

          {/* Experience Breakdown - COMMENTED OUT */}
          {/* {resume.expertise_experience && Object.keys(resume.expertise_experience).length > 0 && (
            <>
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Experience by Expertise Area
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(resume.expertise_experience).map(([area, experience], index) => (
                    <div key={index} className="p-3 border rounded bg-muted/30">
                      <div className="font-medium text-sm">{area}</div>
                      <div className="text-xs text-muted-foreground mt-1">{experience}</div>
                    </div>
                  ))}
                </div>
              </div>
              <Separator />
            </>
          )} */}

          {/* Skills and Expertise Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {/* Expertise Areas */}
            {resume.expertise_areas && resume.expertise_areas.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Expertise Areas
                  <span className="text-xs text-muted-foreground ml-2">
                    (click to see details)
                  </span>
                </h3>
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
                        
                        // Check if it has work_experience or projects keys, even if they're empty arrays
                        if ('work_experience' in details || 'projects' in details) {
                          return true;
                        }
                        
                        return Object.keys(details).length > 0;
                      }
                      
                      return false;
                    })
                    .map((area, index) => (
                    <Badge 
                      key={index} 
                      variant="default" 
                      className="text-sm cursor-pointer hover:bg-primary/80 transition-colors group relative"
                      onClick={() => fetchExpertiseDetails(area)}
                    >
                      <span className="flex items-center gap-1">
                      {area}
                        <ClipboardList className="h-3 w-3 opacity-70 group-hover:opacity-100" />
                      </span>
                      {isLoading && selectedExpertise === area && (
                        <Loader2 className="h-3 w-3 ml-1 animate-spin" />
                      )}
                    </Badge>
                  ))}
                </div>
                {resume.expertise_areas
                  .filter(area => {
                    // Check if this expertise area has details
                    const hasDetails = resume.expertise_details && 
                      resume.expertise_details[area] && 
                      Object.keys(resume.expertise_details[area]).length > 0;
                    
                    // Special handling for areas with empty arrays
                    if (hasDetails) {
                      const details = resume.expertise_details[area];
                      
                      // Check if it has work_experience or projects keys, even if they're empty arrays
                      if ('work_experience' in details || 'projects' in details) {
                        return true;
                      }
                      
                      return Object.keys(details).length > 0;
                    }
                    
                    return false;
                  }).length === 0 && (
                <p className="text-xs text-muted-foreground mt-2">
                    No detailed expertise information available
                </p>
                )}
              </div>
            )}

            {/* Industry Sectors */}
            {resume.sectors && resume.sectors.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Building className="h-5 w-5" />
                  Industry Sectors
                </h3>
                <div className="flex flex-wrap gap-2">
                  {resume.sectors.map((sector, index) => (
                    <Badge key={index} variant="secondary" className="text-sm">
                      {sector}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Skills */}
            {resume.skill_keywords && resume.skill_keywords.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <GraduationCap className="h-5 w-5" />
                  Skills & Keywords
                </h3>
                <div className="flex flex-wrap gap-2">
                  {resume.skill_keywords.slice(0, 15).map((skill, index) => (
                    <Badge key={index} variant="outline" className="text-sm">
                      {skill}
                    </Badge>
                  ))}
                  {resume.skill_keywords.length > 15 && (
                    <Badge variant="outline" className="text-xs">
                      +{resume.skill_keywords.length - 15} more
                    </Badge>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Country-wise Experience */}
          <CountryExperienceView resume={resume} onShowCountryExperience={showCountryExperience} />

          <Separator />

          {/* Additional Information Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Languages */}
            {resume.languages_spoken && resume.languages_spoken.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Languages className="h-5 w-5" />
                  Languages
                </h3>
                <div className="space-y-2">
                  {resume.languages_spoken.map((lang, index) => (
                    <div key={index} className="flex items-center justify-between p-2 border rounded">
                      <span className="font-medium">
                        {typeof lang === 'string' ? lang : lang.language}
                      </span>
                      {typeof lang === 'object' && lang.proficiency && (
                      <Badge variant="secondary" className="text-xs">
                        {lang.proficiency}
                      </Badge>
                      )}
                    </div>
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
                <div className="space-y-2">
                  {resume.professional_certifications.map((cert, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 border rounded">
                      <Award className="h-4 w-4 text-yellow-600" />
                      <span className="text-sm">{cert}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Professional Associations */}
          {resume.professional_associations && resume.professional_associations.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Users className="h-5 w-5" />
                Professional Associations
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {resume.professional_associations.map((association, index) => (
                  <div key={index} className="flex items-center gap-2 p-3 border rounded bg-muted/30">
                    <Users className="h-4 w-4 text-blue-600" />
                    <span className="text-sm">{association}</span>
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
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {resume.publications.map((pub, index) => (
                  <div key={index} className="p-3 border rounded bg-muted/50">
                    <p className="text-sm italic">{pub}</p>
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
              <div className="p-4 border rounded bg-muted/30">
                <p className="text-sm whitespace-pre-wrap">{resume.references}</p>
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
              <div className="p-4 border rounded bg-yellow-50">
                <p className="text-sm whitespace-pre-wrap">{resume.notes}</p>
              </div>
            </div>
          )}

          <Separator />

          {/* File Information */}
          <div>
            <h3 className="text-lg font-semibold mb-3">File Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="font-medium">Original Filename:</span>
                <p className="text-muted-foreground">{resume.original_filename}</p>
              </div>
              <div>
                <span className="font-medium">File Type:</span>
                <p className="text-muted-foreground">{resume.file_type?.toUpperCase()}</p>
              </div>
              <div>
                <span className="font-medium">Processing Status:</span>
                <Badge variant={resume.processing_status === 'completed' ? 'default' : 'destructive'}>
                  {resume.processing_status}
                </Badge>
              </div>
              <div>
                <span className="font-medium">Processed:</span>
                <p className="text-muted-foreground">
                  {new Date(resume.timestamp).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Expertise Details Modal */}
      <ExpertiseDetailsModal
        isOpen={isModalOpen}
        onClose={closeModal}
        expertiseArea={selectedExpertise}
        details={expertiseDetails || {}}
        candidateName={resume.full_name}
      />
      {renderCountryModal()}
    </div>
  )
} 