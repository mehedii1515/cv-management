'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { MapPin } from 'lucide-react'
import { Resume } from '@/types/resume'

interface CountryExperienceViewProps {
  resume: Resume
  onShowCountryExperience?: (country: string, experiences: any[]) => void
}

interface WorkExperienceEntry {
  "Time Period"?: string
  "Organization"?: string
  "Location"?: string
  "Role/Title"?: string
  "Responsibilities"?: string[] | string
  "Achievements"?: string[] | string
  [key: string]: any
}

interface CountryExperiences {
  [country: string]: WorkExperienceEntry[]
}

export function CountryExperienceView({ resume, onShowCountryExperience }: CountryExperienceViewProps) {
  const [countryExperiences, setCountryExperiences] = useState<CountryExperiences>({})
  const [countries, setCountries] = useState<string[]>([])

  // Parse work experience entries from all expertise areas
  useEffect(() => {
    if (!resume.expertise_details) return
    
    const allCountries: Set<string> = new Set()
    const countryWiseExperiences: CountryExperiences = {}
    
    // Helper function to extract country from location string
    const extractCountry = (location: string): string | null => {
      if (!location) return null
      
      // Remove "Location: " prefix if present
      const cleanLocation = location.replace(/^Location:\s*/i, '').trim()
      
      // Split by comma and get the last part (usually country)
      const parts = cleanLocation.split(',').map(part => part.trim())
      
      // If we have multiple parts, last one is likely country
      if (parts.length > 1) {
        return parts[parts.length - 1]
      }
      
      // If only one part, it might be just a country name
      return parts[0]
    }
    
    // Function to process a single work experience entry
    const processExperienceEntry = (exp: any, areaName: string) => {
      // Skip if no location data
      if (!exp.Location && !exp.location) return
      
      // Get location from either Location or location field
      const locationStr = exp.Location || exp.location
      
      // Extract country
      const country = extractCountry(locationStr)
      
      // Skip if no country found or it's "Not specified"
      if (!country || country === 'Not specified') return
      
      // Add country to set
      allCountries.add(country)
      
      // Add experience to country
      if (!countryWiseExperiences[country]) {
        countryWiseExperiences[country] = []
      }
      
      // Add expertise area to the experience
      countryWiseExperiences[country].push({
        ...exp,
        "Expertise Area": areaName,
        "Country": country
      })
    }
    
    // Function to handle string data that might be JSON
    const parseExperienceData = (data: string | any): any[] => {
      // If it's already an array, return it
      if (Array.isArray(data)) return data
      
      // If it's a string, try to parse it as JSON
      if (typeof data === 'string') {
        try {
          const parsed = JSON.parse(data)
          return Array.isArray(parsed) ? parsed : [parsed]
        } catch (e) {
          // If it's not valid JSON, check if it contains multiple entries
          // (some entries might be formatted with multiple entries separated by markers)
          const entries = data.split(/(?:\r?\n){2,}/).filter(Boolean)
          if (entries.length > 1) {
            return entries.map(entry => {
              // Try to extract key information from text entries
              const timeMatch = entry.match(/Time Period:?\s*([^\n]+)/i)
              const orgMatch = entry.match(/Organization:?\s*([^\n]+)/i)
              const locMatch = entry.match(/Location:?\s*([^\n]+)/i)
              const roleMatch = entry.match(/Role\/Title:?\s*([^\n]+)/i)
              
              return {
                "Time Period": timeMatch ? timeMatch[1] : undefined,
                "Organization": orgMatch ? orgMatch[1] : undefined,
                "Location": locMatch ? locMatch[1] : undefined,
                "Role/Title": roleMatch ? roleMatch[1] : undefined,
                "Responsibilities": entry.includes("Responsibilities") ? 
                  entry.split("Responsibilities:")[1]?.trim() : undefined
              }
            })
          }
          // Return a simple object with the string data
          return [{ "work_experience": data }]
        }
      }
      
      // If it's an object but not array, wrap in array
      if (typeof data === 'object' && data !== null) {
        return [data]
      }
      
      return []
    }
    
    // Iterate through all expertise areas
    Object.keys(resume.expertise_details).forEach(area => {
      const details = resume.expertise_details[area]
      console.log(`Processing expertise area: ${area}`, details)
      
      // Try multiple approaches to find experience data
      
      // 1. Check for work_experience field
      if (details.work_experience) {
        try {
          const workExperienceData = parseExperienceData(details.work_experience)
          workExperienceData.forEach(exp => processExperienceEntry(exp, area))
          console.log(`Found ${workExperienceData.length} experiences in work_experience for ${area}`)
        } catch (error) {
          console.error(`Error parsing work experience for ${area}:`, error)
        }
      }
      
      // 2. Check for projects field which might contain location information
      if (details.projects) {
        try {
          const projectsData = parseExperienceData(details.projects)
          projectsData.forEach(exp => processExperienceEntry(exp, area))
          console.log(`Found ${projectsData.length} experiences in projects for ${area}`)
        } catch (error) {
          console.error(`Error parsing projects for ${area}:`, error)
        }
      }
      
      // 3. Try to find any other fields that might contain experience data
      // Some expertise details might directly contain arrays of experiences
      Object.keys(details).forEach(key => {
        // Skip already processed fields
        if (key === 'work_experience' || key === 'projects') return
        
        const value = (details as any)[key]
        if (Array.isArray(value)) {
          value.forEach(item => {
            // Check if item looks like an experience entry with location
            if (item && typeof item === 'object' && (item.Location || item.location)) {
              processExperienceEntry(item, area)
            }
          })
        }
      })
    })
    
    // Sort countries alphabetically
    const sortedCountries = Array.from(allCountries).sort()
    setCountries(sortedCountries)
    setCountryExperiences(countryWiseExperiences)
    
    console.log('Found experiences in these countries:', sortedCountries)
    console.log('Country-wise experience data:', countryWiseExperiences)
    
    // Don't set any default active tab
  }, [resume.expertise_details])

  // If no countries found
  if (countries.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            Country-wise Experience
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No country-specific experience information found in this resume.</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MapPin className="h-5 w-5" />
          Country-wise Experience
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Click on any country below to view work experiences in that location
        </p>
      </CardHeader>
      <CardContent>
        <Tabs>
          <TabsList className="mb-4 flex-wrap">
            {countries.map(country => (
              <TabsTrigger 
                key={country} 
                value={country}
                className="flex items-center gap-1 cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
                onClick={(e) => {
                  // Always prevent default tab switching
                  e.preventDefault();
                  if (onShowCountryExperience) {
                    onShowCountryExperience(country, countryExperiences[country] || []);
                  }
                }}
              >
                {country}
                <Badge variant="secondary" className="ml-1 text-xs">
                  {countryExperiences[country]?.length || 0}
                </Badge>
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </CardContent>
    </Card>
  )
} 