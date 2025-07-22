export type Sentiment = 'positive' | 'neutral' | 'negative'

export interface Feedback {
  id: number
  text: string
  sentiment: Sentiment
  sentiment_confidence: number
  category: string
  category_confidence: number
  tags: string[]
  created_at: string
  analysis_duration_ms: number
  model_used: string
}

export interface FeedbackCreate {
  text: string
  tags: string[]
}

export interface FeedbackUpdate {
  tags: string[]
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface StatsResponse {
  total_feedback: number
  sentiment_distribution: {
    positive: number
    neutral: number
    negative: number
  }
  top_categories: Array<{
    category: string
    count: number
    avg_confidence: number
  }>
  recent_activity: Record<string, number>
  average_confidence: {
    sentiment_positive: number
    sentiment_neutral: number
    sentiment_negative: number
    category: number
  }
}

export interface ErrorResponse {
  error: string
  message: string
  details?: Record<string, unknown>
}