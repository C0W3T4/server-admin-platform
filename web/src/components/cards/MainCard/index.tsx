import {
  Card,
  CardContent,
  CardContentProps,
  CardHeader,
  CardHeaderProps,
  CardProps,
  Divider,
  Typography,
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { CSSProperties, ReactNode, Ref, forwardRef } from 'react'
import { KeyedObject } from '../../../types'

const headerSX = {
  '& .MuiCardHeader-action': { mr: 0 },
}

export interface MainCardProps extends KeyedObject {
  border?: boolean
  boxShadow?: boolean
  children: ReactNode | string
  style?: CSSProperties
  content?: boolean
  className?: string
  contentClass?: string
  contentSX?: CardContentProps['sx']
  darkTitle?: boolean
  sx?: CardProps['sx']
  secondary?: CardHeaderProps['action']
  shadow?: string
  elevation?: number
  title?: ReactNode | string
}

export const MainCard = forwardRef(
  (
    {
      border = true,
      boxShadow,
      children,
      content = true,
      contentClass = '',
      contentSX = {},
      darkTitle,
      secondary,
      shadow,
      sx = {},
      title,
      ...others
    }: MainCardProps,
    ref: Ref<HTMLDivElement>,
  ) => {
    const theme = useTheme()

    return (
      <Card
        ref={ref}
        {...others}
        sx={{
          border: border ? '1px solid' : 'none',
          borderColor:
            theme.palette.mode === 'dark'
              ? theme.palette.background.default
              : theme.palette.primary[200] + 75,
          ':hover': {
            boxShadow: boxShadow
              ? shadow ||
                (theme.palette.mode === 'dark'
                  ? '0 2px 14px 0 rgb(33 150 243 / 10%)'
                  : '0 2px 14px 0 rgb(32 40 45 / 8%)')
              : 'inherit',
          },
          ...sx,
        }}
      >
        {!darkTitle && title && (
          <CardHeader sx={headerSX} title={title} action={secondary} />
        )}
        {darkTitle && title && (
          <CardHeader
            sx={headerSX}
            title={<Typography variant="h3">{title}</Typography>}
            action={secondary}
          />
        )}
        {title && <Divider />}
        {content && (
          <CardContent sx={contentSX} className={contentClass}>
            {children}
          </CardContent>
        )}
        {!content && children}
      </Card>
    )
  },
)

MainCard.displayName = 'MainCard'
