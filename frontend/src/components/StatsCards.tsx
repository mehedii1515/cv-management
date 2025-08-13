'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Users, FileText, Clock, AlertTriangle } from 'lucide-react'
import { ResumeStats } from '@/types/resume'

interface StatsCardsProps {
  stats: ResumeStats | null
}

export function StatsCards({ stats }: StatsCardsProps) {
  if (!stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader className="pb-2">
              <div className="h-4 bg-muted rounded w-1/2"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-muted rounded w-3/4"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  const cards = [
    {
      title: 'Total Resumes',
      value: stats.total_resumes,
      icon: Users,
      description: 'Total uploaded resumes',
      color: 'text-blue-600'
    },
    {
      title: 'Processed',
      value: stats.processed_resumes,
      icon: FileText,
      description: 'Successfully parsed',
      color: 'text-green-600'
    },
    {
      title: 'Pending',
      value: stats.pending_resumes,
      icon: Clock,
      description: 'Awaiting processing',
      color: 'text-yellow-600'
    },
    {
      title: 'Failed',
      value: stats.failed_resumes,
      icon: AlertTriangle,
      description: 'Processing failed',
      color: 'text-red-600'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Main Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-6">
        {cards.map((card, index) => (
          <Card key={index} className={index < 4 ? "xl:col-span-1" : "xl:col-span-2"}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {card.title}
              </CardTitle>
              <card.icon className={`h-4 w-4 ${card.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{card.value}</div>
              <p className="text-xs text-muted-foreground">
                {card.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Additional Stats Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* Top Expertise Areas */}
        <Card>
          <CardHeader>
            <CardTitle>Top Expertise Areas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {stats.top_expertise_areas.slice(0, 5).map(([area, count], index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm truncate">{area}</span>
                  <span className="text-sm font-medium">{count}</span>
                </div>
              ))}
              {stats.top_expertise_areas.length === 0 && (
                <p className="text-sm text-muted-foreground">
                  No data available yet
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Top Locations */}
        <Card>
          <CardHeader>
            <CardTitle>Top Locations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {stats.top_locations.slice(0, 5).map(([location, count], index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm truncate">{location}</span>
                  <span className="text-sm font-medium">{count}</span>
                </div>
              ))}
              {stats.top_locations.length === 0 && (
                <p className="text-sm text-muted-foreground">
                  No data available yet
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-sm">
                <span className="text-muted-foreground">Processing Rate:</span>
                <span className="ml-2 font-medium">
                  {stats.total_resumes > 0 
                    ? Math.round((stats.processed_resumes / stats.total_resumes) * 100)
                    : 0}%
                </span>
              </div>
              <div className="text-sm">
                <span className="text-muted-foreground">Success Rate:</span>
                <span className="ml-2 font-medium">
                  {stats.total_resumes > 0 
                    ? Math.round(((stats.total_resumes - stats.failed_resumes) / stats.total_resumes) * 100)
                    : 0}%
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 