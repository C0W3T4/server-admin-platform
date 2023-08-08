import { ManageAccountsOutlined } from '@mui/icons-material'
import {
  Avatar,
  Box,
  Chip,
  ClickAwayListener,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper,
  Popper,
  Stack,
  Typography,
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { useEffect, useRef, useState } from 'react'
import { TbLogout, TbSettings } from 'react-icons/tb'
import { FormattedMessage, useIntl } from 'react-intl'
import PerfectScrollbar from 'react-perfect-scrollbar'
import { useNavigate } from 'react-router-dom'
import userImg from '../../../../assets/images/user.png'
import useAuth from '../../../../hooks/useAuth'
import useConfig from '../../../../hooks/useConfig'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { userTypeMap } from '../../../../providers/userProvider'
import Transition from '../../../Transition'
import { MainCard } from '../../../cards/MainCard'

export const ProfileSection = () => {
  const theme = useTheme()
  const { borderRadius } = useConfig()
  const navigate = useNavigate()
  const { formatMessage } = useIntl()

  const [selectedIndex, setSelectedIndex] = useState(-1)
  const { logout, user } = useAuth()
  const [open, setOpen] = useState(false)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const anchorRef = useRef<any>(null)
  const handleLogout = async () =>
    await logout().catch(() =>
      dispatch(
        openSnackbar({
          open: true,
          message: formatMessage({ id: 'snackbar.message.error.logout' }),
          transition: 'SlideUp',
          variant: 'alert',
          alert: {
            color: 'error',
          },
          close: true,
        }),
      ),
    )

  const handleListItemClick = (
    event: React.MouseEvent<HTMLDivElement>,
    index: number,
    route: string = '',
  ) => {
    setSelectedIndex(index)
    handleClose(event)

    if (route && route !== '') {
      navigate(route)
    }
  }
  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen)
  }
  const handleClose = (
    event: React.MouseEvent<HTMLDivElement> | MouseEvent | TouchEvent,
  ) => {
    if (anchorRef.current && anchorRef.current.contains(event.target)) {
      return
    }

    setOpen(false)
  }
  const prevOpen = useRef(open)
  useEffect(() => {
    if (prevOpen.current === true && open === false) {
      anchorRef.current.focus()
    }

    prevOpen.current = open
  }, [open])

  return (
    <>
      <Chip
        sx={{
          height: '48px',
          alignItems: 'center',
          borderRadius: '27px',
          transition: 'all .2s ease-in-out',
          borderColor:
            theme.palette.mode === 'dark'
              ? theme.palette.dark.main
              : theme.palette.primary.light,
          backgroundColor:
            theme.palette.mode === 'dark'
              ? theme.palette.dark.main
              : theme.palette.primary.light,
          '&[aria-controls="menu-list-grow"], &:hover': {
            borderColor: theme.palette.primary.main,
            background: `${theme.palette.primary.main}!important`,
            color: theme.palette.primary.light,
            '& svg': {
              stroke: theme.palette.primary.light,
            },
          },
          '& .MuiChip-label': {
            lineHeight: 0,
          },
        }}
        icon={
          <Avatar
            src={userImg}
            sx={{
              ...theme.typography.mediumAvatar,
              margin: '8px 0 8px 8px !important',
              cursor: 'pointer',
            }}
            ref={anchorRef}
            aria-controls={open ? 'menu-list-grow' : undefined}
            aria-haspopup="true"
            color="inherit"
          />
        }
        label={
          <TbSettings
            strokeWidth={1.5}
            size="24px"
            color={theme.palette.primary.main}
          />
        }
        variant="outlined"
        ref={anchorRef}
        aria-controls={open ? 'menu-list-grow' : undefined}
        aria-haspopup="true"
        onClick={handleToggle}
        color="primary"
      />

      <Popper
        placement="bottom"
        open={open}
        anchorEl={anchorRef.current}
        nonce={''}
        onResize={undefined}
        onResizeCapture={undefined}
        role={undefined}
        transition
        disablePortal
        popperOptions={{
          modifiers: [
            {
              name: 'offset',
              options: {
                offset: [0, 14],
              },
            },
          ],
        }}
      >
        {({ TransitionProps }) => (
          <ClickAwayListener onClickAway={handleClose}>
            <Transition in={open} {...TransitionProps}>
              <Paper>
                {open && (
                  <MainCard
                    border={false}
                    elevation={16}
                    content={false}
                    boxShadow
                    shadow={theme.shadows[16]}
                  >
                    <Box sx={{ p: 2, pb: 0 }}>
                      <Stack>
                        <Stack direction="row" alignItems="center">
                          <Typography variant="h4">
                            <FormattedMessage id="app.header.labels.hello" />
                          </Typography>
                          &nbsp;
                          <Typography
                            component="span"
                            variant="h4"
                            sx={{ fontWeight: 700 }}
                          >
                            {user?.first_name && user?.last_name
                              ? `${user.first_name} ${user.last_name}`
                              : user?.username && `${user?.username}`}
                          </Typography>
                        </Stack>
                        <Stack direction="row" alignItems="center">
                          {user?.user_type &&
                            userTypeMap.get(user.user_type)?.icon}
                          <Typography variant="subtitle2">
                            {user?.user_type && (
                              <FormattedMessage
                                id={userTypeMap.get(user.user_type)?.label}
                              />
                            )}
                          </Typography>
                        </Stack>
                      </Stack>
                      <Divider />
                    </Box>
                    <PerfectScrollbar
                      style={{
                        height: '100%',
                        maxHeight: 'calc(100vh - 250px)',
                        overflowX: 'hidden',
                      }}
                    >
                      <Box sx={{ p: 2, pt: 0 }}>
                        <List
                          component="nav"
                          sx={{
                            width: '100%',
                            maxWidth: 350,
                            minWidth: 300,
                            backgroundColor: theme.palette.background.paper,
                            borderRadius: '10px',
                            [theme.breakpoints.down('md')]: {
                              minWidth: '100%',
                            },
                            '& .MuiListItemButton-root': {
                              mt: 0.5,
                            },
                          }}
                        >
                          <ListItemButton
                            sx={{ borderRadius: `${borderRadius}px` }}
                            selected={selectedIndex === 0}
                            onClick={(
                              event: React.MouseEvent<HTMLDivElement>,
                            ) =>
                              handleListItemClick(event, 0, '/settings/account')
                            }
                          >
                            <ListItemIcon>
                              <ManageAccountsOutlined
                                sx={{ fontSize: '20px' }}
                              />
                            </ListItemIcon>
                            <ListItemText
                              primary={
                                <Typography variant="body2">
                                  <FormattedMessage id="app.header.labels.accountSettings" />
                                </Typography>
                              }
                            />
                          </ListItemButton>
                          <ListItemButton
                            sx={{ borderRadius: `${borderRadius}px` }}
                            selected={selectedIndex === 4}
                            onClick={handleLogout}
                          >
                            <ListItemIcon>
                              <TbLogout strokeWidth={1.5} size="20px" />
                            </ListItemIcon>
                            <ListItemText
                              primary={
                                <Typography variant="body2">
                                  <FormattedMessage id="app.header.labels.logout" />
                                </Typography>
                              }
                            />
                          </ListItemButton>
                        </List>
                      </Box>
                    </PerfectScrollbar>
                  </MainCard>
                )}
              </Paper>
            </Transition>
          </ClickAwayListener>
        )}
      </Popper>
    </>
  )
}
