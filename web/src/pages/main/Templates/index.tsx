import { Box } from '@mui/material'
import { Outlet } from 'react-router-dom'

const Templates = () => {
  return (
    <Box>
      <Outlet />
    </Box>
  )
}

export default Templates
