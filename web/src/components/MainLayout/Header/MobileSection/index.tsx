import {
  AppBar,
  Box,
  ClickAwayListener,
  Grid,
  IconButton,
  Paper,
  Popper,
  Toolbar,
  useMediaQuery,
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { useEffect, useRef, useState } from 'react'
import { TbDotsVertical } from 'react-icons/tb'
import Transition from '../../../Transition'
import { LanguageSection } from '../LanguageSection'

export const MobileSection = () => {
  const theme = useTheme()
  const matchMobile = useMediaQuery(theme.breakpoints.down('md'))

  const [open, setOpen] = useState(false)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const anchorRef = useRef<any>(null)

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

  return (
    <>
      <Box component="span" ref={anchorRef} sx={{ mt: 1, ml: 1 }}>
        <IconButton
          sx={{
            color: theme.palette.mode === 'dark' ? 'primary.main' : 'inherit',
            ml: 0.5,
            cursor: 'pointer',
          }}
          onClick={handleToggle}
        >
          <TbDotsVertical
            strokeWidth={1.5}
            aria-controls={open ? 'menu-list-grow' : undefined}
            aria-haspopup="true"
            style={{ fontSize: '1.5rem' }}
          />
        </IconButton>
      </Box>
      <Popper
        placement="bottom-end"
        open={open}
        anchorEl={anchorRef.current}
        nonce={''}
        onResize={undefined}
        onResizeCapture={undefined}
        role={undefined}
        transition
        disablePortal
        style={{ width: '100%', zIndex: 1 }}
        popperOptions={{
          modifiers: [
            {
              name: 'offset',
              options: {
                offset: [0, matchMobile ? 30 : 10],
              },
            },
          ],
        }}
      >
        {({ TransitionProps }) => (
          <ClickAwayListener onClickAway={handleClose}>
            <Transition
              type="zoom"
              in={open}
              {...TransitionProps}
              sx={{ transformOrigin: 'top right' }}
            >
              <Paper>
                {open && (
                  <AppBar
                    color="inherit"
                    sx={{
                      [theme.breakpoints.down('md')]: {
                        background:
                          theme.palette.mode === 'dark'
                            ? theme.palette.dark[800]
                            : '#fff',
                      },
                    }}
                  >
                    <Toolbar sx={{ pt: 2.75, pb: 2.75 }}>
                      <Grid
                        container
                        justifyContent={
                          matchMobile ? 'space-between' : 'flex-end'
                        }
                        alignItems="center"
                      >
                        <LanguageSection />
                      </Grid>
                    </Toolbar>
                  </AppBar>
                )}
              </Paper>
            </Transition>
          </ClickAwayListener>
        )}
      </Popper>
    </>
  )
}
