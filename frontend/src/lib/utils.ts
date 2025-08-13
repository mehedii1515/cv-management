import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function normalizeUrl(url: string): string | null {
  if (!url || typeof url !== 'string') return null

  // Remove any whitespace
  url = url.trim()

  // If URL doesn't start with http:// or https://, add https://
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url
  }

  try {
    // Validate URL
    new URL(url)
    return url
  } catch {
    return null
  }
}