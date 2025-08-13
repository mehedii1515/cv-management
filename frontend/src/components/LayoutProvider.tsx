'use client'

import React, { useState, useEffect } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Navbar } from '@/components/Navbar'
import { Footer } from '@/components/Footer'
import { Button } from '@/components/ui/button'
import { Menu, Building2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface LayoutProviderProps {
  children: React.ReactNode
}

export function LayoutProvider({ children }: LayoutProviderProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // Check if we're on mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
      // Auto-collapse sidebar on mobile
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true)
      }
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Load sidebar state from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined' && !isMobile) {
      const saved = localStorage.getItem('sidebar-collapsed')
      if (saved !== null) {
        setSidebarCollapsed(JSON.parse(saved))
      }
    }
  }, [isMobile])

  // Save sidebar state to localStorage
  const toggleSidebar = () => {
    const newState = !sidebarCollapsed
    setSidebarCollapsed(newState)
    if (typeof window !== 'undefined' && !isMobile) {
      localStorage.setItem('sidebar-collapsed', JSON.stringify(newState))
    }
  }

  return (
    <div className="flex min-h-screen">
      {/* Sidebar - Hidden on mobile, always visible on desktop */}
      <div className={cn(
        "hidden md:flex flex-col fixed left-0 top-0 h-full z-40 transition-all duration-300",
        sidebarCollapsed ? "w-16" : "w-64"
      )}>
        <Sidebar 
          isCollapsed={sidebarCollapsed} 
          onToggle={toggleSidebar}
        />
      </div>

      {/* Main Content Area */}
      <div className={cn(
        "flex flex-col flex-1 transition-all duration-300",
        "md:ml-16", // Always account for collapsed sidebar on desktop
        !sidebarCollapsed && "md:ml-64" // Expand when sidebar is open
      )}>

        
        {/* Desktop Header - Simplified */}
        <div className="hidden md:block">
          <header className="sticky top-0 z-30 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-6">
              <div className="flex h-16 items-center justify-between">
                <div className="flex items-center space-x-4">
                  <h1 className="text-xl font-semibold">Talent Intelligence Platform</h1>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="text-sm text-muted-foreground">
                    Maxwell Stamp Ltd
                  </div>
                </div>
              </div>
            </div>
          </header>
        </div>

        {/* Mobile Header with Menu Button */}
        <div className="md:hidden">
          <header className="sticky top-0 z-30 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-4">
              <div className="flex h-16 items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSidebarCollapsed(false)}
                    className="h-8 w-8 p-0"
                  >
                    <Menu className="h-5 w-5" />
                  </Button>
                  
                  <div className="flex items-center space-x-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                      <Building2 className="h-5 w-5" />
                    </div>
                    <div>
                      <div className="text-sm font-bold">Maxwell Stamp</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </header>
        </div>

        {/* Main Content */}
        <main className="flex-1 overflow-auto pt-16">
          {children}
        </main>

        {/* Footer */}
        <Footer />
      </div>

      {/* Mobile Sidebar Overlay */}
      {isMobile && !sidebarCollapsed && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black/50 z-40 md:hidden" 
            onClick={() => setSidebarCollapsed(true)}
          />
          
          {/* Mobile Sidebar */}
          <div className="fixed left-0 top-0 h-full w-64 z-50 md:hidden">
            <Sidebar 
              isCollapsed={false} 
              onToggle={() => setSidebarCollapsed(true)}
            />
          </div>
        </>
      )}
    </div>
  )
}