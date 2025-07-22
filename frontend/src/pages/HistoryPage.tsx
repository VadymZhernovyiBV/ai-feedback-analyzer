import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  Box,
  Paper,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Pagination,
  Grid,
  Chip,
  IconButton,
  Collapse,
} from '@mui/material'
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Clear as ClearIcon,
} from '@mui/icons-material'

import { AppDispatch, RootState } from '@/store'
import {
  fetchFeedbackList,
  setFilters,
  clearFilters,
  setPage,
  setPageSize,
} from '@/store/slices/feedbackSlice'
import { FeedbackList } from '@/components/feedback/FeedbackList'
import { PAGE_SIZE_OPTIONS } from '@/utils/constants'

export function HistoryPage() {
  const dispatch = useDispatch<AppDispatch>()
  const {
    feedbackList,
    isLoading,
    currentPage,
    pageSize,
    totalPages,
    totalFeedback,
    filters,
  } = useSelector((state: RootState) => state.feedback)

  const [showFilters, setShowFilters] = useState(true)
  const [searchText, setSearchText] = useState(filters.search || '')
  const [selectedSentiment, setSelectedSentiment] = useState(filters.sentiment || '')
  const [selectedCategory, setSelectedCategory] = useState(filters.category || '')
  const [selectedTag, setSelectedTag] = useState(filters.tag || '')

  useEffect(() => {
    // Fetch feedback list with current filters
    dispatch(
      fetchFeedbackList({
        page: currentPage,
        pageSize,
        ...filters,
      })
    )
  }, [dispatch, currentPage, pageSize, filters])

  const handleSearch = () => {
    dispatch(
      setFilters({
        ...filters,
        search: searchText,
      })
    )
  }

  const handleFilterChange = () => {
    dispatch(
      setFilters({
        search: searchText,
        sentiment: selectedSentiment,
        category: selectedCategory,
        tag: selectedTag,
      })
    )
  }

  const handleClearFilters = () => {
    setSearchText('')
    setSelectedSentiment('')
    setSelectedCategory('')
    setSelectedTag('')
    dispatch(clearFilters())
  }

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    dispatch(setPage(value))
  }

  const handlePageSizeChange = (event: SelectChangeEvent<number>) => {
    dispatch(setPageSize(Number(event.target.value)))
  }

  const activeFilterCount = Object.values(filters).filter(Boolean).length

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Feedback History
      </Typography>

      {/* Filters */}
      <Paper elevation={2} sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: showFilters ? 2 : 0 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="h6">Filters</Typography>
            {activeFilterCount > 0 && (
              <Chip
                label={`${activeFilterCount} active`}
                size="small"
                color="primary"
              />
            )}
          </Box>
          <IconButton onClick={() => setShowFilters(!showFilters)}>
            <FilterIcon />
          </IconButton>
        </Box>

        <Collapse in={showFilters}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Search feedback"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={handleSearch}>
                      <SearchIcon />
                    </IconButton>
                  ),
                }}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth>
                <InputLabel>Sentiment</InputLabel>
                <Select
                  value={selectedSentiment}
                  label="Sentiment"
                  onChange={(e) => setSelectedSentiment(e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="positive">Positive</MenuItem>
                  <MenuItem value="neutral">Neutral</MenuItem>
                  <MenuItem value="negative">Negative</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6} md={2}>
              <TextField
                fullWidth
                label="Category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={2}>
              <TextField
                fullWidth
                label="Tag"
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="contained"
                  onClick={handleFilterChange}
                  startIcon={<FilterIcon />}
                >
                  Apply Filters
                </Button>
                <Button
                  variant="outlined"
                  onClick={handleClearFilters}
                  startIcon={<ClearIcon />}
                  disabled={activeFilterCount === 0}
                >
                  Clear Filters
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Collapse>
      </Paper>

      {/* Results Summary */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="body1" color="text.secondary">
          Showing {feedbackList.length} of {totalFeedback} feedback entries
        </Typography>
        <FormControl size="small">
          <Select
            value={pageSize}
            onChange={handlePageSizeChange}
            displayEmpty
          >
            {PAGE_SIZE_OPTIONS.map((size) => (
              <MenuItem key={size} value={size}>
                {size} per page
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* Feedback List */}
      <FeedbackList feedbackList={feedbackList} isLoading={isLoading} />

      {/* Pagination */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={totalPages}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
            size="large"
            showFirstButton
            showLastButton
          />
        </Box>
      )}
    </Box>
  )
}