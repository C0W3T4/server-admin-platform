import { ManageAccountsOutlined } from '@mui/icons-material'
import { GiEvilTower } from 'react-icons/gi'
import { TbSettings } from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { NavItemType } from '../../types/menu'

const administration: NavItemType = {
  id: 'administration',
  title: <FormattedMessage id="app.sidebar.labels.administration" />,
  type: 'group',
  divider: true,
  breadcrumbs: true,
  children: [
    {
      id: 'settings',
      title: <FormattedMessage id="app.sidebar.labels.settings" />,
      type: 'collapse',
      icon: TbSettings,
      breadcrumbs: true,
      children: [
        {
          id: 'account',
          title: <FormattedMessage id="app.sidebar.labels.account" />,
          type: 'item',
          url: '/settings/account',
          icon: ManageAccountsOutlined,
          breadcrumbs: true,
        },
        {
          id: 'system',
          title: <FormattedMessage id="app.sidebar.labels.system" />,
          type: 'item',
          url: '/settings/system',
          icon: GiEvilTower,
          breadcrumbs: true,
        },
      ],
    },
  ],
}

export default administration
