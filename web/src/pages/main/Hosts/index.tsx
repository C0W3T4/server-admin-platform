import { Box } from '@mui/material'
import { Outlet } from 'react-router-dom'

const Hosts = () => {
  return (
    <Box>
      <Outlet />
    </Box>
  )
}

export default Hosts
