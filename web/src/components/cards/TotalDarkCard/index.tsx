import {
  Avatar,
  Box,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Typography,
} from '@mui/material'
import { styled, useTheme } from '@mui/material/styles'
import { ReactElement } from 'react'
import { Link } from 'react-router-dom'
import { OverrideIcon } from '../../../types'
import { MainCard } from '../MainCard'
import TotalCard from '../TotalCard'

const CardWrapper = styled(MainCard)(({ theme }) => ({
  overflow: 'hidden',
  position: 'relative',
  '&:after': {
    content: '""',
    position: 'absolute',
    width: 210,
    height: 210,
    background: `linear-gradient(210.04deg, ${theme.palette.warning.dark} -50.94%, rgba(144, 202, 249, 0) 83.49%)`,
    borderRadius: '50%',
    top: -30,
    right: -180,
  },
  '&:before': {
    content: '""',
    position: 'absolute',
    width: 210,
    height: 210,
    background: `linear-gradient(140.9deg, ${theme.palette.warning.dark} -14.02%, rgba(144, 202, 249, 0) 70.50%)`,
    borderRadius: '50%',
    top: -160,
    right: -130,
  },
}))

interface TotalDarkCardProps {
  isLoading: boolean
  title?: string | number | ReactElement
  subtitle?: string | number | ReactElement
  icon?: OverrideIcon
  link?: string
}

export const TotalDarkCard = ({
  isLoading,
  icon,
  title,
  subtitle,
  link,
}: TotalDarkCardProps) => {
  const theme = useTheme()

  const Icon = icon!

  return (
    <>
      {isLoading ? (
        <TotalCard />
      ) : (
        <CardWrapper border={false} content={false}>
          <Box sx={{ p: 2 }}>
            <List sx={{ py: 0 }}>
              <ListItem
                component={Link}
                to={link || ''}
                alignItems="center"
                disableGutters
                sx={{ py: 0 }}
              >
                {icon && (
                  <ListItemAvatar>
                    <Avatar
                      variant="rounded"
                      sx={{
                        ...theme.typography.commonAvatar,
                        ...theme.typography.largeAvatar,
                        backgroundColor:
                          theme.palette.mode === 'dark'
                            ? theme.palette.dark.main
                            : theme.palette.warning.light,
                        color:
                          theme.palette.mode === 'dark'
                            ? theme.palette.warning.dark
                            : theme.palette.warning.dark,
                      }}
                    >
                      <Icon strokeWidth={1.5} size="24px" />
                    </Avatar>
                  </ListItemAvatar>
                )}
                <ListItemText
                  sx={{
                    py: 0,
                    mt: 0.45,
                    mb: 0.45,
                  }}
                  primary={
                    title && <Typography variant="h4">{title}</Typography>
                  }
                  secondary={
                    subtitle && (
                      <Typography
                        variant="subtitle2"
                        sx={{
                          color: theme.palette.grey[500],
                          mt: 0.5,
                        }}
                      >
                        {subtitle}
                      </Typography>
                    )
                  }
                />
              </ListItem>
            </List>
          </Box>
        </CardWrapper>
      )}
    </>
  )
}
