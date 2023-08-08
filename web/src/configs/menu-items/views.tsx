import { TbLayoutDashboard, TbTiltShift } from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { NavItemType } from '../../types/menu'

const views: NavItemType = {
  id: 'views',
  title: <FormattedMessage id="app.sidebar.labels.views" />,
  type: 'group',
  divider: true,
  breadcrumbs: true,
  children: [
    {
      id: 'dashboard',
      title: <FormattedMessage id="app.sidebar.labels.dashboard" />,
      type: 'item', // type: 'collapse',
      url: '/dashboard/default',
      icon: TbLayoutDashboard,
      breadcrumbs: true,
      // children: [
      //   {
      //     id: 'main',
      //     title: <FormattedMessage id="app.sidebar.labels.main" />,
      //     type: 'item',
      //     url: '/dashboard/default',
      //     icon: TbDashboard,
      //     breadcrumbs: true
      //   },
      //   {
      //     id: 'analytics',
      //     title: <FormattedMessage id="app.sidebar.labels.analytics" />,
      //     type: 'item',
      //     url: '/dashboard/analytics',
      //     icon: TbDeviceAnalytics,
      //     breadcrumbs: true
      //   }
      // ]
    },
    {
      id: 'jobs',
      title: <FormattedMessage id="app.sidebar.labels.jobs" />,
      type: 'item',
      url: '/jobs/list',
      icon: TbTiltShift,
      breadcrumbs: true,
    },
  ],
}

export default views
