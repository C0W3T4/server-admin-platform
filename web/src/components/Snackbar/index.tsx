import CloseIcon from '@mui/icons-material/Close'
import {
  Alert,
  Button,
  Fade,
  Grow,
  IconButton,
  Slide,
  SlideProps,
} from '@mui/material'
import MuiSnackbar from '@mui/material/Snackbar'
import { SyntheticEvent } from 'react'
import { FormattedMessage } from 'react-intl'
import { useDispatch, useSelector } from '../../libs/redux'
import { closeSnackbar } from '../../libs/redux/slices/snackbar'
import { KeyedObject } from '../../types'

function TransitionSlideLeft(props: SlideProps) {
  return <Slide {...props} direction="left" />
}

function TransitionSlideUp(props: SlideProps) {
  return <Slide {...props} direction="up" />
}

function TransitionSlideRight(props: SlideProps) {
  return <Slide {...props} direction="right" />
}

function TransitionSlideDown(props: SlideProps) {
  return <Slide {...props} direction="down" />
}

function GrowTransition(props: SlideProps) {
  return <Grow {...props} />
}

const animation: KeyedObject = {
  SlideLeft: TransitionSlideLeft,
  SlideUp: TransitionSlideUp,
  SlideRight: TransitionSlideRight,
  SlideDown: TransitionSlideDown,
  Grow: GrowTransition,
  Fade,
}

export const Snackbar = () => {
  const dispatch = useDispatch()
  const snackbar = useSelector((state) => state.snackbar)
  const {
    actionButton,
    anchorOrigin,
    alert,
    close,
    message,
    open,
    transition,
    variant,
  } = snackbar

  const handleClose = (_event: SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return
    }
    dispatch(closeSnackbar())
  }

  return (
    <>
      {variant === 'default' && (
        <MuiSnackbar
          anchorOrigin={anchorOrigin}
          open={open}
          autoHideDuration={1250}
          onClose={handleClose}
          message={message}
          TransitionComponent={animation[transition]}
          action={
            <>
              <Button color="secondary" size="small" onClick={handleClose}>
                <FormattedMessage id="snackbar.labels.undo" />
              </Button>
              <IconButton
                size="small"
                aria-label="close"
                color="inherit"
                onClick={handleClose}
                sx={{ mt: 0.25 }}
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </>
          }
        />
      )}
      {variant === 'alert' && (
        <MuiSnackbar
          TransitionComponent={animation[transition]}
          anchorOrigin={anchorOrigin}
          open={open}
          autoHideDuration={1250}
          onClose={handleClose}
        >
          <Alert
            variant={alert.variant}
            color={alert.color}
            action={
              <>
                {actionButton !== false && (
                  <Button
                    size="small"
                    onClick={handleClose}
                    sx={{ color: 'background.paper' }}
                  >
                    <FormattedMessage id="snackbar.labels.undo" />
                  </Button>
                )}
                {close !== false && (
                  <IconButton
                    sx={{ color: 'background.paper' }}
                    size="small"
                    aria-label="close"
                    onClick={handleClose}
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                )}
              </>
            }
            sx={{
              ...(alert.variant === 'outlined' && {
                bgcolor: 'background.paper',
              }),
            }}
          >
            {message}
          </Alert>
        </MuiSnackbar>
      )}
    </>
  )
}
