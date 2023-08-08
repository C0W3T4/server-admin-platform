import { Box } from '@mui/material'
import { Outlet } from 'react-router-dom'

const Users = () => {
  return (
    <Box>
      <Outlet />
    </Box>
  )
}

export default Users
