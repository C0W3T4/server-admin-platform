import TranslateTwoToneIcon from '@mui/icons-material/TranslateTwoTone'
import {
  Avatar,
  Box,
  ClickAwayListener,
  Grid,
  List,
  ListItemButton,
  ListItemText,
  Paper,
  Popper,
  Typography,
  useMediaQuery,
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { useEffect, useRef, useState } from 'react'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import Transition from '../../../Transition'

export const LanguageSection = () => {
  const { borderRadius, locale, onChangeLocale } = useConfig()

  const theme = useTheme()
  const matchesXs = useMediaQuery(theme.breakpoints.down('md'))

  const [open, setOpen] = useState(false)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const anchorRef = useRef<any>(null)
  const [language, setLanguage] = useState<string>(locale)

  const handleListItemClick = (
    _event:
      | React.MouseEvent<HTMLAnchorElement>
      | React.MouseEvent<HTMLDivElement, MouseEvent>,
    lng: string,
  ) => {
    setLanguage(lng)
    onChangeLocale(lng)
    setOpen(false)
  }

  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen)
  }

  const handleClose = (event: MouseEvent | TouchEvent) => {
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

  useEffect(() => {
    setLanguage(locale)
  }, [locale])

  return (
    <>
      <Box
        sx={{
          ml: 2,
          [theme.breakpoints.down('md')]: {
            ml: 1,
          },
        }}
      >
        <Avatar
          variant="rounded"
          sx={{
            ...theme.typography.commonAvatar,
            ...theme.typography.mediumAvatar,
            border: '1px solid',
            borderColor:
              theme.palette.mode === 'dark'
                ? theme.palette.dark.main
                : theme.palette.primary.light,
            background:
              theme.palette.mode === 'dark'
                ? theme.palette.dark.main
                : theme.palette.primary.light,
            color: theme.palette.primary.dark,
            transition: 'all .2s ease-in-out',
            '&[aria-controls="menu-list-grow"],&:hover': {
              borderColor: theme.palette.primary.main,
              background: theme.palette.primary.main,
              color: theme.palette.primary.light,
            },
          }}
          ref={anchorRef}
          aria-controls={open ? 'menu-list-grow' : undefined}
          aria-haspopup="true"
          onClick={handleToggle}
          color="inherit"
        >
          {language !== 'en' && (
            <Typography
              variant="h5"
              sx={{ textTransform: 'uppercase' }}
              color="inherit"
            >
              {language}
            </Typography>
          )}
          {language === 'en' && (
            <TranslateTwoToneIcon sx={{ fontSize: '1.3rem' }} />
          )}
        </Avatar>
      </Box>
      <Popper
        placement={matchesXs ? 'bottom-start' : 'bottom'}
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
                offset: [matchesXs ? 0 : 0, 20],
              },
            },
          ],
        }}
      >
        {({ TransitionProps }) => (
          <ClickAwayListener onClickAway={handleClose}>
            <Transition
              position={matchesXs ? 'top-left' : 'top'}
              in={open}
              {...TransitionProps}
            >
              <Paper elevation={16}>
                {open && (
                  <List
                    component="nav"
                    sx={{
                      width: '100%',
                      minWidth: 200,
                      maxWidth: 280,
                      bgcolor: theme.palette.background.paper,
                      borderRadius: `${borderRadius}px`,
                      [theme.breakpoints.down('md')]: {
                        maxWidth: 250,
                      },
                    }}
                  >
                    <ListItemButton
                      selected={language === 'en'}
                      onClick={(event) => handleListItemClick(event, 'en')}
                    >
                      <ListItemText
                        primary={
                          <Grid container>
                            <Typography color="textPrimary">
                              <FormattedMessage id="language.en_uk" />
                            </Typography>
                          </Grid>
                        }
                      />
                    </ListItemButton>
                    <ListItemButton
                      selected={language === 'pt'}
                      onClick={(event) => handleListItemClick(event, 'pt')}
                    >
                      <ListItemText
                        primary={
                          <Grid container>
                            <Typography color="textPrimary">
                              <FormattedMessage id="language.pt_pt" />
                            </Typography>
                          </Grid>
                        }
                      />
                    </ListItemButton>
                  </List>
                )}
              </Paper>
            </Transition>
          </ClickAwayListener>
        )}
      </Popper>
    </>
  )
}
