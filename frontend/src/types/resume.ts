export interface Resume {
  id: string
  timestamp: string
  cv_hash: string
  
  // Personal Information
  first_name: string
  last_name: string
  full_name: string
  email: string
  phone_number: string
  location: string
  date_of_birth?: string
  age?: number
  
  // Professional Information
  current_employer: string
  years_of_experience: number
  total_experience_months: number
  total_experience_years: number
  experience_level: string
  experience_display: string
  availability: string
  preferred_contract_type: string
  preferred_work_arrangement: string
  
  // Skills and Expertise
  expertise_areas: string[]
  expertise_details: Record<string, {
    work_experience?: string
    projects?: string
    other_related_info?: string
  }>
  sectors: string[]
  skill_keywords: string[]
  
  // Contact Information
  linkedin_profile: string
  website_portfolio: string
  
  // Additional Information
  languages_spoken: Array<{
    language: string
    proficiency: string
    mother_tongue: boolean
  }>
  references: string
  notes: string
  
  // Education and Certifications
  professional_certifications: string[]
  professional_associations: string[]
  publications: string[]
  
  // File Information
  original_filename: string
  file_path: string
  file_type: string
  
  // Processing Status
  is_processed: boolean
  processing_status: string
  error_message: string
}

export interface Language {
  language: string
  proficiency: string
  mother_tongue: boolean
}

export interface ResumeStats {
  total_resumes: number
  processed_resumes: number
  pending_resumes: number
  failed_resumes: number
  processing_rate: number
  top_expertise_areas: [string, number][]
  top_locations: [string, number][]
}

export interface UploadResponse {
  id: string
  status: string
  message: string
} 