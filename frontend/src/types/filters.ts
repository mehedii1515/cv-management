export interface SelectedFilters {
  expertise: string[]
  location: string[]
  sectors: string[]
  skills: string[]
  experience_level: string[]
  availability: string[]
}

export type FilterCategory = 'expertise' | 'location' | 'sectors' | 'skills' | 'experience_level' | 'availability' 