import { Box, Typography, Paper } from '@mui/material'
import { Feedback as FeedbackIcon } from '@mui/icons-material'

import { Feedback } from '@/types/feedback'
import { FeedbackCard } from './FeedbackCard'
import { LoadingSpinner } from '../common/LoadingSpinner'

interface FeedbackListProps {
  feedbackList: Feedback[]
  isLoading: boolean
}

export function FeedbackList({ feedbackList, isLoading }: FeedbackListProps) {
  if (isLoading) {
    return <LoadingSpinner message="Loading feedback..." />
  }

  if (feedbackList.length === 0) {
    return (
      <Paper
        elevation={1}
        sx={{
          p: 4,
          textAlign: 'center',
          color: 'text.secondary',
        }}
      >
        <FeedbackIcon sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
        <Typography variant="h6" gutterBottom>
          No feedback found
        </Typography>
        <Typography variant="body2">
          Try adjusting your filters or submit some feedback to get started.
        </Typography>
      </Paper>
    )
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {feedbackList.map((feedback) => (
        <FeedbackCard key={feedback.id} feedback={feedback} />
      ))}
    </Box>
  )
}