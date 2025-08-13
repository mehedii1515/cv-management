import React from 'react'
import { Badge } from '@/components/ui/badge'
import { LucideIcon } from 'lucide-react'

interface PageHeaderProps {
  title: string
  description?: string
  badge?: {
    text: string
    icon?: LucideIcon
    variant?: 'default' | 'secondary' | 'destructive' | 'outline'
  }
  children?: React.ReactNode
}

export function PageHeader({ title, description, badge, children }: PageHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-8">
      <div>
        <div className="flex items-center space-x-4">
          <h1 className="text-3xl font-bold">{title}</h1>
          {badge && (
            <Badge variant={badge.variant || 'secondary'}>
              {badge.icon && <badge.icon className="mr-1 h-3 w-3" />}
              {badge.text}
            </Badge>
          )}
        </div>
        {description && (
          <p className="text-muted-foreground mt-2">
            {description}
          </p>
        )}
      </div>
      {children && (
        <div className="flex items-center space-x-4">
          {children}
        </div>
      )}
    </div>
  )
} 