import { Box, Collapse, Fade, Grow, Slide, Zoom } from '@mui/material'
import {
  CSSProperties,
  ExoticComponent,
  ReactElement,
  Ref,
  forwardRef,
} from 'react'

interface TSProps {
  children?: ReactElement
  position?: string
  sx?: CSSProperties
  in?: boolean
  type?: string
  direction?: 'up' | 'right' | 'left' | 'down'
  [others: string]: unknown
}

const Transition = forwardRef(
  (
    { children, position, sx, type, direction, ...others }: TSProps,
    ref: Ref<ExoticComponent>,
  ) => {
    let positionSX = {
      transformOrigin: '0 0 0',
    }

    switch (position) {
      case 'top-right':
        positionSX = {
          transformOrigin: 'top right',
        }
        break
      case 'top':
        positionSX = {
          transformOrigin: 'top',
        }
        break
      case 'bottom-left':
        positionSX = {
          transformOrigin: 'bottom left',
        }
        break
      case 'bottom-right':
        positionSX = {
          transformOrigin: 'bottom right',
        }
        break
      case 'bottom':
        positionSX = {
          transformOrigin: 'bottom',
        }
        break
      case 'top-left':
      default:
        positionSX = {
          transformOrigin: '0 0 0',
        }
        break
    }

    return (
      <Box ref={ref} sx={sx}>
        {type === 'grow' && (
          <Grow {...others}>
            <Box sx={positionSX}>{children}</Box>
          </Grow>
        )}
        {type === 'collapse' && (
          <Collapse {...others} sx={positionSX}>
            {children}
          </Collapse>
        )}
        {type === 'fade' && (
          <Fade
            {...others}
            timeout={{
              appear: 500,
              enter: 600,
              exit: 400,
            }}
          >
            <Box sx={positionSX}>{children}</Box>
          </Fade>
        )}
        {type === 'slide' && (
          <Slide
            {...others}
            timeout={{
              appear: 0,
              enter: 400,
              exit: 200,
            }}
            direction={direction}
          >
            <Box sx={positionSX}>{children}</Box>
          </Slide>
        )}
        {type === 'zoom' && (
          <Zoom {...others}>
            <Box sx={positionSX}>{children}</Box>
          </Zoom>
        )}
      </Box>
    )
  },
)

Transition.displayName = 'Transition'

Transition.defaultProps = {
  type: 'grow',
  position: 'top-left',
  direction: 'up',
}

export default Transition
