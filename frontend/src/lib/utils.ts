import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value: number, decimals = 2): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function formatCurrency(value: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(value);
}

export function formatCarbonFootprint(value: number): string {
  if (value < 1) {
    return `${formatNumber(value * 1000, 0)}g CO₂e`;
  } else if (value < 1000) {
    return `${formatNumber(value, 1)}kg CO₂e`;
  } else {
    return `${formatNumber(value / 1000, 1)}t CO₂e`;
  }
}

export function getCarbonIntensityLevel(value: number): 'low' | 'medium' | 'high' {
  // These thresholds can be adjusted based on domain knowledge
  if (value < 5) return 'low';
  if (value < 20) return 'medium';
  return 'high';
}

export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function truncate(text: string, length: number): string {
  if (text.length <= length) return text;
  return text.slice(0, length) + '...';
}

export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}