import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  LinearProgress,
} from '@mui/material'
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts'

import { AppDispatch, RootState } from '@/store'
import { fetchStats } from '@/store/slices/feedbackSlice'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { SENTIMENT_COLORS } from '@/utils/constants'

export function AnalyticsPage() {
  const dispatch = useDispatch<AppDispatch>()
  const { stats, isLoadingStats } = useSelector((state: RootState) => state.feedback)

  useEffect(() => {
    dispatch(fetchStats())
  }, [dispatch])

  if (isLoadingStats || !stats) {
    return <LoadingSpinner message="Loading analytics..." />
  }

  // Prepare data for charts
  const sentimentData = Object.entries(stats.sentiment_distribution).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
    color: SENTIMENT_COLORS[name as keyof typeof SENTIMENT_COLORS],
  }))

  const categoryData = stats.top_categories.slice(0, 10)

  const activityData = Object.entries(stats.recent_activity)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([date, count]) => ({
      date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      count,
    }))

  const confidenceData = [
    {
      name: 'Positive',
      value: stats.average_confidence.sentiment_positive * 100,
      color: SENTIMENT_COLORS.positive,
    },
    {
      name: 'Neutral',
      value: stats.average_confidence.sentiment_neutral * 100,
      color: SENTIMENT_COLORS.neutral,
    },
    {
      name: 'Negative',
      value: stats.average_confidence.sentiment_negative * 100,
      color: SENTIMENT_COLORS.negative,
    },
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Feedback
              </Typography>
              <Typography variant="h3" color="primary">
                {stats.total_feedback}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Positive Rate
              </Typography>
              <Typography variant="h3" color={SENTIMENT_COLORS.positive}>
                {stats.total_feedback > 0
                  ? Math.round((stats.sentiment_distribution.positive / stats.total_feedback) * 100)
                  : 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Top Category
              </Typography>
              <Typography variant="h6" noWrap>
                {stats.top_categories[0]?.category || 'N/A'}
              </Typography>
              <Chip
                label={`${stats.top_categories[0]?.count || 0} entries`}
                size="small"
                color="primary"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Avg. Category Confidence
              </Typography>
              <Typography variant="h3">
                {Math.round(stats.average_confidence.category * 100)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Sentiment Distribution */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Sentiment Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Sentiment Confidence */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Average Sentiment Confidence
            </Typography>
            <Box sx={{ mt: 3 }}>
              {confidenceData.map((item) => (
                <Box key={item.name} sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">{item.name}</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {item.value.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={item.value}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: item.color,
                      },
                    }}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Top Categories */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top Categories
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="category"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#1976d2" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity (7 days)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#1976d2"
                  strokeWidth={2}
                  dot={{ fill: '#1976d2' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}