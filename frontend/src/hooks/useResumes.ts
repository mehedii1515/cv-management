'use client'

import { useState, useEffect, useCallback } from 'react'
import { Resume, ResumeStats } from '@/types/resume'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export function useResumes() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [stats, setStats] = useState<ResumeStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [pagination, setPagination] = useState({
    count: 0,
    next: null as string | null,
    previous: null as string | null,
    currentPage: 1,
    totalPages: 1,
    pageSize: 10
  })
  const [filterOptions, setFilterOptions] = useState<{
    expertise: string[]
    locations: string[]
    sectors: string[]
    skills: string[]
    experienceLevels: string[]
  }>({
    expertise: [],
    locations: [],
    sectors: [],
    skills: [],
    experienceLevels: []
  })

  // Fetch resumes from API with search and filter support
  const fetchResumes = useCallback(async (searchTerm?: string, filters?: any, page: number = 1, pageSize: number = 10) => {
    try {
      setLoading(true)
      
      // Build query parameters
      const params = new URLSearchParams()
      
      // Add pagination parameters
      params.append('page', page.toString())
      params.append('page_size', pageSize.toString())
      
      if (searchTerm?.trim()) {
        params.append('search', searchTerm.trim())
      }
      
      if (filters) {
        // Add filter parameters
        filters.expertise?.forEach((exp: string) => {
          params.append('expertise_areas', exp)
        })
        
        filters.location?.forEach((loc: string) => {
          params.append('location', loc)
        })
        
        filters.sectors?.forEach((sector: string) => {
          params.append('sectors', sector)
        })
        
        filters.skills?.forEach((skill: string) => {
          params.append('skills', skill)
        })
        
        filters.experience?.forEach((exp: string) => {
          params.append('experience', exp)
        })
      }
      
      const queryString = params.toString()
      const url = `${API_URL}/resumes/${queryString ? `?${queryString}` : ''}`
      
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch resumes`)
      }
      const data = await response.json()
      
      // Handle paginated response
      const results = data.results || data
      const validResumes = (Array.isArray(results) ? results : []).filter((resume: Resume) => 
        resume.processing_status !== 'failed'
      )
      
      setResumes(validResumes)
      
      // Update pagination info
      if (data.count !== undefined) {
        setPagination({
          count: data.count,
          next: data.next,
          previous: data.previous,
          currentPage: page,
          totalPages: Math.ceil(data.count / pageSize),
          pageSize: pageSize
        })
      } else {
        // Fallback for non-paginated response
        setPagination({
          count: validResumes.length,
          next: null,
          previous: null,
          currentPage: 1,
          totalPages: 1,
          pageSize: validResumes.length
        })
      }
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setResumes([])
    } finally {
      setLoading(false)
    }
  }, [])

  // Fetch statistics
  const fetchStats = useCallback(async () => {
    try {
      console.log('Fetching stats from:', `${API_URL}/resumes/stats/`)
      const response = await fetch(`${API_URL}/resumes/stats/`)
      console.log('Stats response status:', response.status)
      if (!response.ok) {
        throw new Error(`Failed to fetch stats: ${response.status}`)
      }
      const data = await response.json()
      console.log('Stats data received:', data)
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
      // Create mock stats if API fails
      const mockStats = {
        total_resumes: 0,
        processed_resumes: 0,
        pending_resumes: 0,
        failed_resumes: 0,
        processing_rate: 0,
        top_expertise_areas: [],
        top_locations: []
      }
      console.log('Setting mock stats:', mockStats)
      setStats(mockStats)
    }
  }, [])

  // Fetch filter options from API
  const fetchFilterOptions = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/resumes/filter_options/`)
      if (!response.ok) {
        throw new Error(`Failed to fetch filter options: ${response.status}`)
      }
      const data = await response.json()
      setFilterOptions(data)
    } catch (err) {
      console.error('Failed to fetch filter options:', err)
      // Keep existing filter options if API fails
    }
  }, [])

  // Upload resume
  const uploadResume = useCallback(async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_URL}/resumes/upload/`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      
      // Handle specific error cases with user-friendly messages
      if (errorData.detail && errorData.detail.includes("overloaded")) {
        throw new Error(`The AI service is currently overloaded. Please try again in a few minutes.`)
      } else if (errorData.detail && errorData.detail.includes("quota")) {
        throw new Error(`AI service quota exceeded. Please try again later.`)
      } else if (errorData.error === 'Identical resume already exists') {
        throw new Error(`This resume already exists in the system.`)
      } else {
        throw new Error(errorData.error || errorData.detail || 'Failed to upload resume')
      }
    }

    const result = await response.json()
    
    // Refresh the resumes list - go back to first page
    await fetchResumes()
    
    // Refresh filter options in case new sectors were added
    await fetchFilterOptions()
    
    return result
  }, [fetchResumes, fetchFilterOptions])

  // Batch upload resumes
  const batchUploadResumes = useCallback(async (files: File[]) => {
    const formData = new FormData()
    
    // Append all files
    files.forEach((file) => {
      formData.append('files', file)
    })

    const response = await fetch(`${API_URL}/resumes/batch_upload/`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      
      // Handle specific error cases with user-friendly messages
      if (errorData.detail && errorData.detail.includes("overloaded")) {
        throw new Error(`The AI service is currently overloaded. Please try again in a few minutes.`)
      } else if (errorData.detail && errorData.detail.includes("quota")) {
        throw new Error(`AI service quota exceeded. Please try again later.`)
      } else {
        throw new Error(errorData.error || errorData.detail || 'Failed to upload resumes')
      }
    }

    const result = await response.json()
    
    // Refresh the resumes list and stats - go back to first page
    await fetchResumes()
    await fetchStats()
    
    // Refresh filter options in case new sectors were added
    await fetchFilterOptions()
    
    return result
  }, [fetchResumes, fetchStats, fetchFilterOptions])

  // Get available filter options
  const getFilterOptions = useCallback(() => {
    return filterOptions
  }, [filterOptions])

  // Initial load
  useEffect(() => {
    // Only run on client side and only once
    if (typeof window !== 'undefined') {
      fetchResumes()
      fetchStats()
      fetchFilterOptions()
    }
  }, []) // Empty dependency array to run only once

  return {
    resumes,
    stats,
    loading,
    error,
    pagination,
    uploadResume,
    batchUploadResumes,
    getFilterOptions,
    fetchResumes,
    refetch: () => fetchResumes()
  }
} 

// TEST FUNCTION: Check backend connection
export async function testBackendConnection() {
  const url = `${API_URL}/resumes/`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(`Backend connection failed: HTTP ${response.status}`);
      return false;
    }
    const data = await response.json();
    console.log('Backend connection successful. Resume data:', data);
    return true;
  } catch (err) {
    console.error('Backend connection error:', err);
    return false;
  }
} 

// Automatically test backend connection on page load
if (typeof window !== 'undefined') {
  testBackendConnection().then((result) => {
    if (result) {
      console.log('✅ Frontend is connected to the backend API.');
    } else {
      console.error('❌ Frontend could NOT connect to the backend API.');
    }
  });
}