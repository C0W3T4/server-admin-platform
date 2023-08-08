import { Divider, List, Typography } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { FormattedMessage } from 'react-intl'
import { NavItemType } from '../../../../../types/menu'
import NavCollapse from '../NavCollapse'
import NavItem from '../NavItem'

const NavGroup = ({ item }: { item: NavItemType }) => {
  const theme = useTheme()

  const items = item.children?.map((menu) => {
    switch (menu.type) {
      case 'collapse':
        return <NavCollapse key={menu.id} menu={menu} level={1} />
      case 'item':
        return <NavItem key={menu.id} item={menu} level={1} />
      default:
        return (
          <Typography key={menu.id} variant="h6" color="error" align="center">
            <FormattedMessage id="errors.menu.items" />
          </Typography>
        )
    }
  })

  return (
    <>
      <List
        subheader={
          item.title && (
            <Typography
              variant="caption"
              sx={{ ...theme.typography.menuCaption }}
              display="block"
              gutterBottom
            >
              {item.title}
              {item.caption && (
                <Typography
                  variant="caption"
                  sx={{ ...theme.typography.subMenuCaption }}
                  display="block"
                  gutterBottom
                >
                  {item.caption}
                </Typography>
              )}
            </Typography>
          )
        }
      >
        {items}
      </List>
      {item.divider && <Divider sx={{ mt: 0.25, mb: 1.25 }} />}
    </>
  )
}

export default NavGroup
