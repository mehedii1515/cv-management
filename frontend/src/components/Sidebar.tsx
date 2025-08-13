'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import {
  Building2,
  Users,
  Upload,
  BarChart3,
  Search,
  Zap,
  File,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Activity,
  Database,
  FileText,
  Brain,
  Filter,
  Download,
  History,
  Shield,
  Monitor
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface SidebarProps {
  isCollapsed: boolean
  onToggle: () => void
}

interface NavItem {
  title: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  description?: string
  badge?: string
  isActive?: boolean
}

interface NavSection {
  title: string
  items: NavItem[]
}

export function Sidebar({ isCollapsed, onToggle }: SidebarProps) {
  const pathname = usePathname()
  
  const navigationSections: NavSection[] = [
    {
      title: "Dashboard",
      items: [
        {
          title: "Overview",
          href: "/#resumes",
          icon: BarChart3,
          description: "Analytics and insights",
          isActive: pathname === '/' || pathname.includes('#resumes')
        }
      ]
    },
    {
      title: "Resume Management",
      items: [
        {
          title: "Regular Search",
          href: "/#resumes",
          icon: Search,
          description: "Search CVs with filters and pagination",
          isActive: pathname.includes('#resumes')
        },
        {
          title: "Upload CV",
          href: "/#upload",
          icon: Upload,
          description: "Upload new CVs",
          isActive: pathname.includes('#upload')
        }
      ]
    },
    {
      title: "Search & Discovery",
      items: [
        {
          title: "Regular Search",
          href: "/#resumes",
          icon: Search,
          description: "Standard resume search with filters",
          isActive: pathname.includes('#resumes')
        },
        {
          title: "Database Index Search",
          href: "/#dtsearch",
          icon: Database,
          description: "Advanced database indexing search",
          isActive: pathname.includes('#dtsearch')
        },
        {
          title: "File Index Search",
          href: "/#filesearch",
          icon: File,
          description: "Search through file index",
          isActive: pathname.includes('#filesearch')
        }
      ]
    }
  ]

  const handleNavClick = (href: string) => {
    if (typeof window !== 'undefined') {
      // Extract hash from href
      const hash = href.split('#')[1]
      if (hash) {
        window.location.hash = hash
        // Trigger hashchange event manually for immediate response
        window.dispatchEvent(new HashChangeEvent('hashchange'))
      }
    }
  }

  return (
    <div className={cn(
      "relative flex flex-col bg-background border-r transition-all duration-300 ease-in-out",
      isCollapsed ? "w-16" : "w-64"
    )}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        {!isCollapsed && (
          <div className="flex items-center space-x-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Building2 className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-bold">Maxwell Stamp</div>
              <div className="text-xs text-muted-foreground">Talent Intelligence</div>
            </div>
          </div>
        )}
        
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggle}
          className={cn(
            "h-8 w-8 p-0",
            isCollapsed && "mx-auto"
          )}
        >
          {isCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-4">
          {navigationSections.map((section, sectionIndex) => (
            <div key={section.title}>
              {!isCollapsed && (
                <div className="px-3 py-2">
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    {section.title}
                  </h3>
                </div>
              )}
              
              <div className="space-y-1">
                {section.items.map((item) => {
                  const isActive = item.isActive || pathname === item.href
                  
                  return (
                    <Button
                      key={item.title}
                      variant={isActive ? "secondary" : "ghost"}
                      className={cn(
                        "w-full justify-start h-auto p-3",
                        isCollapsed && "px-2",
                        isActive && "bg-accent text-accent-foreground"
                      )}
                      onClick={() => handleNavClick(item.href)}
                      title={isCollapsed ? item.title : undefined}
                    >
                      <item.icon className={cn(
                        "h-4 w-4 flex-shrink-0",
                        !isCollapsed && "mr-3"
                      )} />
                      
                      {!isCollapsed && (
                        <div className="flex-1 text-left">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">{item.title}</span>
                            {item.badge && (
                              <Badge variant="secondary" className="text-xs px-1.5 py-0.5">
                                {item.badge}
                              </Badge>
                            )}
                          </div>
                          {item.description && (
                            <div className="text-xs text-muted-foreground mt-0.5">
                              {item.description}
                            </div>
                          )}
                        </div>
                      )}
                    </Button>
                  )
                })}
              </div>
              
              {sectionIndex < navigationSections.length - 1 && !isCollapsed && (
                <Separator className="my-3" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      {!isCollapsed && (
        <div className="p-4 border-t">
          <div className="text-xs text-muted-foreground text-center">
            <div>Resume Parser v1.0</div>
            <div className="mt-1">AI-Powered Platform</div>
          </div>
        </div>
      )}
    </div>
  )
}