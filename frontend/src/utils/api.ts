import axios, { AxiosError } from 'axios'
import { API_BASE_URL } from './constants'
import { ErrorResponse } from '@/types/feedback'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed in future
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError<ErrorResponse>) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error
      const errorData = error.response.data
      
      // Create a more user-friendly error message
      const message = errorData?.message || 'An error occurred'
      
      // Log error details for debugging
      console.error('API Error:', {
        status: error.response.status,
        message,
        details: errorData?.details,
      })
      
      // Throw a new error with the message
      throw new Error(message)
    } else if (error.request) {
      // Request was made but no response
      throw new Error('Network error. Please check your connection.')
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred')
    }
  }
)

// Retry logic for failed requests
const retryRequest = async <T>(
  fn: () => Promise<T>,
  retries = 3,
  delay = 1000
): Promise<T> => {
  try {
    return await fn()
  } catch (error) {
    if (retries === 0) throw error
    
    // Check if it's a rate limit error
    if (error instanceof AxiosError && error.response?.status === 429) {
      // Wait longer for rate limit errors
      await new Promise(resolve => setTimeout(resolve, delay * 2))
    } else {
      await new Promise(resolve => setTimeout(resolve, delay))
    }
    
    return retryRequest(fn, retries - 1, delay * 2)
  }
}

export { api, retryRequest }