import { Avatar, Box } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { TbMenu2 } from 'react-icons/tb'
import { useDispatch, useSelector } from '../../../libs/redux'
import { openDrawer } from '../../../libs/redux/slices/menu'
import LogoSection from '../LogoSection'
import { LanguageSection } from './LanguageSection'
import { MobileSection } from './MobileSection'
import { ProfileSection } from './ProfileSection'

const Header = () => {
  const theme = useTheme()

  const dispatch = useDispatch()
  const { drawerOpen } = useSelector((state) => state.menu)

  return (
    <>
      <Box
        sx={{
          width: 228,
          display: 'flex',
          [theme.breakpoints.down('md')]: {
            width: 'auto',
          },
        }}
      >
        <Box
          component="span"
          sx={{ display: { xs: 'none', md: 'block' }, flexGrow: 1 }}
        >
          <LogoSection />
        </Box>
        <Avatar
          variant="rounded"
          sx={{
            ...theme.typography.commonAvatar,
            ...theme.typography.mediumAvatar,
            overflow: 'hidden',
            transition: 'all .2s ease-in-out',
            background:
              theme.palette.mode === 'dark'
                ? theme.palette.dark.main
                : theme.palette.secondary.light,
            color:
              theme.palette.mode === 'dark'
                ? theme.palette.secondary.main
                : theme.palette.secondary.dark,
            '&:hover': {
              background:
                theme.palette.mode === 'dark'
                  ? theme.palette.secondary.main
                  : theme.palette.secondary.dark,
              color:
                theme.palette.mode === 'dark'
                  ? theme.palette.secondary.light
                  : theme.palette.secondary.light,
            },
          }}
          onClick={() => dispatch(openDrawer(!drawerOpen))}
          color="inherit"
        >
          <TbMenu2 strokeWidth={1.5} size="20px" />
        </Avatar>
      </Box>
      <Box sx={{ flexGrow: 1 }} />
      <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
        <LanguageSection />
      </Box>
      <ProfileSection />
      <Box sx={{ display: { xs: 'block', sm: 'none' } }}>
        <MobileSection />
      </Box>
    </>
  )
}

export default Header
