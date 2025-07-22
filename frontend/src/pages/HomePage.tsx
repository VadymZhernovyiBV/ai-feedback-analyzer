import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Grid, Typography, Paper, Box, Chip } from '@mui/material'
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material'

import { AppDispatch, RootState } from '@/store'
import { fetchFeedbackList, fetchStats } from '@/store/slices/feedbackSlice'
import { FeedbackForm } from '@/components/feedback/FeedbackForm'
import { FeedbackList } from '@/components/feedback/FeedbackList'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { SENTIMENT_COLORS } from '@/utils/constants'

export function HomePage() {
  const dispatch = useDispatch<AppDispatch>()
  const { feedbackList, isLoading, stats, isLoadingStats } = useSelector(
    (state: RootState) => state.feedback
  )

  useEffect(() => {
    // Fetch recent feedback
    dispatch(fetchFeedbackList({ page: 1, pageSize: 5 }))
    // Fetch stats
    dispatch(fetchStats())
  }, [dispatch])

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <TrendingUp />
      case 'negative':
        return <TrendingDown />
      default:
        return <TrendingFlat />
    }
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Welcome to AI Feedback Analyzer
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Submit your feedback below and get instant AI-powered sentiment analysis and categorization.
        </Typography>
      </Grid>

      {/* Quick Stats */}
      {stats && !isLoadingStats && (
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Stats
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {stats.total_feedback}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Feedback
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={8}>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
                  {Object.entries(stats.sentiment_distribution).map(([sentiment, count]) => (
                    <Box
                      key={sentiment}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                        p: 1,
                        borderRadius: 1,
                        backgroundColor: `${SENTIMENT_COLORS[sentiment as keyof typeof SENTIMENT_COLORS]}20`,
                      }}
                    >
                      {getSentimentIcon(sentiment)}
                      <Box>
                        <Typography variant="h6">{count}</Typography>
                        <Typography variant="caption" sx={{ textTransform: 'capitalize' }}>
                          {sentiment}
                        </Typography>
                      </Box>
                    </Box>
                  ))}
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      )}

      {/* Feedback Form */}
      <Grid item xs={12} md={6}>
        <FeedbackForm />
      </Grid>

      {/* Recent Feedback */}
      <Grid item xs={12} md={6}>
        <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5">
              Recent Feedback
            </Typography>
            <Chip label={`${feedbackList.length} items`} size="small" />
          </Box>
          
          {isLoading ? (
            <LoadingSpinner message="Loading recent feedback..." />
          ) : (
            <FeedbackList feedbackList={feedbackList} isLoading={false} />
          )}
        </Paper>
      </Grid>
    </Grid>
  )
}