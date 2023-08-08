import { NavItemType } from '../../types/menu'
import access from './access'
import administration from './administration'
import resources from './resources'
import views from './views'

const menuItems: { items: NavItemType[] } = {
  items: [views, resources, access, administration],
}

export default menuItems
