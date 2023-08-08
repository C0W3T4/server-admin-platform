import { Typography } from '@mui/material'
import { memo } from 'react'
import { FormattedMessage } from 'react-intl'
import menuItems from '../../../../configs/menu-items'
import { NavItemType } from '../../../../types/menu'
import NavGroup from './NavGroup'

const MenuList = () => {
  const navItems = menuItems.items.map((item: NavItemType) => {
    switch (item.type) {
      case 'group':
        return <NavGroup key={item.id} item={item} />
      default:
        return (
          <Typography key={item.id} variant="h6" color="error" align="center">
            <FormattedMessage id="errors.menu.items" />
          </Typography>
        )
    }
  })

  return <>{navItems}</>
}

export default memo(MenuList)
