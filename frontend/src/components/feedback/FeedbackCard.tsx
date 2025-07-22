import { useState } from 'react'
import { useDispatch } from 'react-redux'
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Tooltip,
} from '@mui/material'
import {
  MoreVert as MoreIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  AccessTime as TimeIcon,
  Speed as SpeedIcon,
  SmartToy as AIIcon,
} from '@mui/icons-material'

import { AppDispatch } from '@/store'
import { updateFeedbackTags, deleteFeedback } from '@/store/slices/feedbackSlice'
import { Feedback } from '@/types/feedback'
import { SENTIMENT_COLORS, SENTIMENT_ICONS } from '@/utils/constants'

interface FeedbackCardProps {
  feedback: Feedback
}

export function FeedbackCard({ feedback }: FeedbackCardProps) {
  const dispatch = useDispatch<AppDispatch>()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [editTagsOpen, setEditTagsOpen] = useState(false)
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false)
  const [tagInput, setTagInput] = useState(feedback.tags.join(', '))

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleEditTags = () => {
    handleMenuClose()
    setEditTagsOpen(true)
  }

  const handleDeleteClick = () => {
    handleMenuClose()
    setDeleteConfirmOpen(true)
  }

  const handleSaveTags = async () => {
    const tags = tagInput
      .split(',')
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0)
      .slice(0, 10) // Limit to 10 tags

    await dispatch(
      updateFeedbackTags({
        id: feedback.id,
        data: { tags },
      })
    )
    setEditTagsOpen(false)
  }

  const handleDelete = async () => {
    await dispatch(deleteFeedback(feedback.id))
    setDeleteConfirmOpen(false)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  }

  return (
    <>
      <Card elevation={2}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip
                label={feedback.sentiment}
                size="small"
                icon={
                  <Typography component="span" sx={{ fontSize: '1rem' }}>
                    {SENTIMENT_ICONS[feedback.sentiment]}
                  </Typography>
                }
                sx={{
                  backgroundColor: SENTIMENT_COLORS[feedback.sentiment],
                  color: 'white',
                  fontWeight: 'bold',
                }}
              />
              <Chip
                label={feedback.category}
                size="small"
                variant="outlined"
                color="primary"
              />
            </Box>
            <IconButton size="small" onClick={handleMenuOpen}>
              <MoreIcon />
            </IconButton>
          </Box>

          <Typography variant="body1" paragraph>
            {feedback.text}
          </Typography>

          {feedback.tags.length > 0 && (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
              {feedback.tags.map((tag) => (
                <Chip key={tag} label={tag} size="small" variant="outlined" />
              ))}
            </Box>
          )}

          <Box
            sx={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: 2,
              mt: 2,
              color: 'text.secondary',
              fontSize: '0.875rem',
            }}
          >
            <Tooltip title="Created at">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <TimeIcon fontSize="small" />
                {formatDate(feedback.created_at)}
              </Box>
            </Tooltip>
            <Tooltip title="Analysis duration">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <SpeedIcon fontSize="small" />
                {feedback.analysis_duration_ms}ms
              </Box>
            </Tooltip>
            <Tooltip title="AI model used">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <AIIcon fontSize="small" />
                {feedback.model_used}
              </Box>
            </Tooltip>
          </Box>

          <Box
            sx={{
              display: 'flex',
              gap: 2,
              mt: 1,
              fontSize: '0.75rem',
              color: 'text.secondary',
            }}
          >
            <Typography variant="caption">
              Sentiment confidence: {(feedback.sentiment_confidence * 100).toFixed(0)}%
            </Typography>
            <Typography variant="caption">
              Category confidence: {(feedback.category_confidence * 100).toFixed(0)}%
            </Typography>
          </Box>
        </CardContent>
      </Card>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleEditTags}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Edit Tags
        </MenuItem>
        <MenuItem onClick={handleDeleteClick} sx={{ color: 'error.main' }}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>

      {/* Edit Tags Dialog */}
      <Dialog open={editTagsOpen} onClose={() => setEditTagsOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Tags</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Tags (comma-separated)"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            helperText="Enter tags separated by commas. Maximum 10 tags."
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditTagsOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveTags} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Delete Feedback</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this feedback? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Cancel</Button>
          <Button onClick={handleDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  )
}