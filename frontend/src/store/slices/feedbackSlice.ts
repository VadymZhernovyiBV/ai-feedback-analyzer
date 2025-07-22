import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { api, retryRequest } from '@/utils/api'
import { API_ENDPOINTS } from '@/utils/constants'
import {
  Feedback,
  FeedbackCreate,
  FeedbackUpdate,
  PaginatedResponse,
  StatsResponse,
} from '@/types/feedback'

interface FeedbackState {
  // Feedback list
  feedbackList: Feedback[]
  totalFeedback: number
  currentPage: number
  pageSize: number
  totalPages: number
  
  // Filters
  filters: {
    sentiment?: string
    category?: string
    search?: string
    tag?: string
  }
  
  // Stats
  stats: StatsResponse | null
  
  // Loading states
  isLoading: boolean
  isAnalyzing: boolean
  isLoadingStats: boolean
  
  // Error states
  error: string | null
  
  // Selected feedback
  selectedFeedback: Feedback | null
}

const initialState: FeedbackState = {
  feedbackList: [],
  totalFeedback: 0,
  currentPage: 1,
  pageSize: 20,
  totalPages: 0,
  filters: {},
  stats: null,
  isLoading: false,
  isAnalyzing: false,
  isLoadingStats: false,
  error: null,
  selectedFeedback: null,
}

// Async thunks
export const analyzeFeedback = createAsyncThunk(
  'feedback/analyze',
  async (data: FeedbackCreate) => {
    const response = await retryRequest(() =>
      api.post<Feedback>(API_ENDPOINTS.ANALYZE_FEEDBACK, data)
    )
    return response.data
  }
)

export const fetchFeedbackList = createAsyncThunk(
  'feedback/fetchList',
  async (params: {
    page?: number
    pageSize?: number
    sentiment?: string
    category?: string
    search?: string
    tag?: string
  }) => {
    const response = await api.get<PaginatedResponse<Feedback>>(
      API_ENDPOINTS.FEEDBACK_LIST,
      { params }
    )
    return response.data
  }
)

export const fetchFeedbackById = createAsyncThunk(
  'feedback/fetchById',
  async (id: number) => {
    const response = await api.get<Feedback>(API_ENDPOINTS.FEEDBACK_DETAIL(id))
    return response.data
  }
)

export const updateFeedbackTags = createAsyncThunk(
  'feedback/updateTags',
  async ({ id, data }: { id: number; data: FeedbackUpdate }) => {
    const response = await api.put<Feedback>(
      API_ENDPOINTS.UPDATE_TAGS(id),
      data
    )
    return response.data
  }
)

export const deleteFeedback = createAsyncThunk(
  'feedback/delete',
  async (id: number) => {
    await api.delete(API_ENDPOINTS.DELETE_FEEDBACK(id))
    return id
  }
)

export const fetchStats = createAsyncThunk(
  'feedback/fetchStats',
  async () => {
    const response = await api.get<StatsResponse>(API_ENDPOINTS.STATS)
    return response.data
  }
)

// Slice
const feedbackSlice = createSlice({
  name: 'feedback',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<typeof initialState.filters>) => {
      state.filters = action.payload
      state.currentPage = 1 // Reset to first page when filters change
    },
    clearFilters: (state) => {
      state.filters = {}
      state.currentPage = 1
    },
    setPage: (state, action: PayloadAction<number>) => {
      state.currentPage = action.payload
    },
    setPageSize: (state, action: PayloadAction<number>) => {
      state.pageSize = action.payload
      state.currentPage = 1 // Reset to first page when page size changes
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // Analyze feedback
    builder
      .addCase(analyzeFeedback.pending, (state) => {
        state.isAnalyzing = true
        state.error = null
      })
      .addCase(analyzeFeedback.fulfilled, (state, action) => {
        state.isAnalyzing = false
        // Add new feedback to the beginning of the list
        state.feedbackList.unshift(action.payload)
        state.totalFeedback += 1
      })
      .addCase(analyzeFeedback.rejected, (state, action) => {
        state.isAnalyzing = false
        state.error = action.error.message || 'Failed to analyze feedback'
      })
    
    // Fetch feedback list
    builder
      .addCase(fetchFeedbackList.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchFeedbackList.fulfilled, (state, action) => {
        state.isLoading = false
        state.feedbackList = action.payload.items
        state.totalFeedback = action.payload.total
        state.currentPage = action.payload.page
        state.pageSize = action.payload.page_size
        state.totalPages = action.payload.pages
      })
      .addCase(fetchFeedbackList.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.error.message || 'Failed to fetch feedback'
      })
    
    // Fetch feedback by ID
    builder
      .addCase(fetchFeedbackById.fulfilled, (state, action) => {
        state.selectedFeedback = action.payload
      })
    
    // Update tags
    builder
      .addCase(updateFeedbackTags.fulfilled, (state, action) => {
        const index = state.feedbackList.findIndex(
          (f) => f.id === action.payload.id
        )
        if (index !== -1) {
          state.feedbackList[index] = action.payload
        }
        if (state.selectedFeedback?.id === action.payload.id) {
          state.selectedFeedback = action.payload
        }
      })
    
    // Delete feedback
    builder
      .addCase(deleteFeedback.fulfilled, (state, action) => {
        state.feedbackList = state.feedbackList.filter(
          (f) => f.id !== action.payload
        )
        state.totalFeedback -= 1
        if (state.selectedFeedback?.id === action.payload) {
          state.selectedFeedback = null
        }
      })
    
    // Fetch stats
    builder
      .addCase(fetchStats.pending, (state) => {
        state.isLoadingStats = true
      })
      .addCase(fetchStats.fulfilled, (state, action) => {
        state.isLoadingStats = false
        state.stats = action.payload
      })
      .addCase(fetchStats.rejected, (state) => {
        state.isLoadingStats = false
      })
  },
})

export const {
  setFilters,
  clearFilters,
  setPage,
  setPageSize,
  clearError,
} = feedbackSlice.actions

export default feedbackSlice.reducer