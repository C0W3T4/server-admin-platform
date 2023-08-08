import { Box } from '@mui/material'
import { Outlet } from 'react-router-dom'

const Inventories = () => {
  return (
    <Box>
      <Outlet />
    </Box>
  )
}

export default Inventories
