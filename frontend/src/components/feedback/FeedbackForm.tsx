import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useForm, Controller } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Chip,
  IconButton,
  Alert,
  LinearProgress,
} from '@mui/material'
import { Add as AddIcon } from '@mui/icons-material'

import { AppDispatch, RootState } from '@/store'
import { analyzeFeedback, clearError } from '@/store/slices/feedbackSlice'
import { MAX_FEEDBACK_LENGTH, MAX_TAGS, MAX_TAG_LENGTH } from '@/utils/constants'

const schema = yup.object({
  text: yup
    .string()
    .required('Feedback text is required')
    .min(1, 'Feedback cannot be empty')
    .max(MAX_FEEDBACK_LENGTH, `Feedback cannot exceed ${MAX_FEEDBACK_LENGTH} characters`),
  tags: yup
    .array()
    .of(yup.string().max(MAX_TAG_LENGTH))
    .max(MAX_TAGS, `Cannot have more than ${MAX_TAGS} tags`)
    .default([]),
}).required()

type FeedbackFormData = yup.InferType<typeof schema>

export function FeedbackForm() {
  const dispatch = useDispatch<AppDispatch>()
  const { isAnalyzing, error } = useSelector((state: RootState) => state.feedback)
  const [tagInput, setTagInput] = useState('')

  const {
    control,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors },
  } = useForm<FeedbackFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      text: '',
      tags: [],
    },
  })

  const watchedText = watch('text')
  const watchedTags = watch('tags')

  const onSubmit = async (data: FeedbackFormData) => {
    try {
      await dispatch(analyzeFeedback({
        text: data.text,
        tags: data.tags || []
      })).unwrap()
      reset()
      setTagInput('')
    } catch {
      // Error is handled by the slice
    }
  }

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim()
    if (trimmedTag && !watchedTags.includes(trimmedTag)) {
      setValue('tags', [...watchedTags, trimmedTag])
      setTagInput('')
    }
  }

  const handleRemoveTag = (tagToRemove: string) => {
    setValue('tags', watchedTags.filter(tag => tag !== tagToRemove))
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleAddTag()
    }
  }

  const handleClearError = () => {
    dispatch(clearError())
  }

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Analyze Feedback
      </Typography>

      {error && (
        <Alert severity="error" onClose={handleClearError} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
        <Controller
          name="text"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              multiline
              rows={4}
              fullWidth
              label="Feedback Text"
              error={!!errors.text}
              helperText={
                errors.text?.message ||
                `${watchedText.length}/${MAX_FEEDBACK_LENGTH} characters`
              }
              disabled={isAnalyzing}
              sx={{ mb: 2 }}
            />
          )}
        />

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Tags (optional)
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 1 }}>
            {watchedTags.map((tag) => (
              <Chip
                key={tag}
                label={tag}
                onDelete={() => handleRemoveTag(tag)}
                disabled={isAnalyzing}
              />
            ))}
          </Box>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              size="small"
              placeholder="Add a tag"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={isAnalyzing || watchedTags.length >= MAX_TAGS}
              sx={{ flexGrow: 1 }}
            />
            <IconButton
              onClick={handleAddTag}
              disabled={isAnalyzing || !tagInput.trim() || watchedTags.length >= MAX_TAGS}
            >
              <AddIcon />
            </IconButton>
          </Box>
          
          {watchedTags.length >= MAX_TAGS && (
            <Typography variant="caption" color="text.secondary">
              Maximum {MAX_TAGS} tags allowed
            </Typography>
          )}
        </Box>

        {isAnalyzing && <LinearProgress sx={{ mb: 2 }} />}

        <Button
          type="submit"
          variant="contained"
          fullWidth
          disabled={isAnalyzing || !watchedText.trim()}
          sx={{ mt: 2 }}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Feedback'}
        </Button>
      </Box>
    </Paper>
  )
}