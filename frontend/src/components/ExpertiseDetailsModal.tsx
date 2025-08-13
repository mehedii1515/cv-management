'use client'

import React from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  ClipboardList, 
  Briefcase, 
  FileText, 
  Info, 
  Award,
  GraduationCap,
  Settings,
  Star,
  BookOpen,
  Users,
  Languages,
  ChevronRight,
  Calendar,
  MapPin,
  Building
} from 'lucide-react'

interface ExpertiseDetailsModalProps {
  isOpen: boolean
  onClose: () => void
  expertiseArea: string
  details: {
    work_experience?: string
    projects?: string
    other_related_info?: string
    message?: string
    error?: string
  }
  candidateName: string
}

interface ParsedSection {
  title: string
  icon: React.ReactNode
  color: string
  items: string[]
}

export function ExpertiseDetailsModal({ 
  isOpen, 
  onClose, 
  expertiseArea, 
  details, 
  candidateName 
}: ExpertiseDetailsModalProps) {

  const formatStructuredText = (text: string) => {
    if (!text) return null;
    
    // Split by double newlines first to separate major sections
    const sections = text.split('\n\n').filter(section => section.trim());
    
    return (
      <div className="space-y-4">
        {sections.map((section, index) => {
          const lines = section.trim().split('\n');
          const isHeader = lines[0] && (
            lines[0].includes(':') && 
            !lines[0].startsWith('-') && 
            !lines[0].startsWith('•')
          );
          
          if (isHeader) {
            const [header, ...content] = lines;
            return (
              <div key={index} className="border-l-4 border-blue-400 pl-4">
                <h5 className="font-medium text-gray-800 mb-2">{header}</h5>
                <div className="space-y-1">
                  {content.map((line, idx) => (
                    <p key={idx} className="text-sm text-gray-700 leading-relaxed">
                      {line.trim()}
                    </p>
                  ))}
                </div>
              </div>
            );
          } else {
            return (
              <div key={index} className="space-y-1">
                {lines.map((line, idx) => (
                  <p key={idx} className="text-sm text-gray-700 leading-relaxed">
                    {line.trim()}
                  </p>
                ))}
              </div>
            );
          }
        })}
      </div>
    );
  };

  const parseOtherRelatedInfo = (info: string): ParsedSection[] => {
    if (!info) return [];
    
    const sections: ParsedSection[] = [];
    const lines = info.split('\n').filter(line => line.trim());
    
    let currentSection: ParsedSection | null = null;
    
    lines.forEach(line => {
      const trimmedLine = line.trim();
      if (trimmedLine.includes(':')) {
        const [key, ...valueParts] = trimmedLine.split(':');
        const value = valueParts.join(':').trim();
        const lowerKey = key.toLowerCase().trim();
        
        // Save previous section if exists
        if (currentSection && currentSection.items.length > 0) {
          sections.push(currentSection);
        }
        
        // Create new section with appropriate icon and color
        let icon: React.ReactNode = <Info className="h-4 w-4" />;
        let color = 'border-gray-400';
        
        if (lowerKey.includes('skills') || lowerKey.includes('technologies')) {
          icon = <Settings className="h-4 w-4" />;
          color = 'border-blue-400';
        } else if (lowerKey.includes('certification')) {
          icon = <Award className="h-4 w-4" />;
          color = 'border-yellow-400';
        } else if (lowerKey.includes('education') || lowerKey.includes('training')) {
          icon = <GraduationCap className="h-4 w-4" />;
          color = 'border-green-400';
        } else if (lowerKey.includes('tools') || lowerKey.includes('software')) {
          icon = <Settings className="h-4 w-4" />;
          color = 'border-purple-400';
        } else if (lowerKey.includes('achievement') || lowerKey.includes('award')) {
          icon = <Star className="h-4 w-4" />;
          color = 'border-orange-400';
        } else if (lowerKey.includes('publication') || lowerKey.includes('paper')) {
          icon = <BookOpen className="h-4 w-4" />;
          color = 'border-indigo-400';
        } else if (lowerKey.includes('association') || lowerKey.includes('member')) {
          icon = <Users className="h-4 w-4" />;
          color = 'border-pink-400';
        } else if (lowerKey.includes('language')) {
          icon = <Languages className="h-4 w-4" />;
          color = 'border-red-400';
        }
        
        currentSection = {
          title: key.trim(),
          icon,
          color,
          items: value ? [value] : []
        };
      } else if (currentSection && trimmedLine) {
        currentSection.items.push(trimmedLine);
      }
    });
    
    // Add the last section
    if (currentSection && (currentSection as ParsedSection).items.length > 0) {
      sections.push(currentSection as ParsedSection);
    }
    
    return sections;
  };

  const renderWorkExperience = (text: string) => {
    const sections = text.split('\n\n').filter(section => section.trim());
    
    return (
      <div className="space-y-6">
        {sections.map((section, index) => {
          const lines = section.trim().split('\n');
          const experienceData: { [key: string]: string } = {};
          let responsibilities: string[] = [];
          
          lines.forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine.includes(':')) {
              const [key, ...valueParts] = trimmedLine.split(':');
              const value = valueParts.join(':').trim();
              if (key.toLowerCase().includes('responsibilities')) {
                // Start collecting responsibilities
                if (value) responsibilities.push(value);
              } else {
                experienceData[key.trim()] = value;
              }
            } else if (trimmedLine.startsWith('-') || trimmedLine.startsWith('•')) {
              responsibilities.push(trimmedLine.substring(1).trim());
            } else if (responsibilities.length > 0) {
              // Continue collecting responsibilities
              responsibilities.push(trimmedLine);
            }
          });
          
          return (
            <div key={index} className="border border-blue-200 rounded-lg p-4 bg-gradient-to-br from-blue-50 to-white">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  {experienceData['Role/Title'] && (
                    <h5 className="font-semibold text-blue-800 mb-1">
                      {experienceData['Role/Title']}
                    </h5>
                  )}
                  {experienceData['Organization'] && (
                    <div className="flex items-center gap-2 text-sm text-blue-600 mb-1">
                      <Building className="h-3 w-3" />
                      {experienceData['Organization']}
                    </div>
                  )}
                  {experienceData['Location'] && (
                    <div className="flex items-center gap-2 text-sm text-blue-600 mb-1">
                      <MapPin className="h-3 w-3" />
                      {experienceData['Location']}
                    </div>
                  )}
                  {experienceData['Time Period'] && (
                    <div className="flex items-center gap-2 text-sm text-blue-600">
                      <Calendar className="h-3 w-3" />
                      {experienceData['Time Period']}
                    </div>
                  )}
                </div>
              </div>
              
              {responsibilities.length > 0 && (
                <div>
                  <h6 className="font-medium text-blue-700 mb-2">Key Responsibilities:</h6>
                  <ul className="space-y-1">
                    {responsibilities.map((resp, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-blue-600">
                        <ChevronRight className="h-3 w-3 mt-0.5 flex-shrink-0" />
                        {resp}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  const renderProjects = (text: string) => {
    const sections = text.split('\n\n').filter(section => section.trim());
    
    return (
      <div className="space-y-6">
        {sections.map((section, index) => {
          const lines = section.trim().split('\n');
          const projectData: { [key: string]: string } = {};
          let descriptions: string[] = [];
          
          lines.forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine.includes(':')) {
              const [key, ...valueParts] = trimmedLine.split(':');
              const value = valueParts.join(':').trim();
              if (key.toLowerCase().includes('description')) {
                if (value) descriptions.push(value);
              } else {
                projectData[key.trim()] = value;
              }
            } else if (trimmedLine.startsWith('-') || trimmedLine.startsWith('•')) {
              descriptions.push(trimmedLine.substring(1).trim());
            } else if (descriptions.length > 0) {
              descriptions.push(trimmedLine);
            }
          });
          
          return (
            <div key={index} className="border border-purple-200 rounded-lg p-4 bg-gradient-to-br from-purple-50 to-white">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  {projectData['Project Name'] && (
                    <h5 className="font-semibold text-purple-800 mb-1">
                      {projectData['Project Name']}
                    </h5>
                  )}
                  {projectData['Client/Organization'] && (
                    <div className="flex items-center gap-2 text-sm text-purple-600 mb-1">
                      <Building className="h-3 w-3" />
                      {projectData['Client/Organization']}
                    </div>
                  )}
                  {projectData['Time Period'] && (
                    <div className="flex items-center gap-2 text-sm text-purple-600">
                      <Calendar className="h-3 w-3" />
                      {projectData['Time Period']}
                    </div>
                  )}
                </div>
              </div>
              
              {descriptions.length > 0 && (
                <div>
                  <h6 className="font-medium text-purple-700 mb-2">Project Description:</h6>
                  <ul className="space-y-1">
                    {descriptions.map((desc, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-purple-600">
                        <ChevronRight className="h-3 w-3 mt-0.5 flex-shrink-0" />
                        {desc}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-5xl max-h-[85vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <ClipboardList className="h-5 w-5" />
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              {expertiseArea}
            </span>
            - Expertise Details
          </DialogTitle>
          <p className="text-sm text-muted-foreground">
            Information extracted from {candidateName}'s resume
          </p>
        </DialogHeader>
        
        <div className="space-y-6">
          {details.error ? (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{details.error}</p>
            </div>
          ) : details.message ? (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-yellow-700">{details.message}</p>
            </div>
          ) : (
            <>
              {details.work_experience && (
                <div>
                  <h4 className="font-semibold flex items-center gap-2 mb-4">
                    <Briefcase className="h-5 w-5 text-blue-600" />
                    Work Experience
                  </h4>
                  {renderWorkExperience(details.work_experience)}
                </div>
              )}
              
              {details.projects && (
                <div>
                  <h4 className="font-semibold flex items-center gap-2 mb-4">
                    <FileText className="h-5 w-5 text-purple-600" />
                    Projects
                  </h4>
                  {renderProjects(details.projects)}
                </div>
              )}
              
              {details.other_related_info && (
                <div>
                  <h4 className="font-semibold flex items-center gap-2 mb-4">
                    <Info className="h-5 w-5 text-green-600" />
                    Additional Information
                  </h4>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {parseOtherRelatedInfo(details.other_related_info).map((section, index) => (
                      <div key={index} className={`border-l-4 ${section.color} pl-4 bg-gray-50 p-3 rounded-r-lg`}>
                        <h5 className="font-medium text-gray-800 mb-2 flex items-center gap-2">
                          {section.icon}
                          {section.title}
                        </h5>
                        <div className="space-y-1">
                          {section.items.map((item, idx) => (
                            <Badge key={idx} variant="secondary" className="mr-1 mb-1 text-xs">
                              {item}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
        
        <div className="flex justify-end pt-4 border-t">
          <Button onClick={onClose} variant="outline">
            Close
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
