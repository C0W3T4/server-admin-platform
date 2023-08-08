import { Box, FormControl, Grid, Typography } from '@mui/material'
import { StringColorProps } from '../../types'

interface PasswordIndicatorProps {
  level?: StringColorProps
  strength?: number
}

export const PasswordIndicator = ({ level }: PasswordIndicatorProps) => {
  return (
    <FormControl fullWidth>
      <Box sx={{ mb: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Box
              style={{ backgroundColor: level?.color }}
              sx={{ width: 85, height: 8, borderRadius: '7px' }}
            />
          </Grid>
          <Grid item>
            <Typography variant="subtitle1" fontSize="0.75rem">
              {level?.label}
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </FormControl>
  )
}
