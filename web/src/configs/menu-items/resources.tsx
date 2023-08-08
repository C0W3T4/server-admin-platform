import { AiOutlineCluster } from 'react-icons/ai'
import { IoMdGitNetwork } from 'react-icons/io'
import {
  TbCalendarTime,
  TbCirclePlus,
  TbFolders,
  TbKey,
  TbList,
  TbServer,
  TbTemplate,
} from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { NavItemType } from '../../types/menu'

const resources: NavItemType = {
  id: 'resources',
  title: <FormattedMessage id="app.sidebar.labels.resources" />,
  type: 'group',
  divider: true,
  breadcrumbs: true,
  children: [
    {
      id: 'templates',
      title: <FormattedMessage id="app.sidebar.labels.templates" />,
      type: 'collapse',
      icon: TbTemplate,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/templates/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/templates/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'credentials',
      title: <FormattedMessage id="app.sidebar.labels.credentials" />,
      type: 'collapse',
      icon: TbKey,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/credentials/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/credentials/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'projects',
      title: <FormattedMessage id="app.sidebar.labels.projects" />,
      type: 'collapse',
      icon: TbFolders,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/projects/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/projects/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'inventories',
      title: <FormattedMessage id="app.sidebar.labels.inventories" />,
      type: 'collapse',
      icon: AiOutlineCluster,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/inventories/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/inventories/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'groups',
      title: <FormattedMessage id="app.sidebar.labels.groups" />,
      type: 'collapse',
      icon: IoMdGitNetwork,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/groups/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/groups/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'hosts',
      title: <FormattedMessage id="app.sidebar.labels.hosts" />,
      type: 'collapse',
      icon: TbServer,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/hosts/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/hosts/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
    {
      id: 'schedules',
      title: <FormattedMessage id="app.sidebar.labels.schedules" />,
      type: 'collapse',
      icon: TbCalendarTime,
      breadcrumbs: true,
      children: [
        {
          id: 'list',
          title: <FormattedMessage id="app.sidebar.labels.list" />,
          type: 'item',
          url: '/schedules/list',
          icon: TbList,
          breadcrumbs: true,
        },
        {
          id: 'create',
          title: <FormattedMessage id="app.sidebar.labels.create" />,
          type: 'item',
          url: '/schedules/create',
          icon: TbCirclePlus,
          breadcrumbs: true,
        },
      ],
    },
  ],
}

export default resources
