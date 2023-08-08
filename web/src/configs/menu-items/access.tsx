import { FaUsers } from 'react-icons/fa'
import { TbBuilding, TbCirclePlus, TbList, TbUsers } from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { NavItemType } from '../../types/menu'

const access: NavItemType = {
  id: 'access',
  title: <FormattedMessage id="app.sidebar.labels.access" />,
  type: 'group',
  divider: true,
  breadcrumbs: true,
  children: [
    {
      id: 'users',
      title: <FormattedMessage id="app.sidebar.labels.users" />,
      type: 'collapse',
      icon: TbUsers,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/users/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/users/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'teams',
      title: <FormattedMessage id="app.sidebar.labels.teams" />,
      type: 'collapse',
      icon: FaUsers,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/teams/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/teams/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'organizations',
      title: <FormattedMessage id="app.sidebar.labels.organizations" />,
      type: 'collapse',
      icon: TbBuilding,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/organizations/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/organizations/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
  ],
}

export default access
