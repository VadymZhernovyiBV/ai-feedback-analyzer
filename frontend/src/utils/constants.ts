export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export const API_ENDPOINTS = {
  ANALYZE_FEEDBACK: '/api/feedback/analyze',
  FEEDBACK_LIST: '/api/feedback',
  FEEDBACK_DETAIL: (id: number) => `/api/feedback/${id}`,
  UPDATE_TAGS: (id: number) => `/api/feedback/${id}/tags`,
  DELETE_FEEDBACK: (id: number) => `/api/feedback/${id}`,
  STATS: '/api/stats',
  HEALTH: '/api/health',
} as const

export const SENTIMENT_COLORS = {
  positive: '#4caf50',
  neutral: '#ff9800',
  negative: '#f44336',
} as const

export const SENTIMENT_ICONS = {
  positive: '😊',
  neutral: '😐',
  negative: '😞',
} as const

export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]

export const MAX_FEEDBACK_LENGTH = 5000
export const MAX_TAGS = 10
export const MAX_TAG_LENGTH = 50