'use client'

import React, { useState, useMemo } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { 
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Search, X, Filter, ChevronDown, MapPin, Briefcase, GraduationCap, Users, Code } from 'lucide-react'

interface SearchFiltersProps {
  searchTerm: string
  onSearchChange: (term: string) => void
  selectedFilters: {
    expertise: string[]
    location: string[]
    sectors: string[]
    skills: string[]
    experience_level: string[]
    availability: string[]
  }
  onFilterChange: (filterType: string, value: string) => void
  onClearFilters: () => void
  availableFilters: {
    expertise: string[]
    locations: string[]
    sectors: string[]
    skills: string[]
    experienceLevels: string[]
    availabilities?: string[]
  }
}

interface FilterCategoryProps {
  title: string
  icon: React.ComponentType<{ className?: string }>
  items: string[]
  selectedItems: string[]
  onItemToggle: (item: string) => void
  showSearch?: boolean
  placeholder?: string
  showYearRanges?: boolean
}

function FilterCategory({ 
  title, 
  icon: Icon, 
  items, 
  selectedItems, 
  onItemToggle, 
  showSearch = true,
  placeholder = "Search...",
  showYearRanges = false
}: FilterCategoryProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [isOpen, setIsOpen] = useState(false)

  // Experience level year ranges mapping
  const experienceYearRanges: { [key: string]: string } = {
    'Not specified': 'No experience data',
    'Junior': '0-2 years',
    'Mid-level': '2-5 years', 
    'Senior': '5-10 years',
    'Expert': '10+ years'
  }

  const filteredItems = useMemo(() => {
    let result = items
    
    // Filter by search term if search is enabled and has value
    if (showSearch && searchTerm.trim()) {
      result = result.filter(item => 
      item.toLowerCase().includes(searchTerm.toLowerCase())
    )
    }
    
    // Sort to show selected items first, then unselected items
    return result.sort((a, b) => {
      const aSelected = selectedItems.includes(a)
      const bSelected = selectedItems.includes(b)
      
      // Selected items come first
      if (aSelected && !bSelected) return -1
      if (!aSelected && bSelected) return 1
      
      // Within each group (selected/unselected), sort alphabetically
      return a.localeCompare(b)
    })
  }, [items, searchTerm, showSearch, selectedItems])

  const selectedCount = selectedItems.length
  const hasSelected = selectedCount > 0

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button 
          variant={hasSelected ? "default" : "outline"} 
          className="h-10 px-4 justify-between min-w-[140px]"
        >
          <div className="flex items-center gap-2">
            <Icon className="h-4 w-4" />
            <span className="truncate">{title}</span>
            {hasSelected && (
              <Badge variant="secondary" className="ml-1 h-5 w-5 rounded-full p-0 text-xs">
                {selectedCount}
              </Badge>
            )}
          </div>
          <ChevronDown className="h-4 w-4 ml-2 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <div className="p-4 border-b">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium">{title}</h4>
            {hasSelected && (
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => {
                  selectedItems.forEach(item => onItemToggle(item))
                }}
                className="h-6 text-xs"
              >
                Clear
              </Button>
            )}
          </div>
          {showSearch && (
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder={placeholder}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 h-9"
              />
            </div>
          )}
        </div>
        <div className="max-h-60 overflow-y-auto">
          {filteredItems.length > 0 ? (
            <div className="p-2">
              {(() => {
                const selectedFilteredItems = filteredItems.filter(item => selectedItems.includes(item))
                const unselectedFilteredItems = filteredItems.filter(item => !selectedItems.includes(item))
                
                return (
                  <>
                    {/* Selected Items Section */}
                    {selectedFilteredItems.length > 0 && (
                      <div className="mb-3">
                        <div className="px-3 py-1 mb-1 text-xs font-medium text-muted-foreground bg-muted/50 rounded">
                          Selected ({selectedFilteredItems.length})
                        </div>
                        <div className="space-y-1">
                          {selectedFilteredItems.map((item, index) => (
                  <div
                              key={`selected-${index}`}
                              className="flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer hover:bg-accent bg-primary/10 border border-primary/20"
                              onClick={() => onItemToggle(item)}
                            >
                              <div className="w-4 h-4 rounded border-2 flex items-center justify-center bg-primary border-primary">
                                <div className="w-2 h-2 bg-primary-foreground rounded" />
                              </div>
                              <span className="text-sm flex-1 truncate font-medium">
                                {item}
                                {showYearRanges && experienceYearRanges[item] && (
                                  <span className="block text-xs text-muted-foreground font-normal">
                                    {experienceYearRanges[item]}
                                  </span>
                                )}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Unselected Items Section */}
                    {unselectedFilteredItems.length > 0 && (
                      <div>
                        {selectedFilteredItems.length > 0 && (
                          <div className="px-3 py-1 mb-1 text-xs font-medium text-muted-foreground bg-muted/50 rounded">
                            Available ({unselectedFilteredItems.length})
                          </div>
                        )}
                        <div className="space-y-1">
                          {unselectedFilteredItems.map((item, index) => (
                            <div
                              key={`unselected-${index}`}
                              className="flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer hover:bg-accent"
                    onClick={() => onItemToggle(item)}
                  >
                              <div className="w-4 h-4 rounded border-2 flex items-center justify-center border-muted-foreground">
                              </div>
                              <span className="text-sm flex-1 truncate">
                                {item}
                                {showYearRanges && experienceYearRanges[item] && (
                                  <span className="block text-xs text-muted-foreground font-normal">
                                    {experienceYearRanges[item]}
                                  </span>
                                )}
                              </span>
                            </div>
                          ))}
                    </div>
                  </div>
                    )}
                  </>
                )
              })()}
            </div>
          ) : (
            <div className="p-4 text-center text-sm text-muted-foreground">
              No {title.toLowerCase()} found
            </div>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}

export function SearchFilters({
  searchTerm,
  onSearchChange,
  selectedFilters,
  onFilterChange,
  onClearFilters,
  availableFilters
}: SearchFiltersProps) {
  // Safely calculate total filters with null checks
  const totalFilters = selectedFilters ? 
    Object.values(selectedFilters).reduce((acc, arr) => acc + (arr?.length || 0), 0) : 0

  const handleFilterToggle = (filterType: string) => (value: string) => {
    onFilterChange(filterType, value)
  }

  return (
    <div className="space-y-4">
      {/* Search Bar and Filters Row */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1 min-w-0">
          <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
                  placeholder="Search across all resume data: names, skills, companies, locations, certifications, publications..."
              value={searchTerm}
              onChange={(e) => onSearchChange(e.target.value)}
                  className="pl-10 h-12 text-base"
            />
              </div>
            </div>
            
            {/* Filter Buttons */}
            <div className="flex flex-wrap gap-2 lg:gap-3">
              <FilterCategory
                title="Sectors"
                icon={Briefcase}
                items={availableFilters?.sectors || []}
                selectedItems={selectedFilters?.sectors || []}
                onItemToggle={handleFilterToggle('sectors')}
                placeholder="Search sectors..."
              />
              
              <FilterCategory
                title="Expertise"
                icon={GraduationCap}
                items={availableFilters?.expertise || []}
                selectedItems={selectedFilters?.expertise || []}
                onItemToggle={handleFilterToggle('expertise')}
                placeholder="Search expertise areas..."
              />
              
              <FilterCategory
                title="Skills"
                icon={Code}
                items={availableFilters?.skills || []}
                selectedItems={selectedFilters?.skills || []}
                onItemToggle={handleFilterToggle('skills')}
                placeholder="Search skills..."
              />
              
              <FilterCategory
                title="Location"
                icon={MapPin}
                items={availableFilters?.locations || []}
                selectedItems={selectedFilters?.location || []}
                onItemToggle={handleFilterToggle('location')}
                placeholder="Search locations..."
              />
              
              <FilterCategory
                title="Experience"
                icon={Users}
                items={availableFilters?.experienceLevels || []}
                selectedItems={selectedFilters?.experience_level || []}
                onItemToggle={handleFilterToggle('experience_level')}
                showSearch={false}
                showYearRanges={true}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Active Filters */}
      {totalFilters > 0 && selectedFilters && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium flex items-center gap-2">
                <Filter className="h-4 w-4" />
                Active Filters ({totalFilters})
              </h3>
              <Button
                variant="outline"
                size="sm"
                onClick={onClearFilters}
                className="h-8 text-xs"
              >
                Clear All
              </Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {Object.entries(selectedFilters || {}).map(([filterType, values]) =>
                (values || []).map((value, index) => (
                  <Badge
                    key={`${filterType}-${index}`}
                    variant="secondary"
                    className="cursor-pointer flex items-center gap-1"
                    onClick={() => onFilterChange(filterType, value)}
                  >
                    {value}
                    <X className="h-3 w-3" />
                  </Badge>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
} 