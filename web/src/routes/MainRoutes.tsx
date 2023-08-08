import { lazy } from 'react'
import { RouteObject } from 'react-router-dom'
import { Loadable } from '../components/Loadable'
import { MainLayout } from '../components/MainLayout'
import AuthGuard from '../guards/AuthGuard'
import RolesGuard from '../guards/RolesGuard'
import { UserType } from '../types/user'

const DashboardDefault = Loadable(lazy(() => import('../pages/main/Dashboard')))
const DashboardAnalytics = Loadable(
  lazy(() => import('../pages/main/Analytics')),
)

const Jobs = Loadable(lazy(() => import('../pages/main/Jobs')))
const JobsList = Loadable(lazy(() => import('../pages/main/Jobs/JobsList')))
const JobDetails = Loadable(lazy(() => import('../pages/main/Jobs/JobDetails')))

const Credentials = Loadable(lazy(() => import('../pages/main/Credentials')))
const CredentialsList = Loadable(
  lazy(() => import('../pages/main/Credentials/CredentialsList')),
)
const CredentialCreate = Loadable(
  lazy(() => import('../pages/main/Credentials/CredentialCreate')),
)
const CredentialDetails = Loadable(
  lazy(() => import('../pages/main/Credentials/CredentialDetails')),
)
const CredentialEdit = Loadable(
  lazy(() => import('../pages/main/Credentials/CredentialEdit')),
)

const Inventories = Loadable(lazy(() => import('../pages/main/Inventories')))
const InventoriesList = Loadable(
  lazy(() => import('../pages/main/Inventories/InventoriesList')),
)
const InventoryCreate = Loadable(
  lazy(() => import('../pages/main/Inventories/InventoryCreate')),
)
const InventoryDetails = Loadable(
  lazy(() => import('../pages/main/Inventories/InventoryDetails')),
)
const InventoryEdit = Loadable(
  lazy(() => import('../pages/main/Inventories/InventoryEdit')),
)

const Groups = Loadable(lazy(() => import('../pages/main/Groups')))
const GroupsList = Loadable(
  lazy(() => import('../pages/main/Groups/GroupsList')),
)
const GroupCreate = Loadable(
  lazy(() => import('../pages/main/Groups/GroupCreate')),
)
const GroupDetails = Loadable(
  lazy(() => import('../pages/main/Groups/GroupDetails')),
)
const GroupEdit = Loadable(lazy(() => import('../pages/main/Groups/GroupEdit')))

const Hosts = Loadable(lazy(() => import('../pages/main/Hosts')))
const HostsList = Loadable(lazy(() => import('../pages/main/Hosts/HostsList')))
const HostCreate = Loadable(
  lazy(() => import('../pages/main/Hosts/HostCreate')),
)
const HostDetails = Loadable(
  lazy(() => import('../pages/main/Hosts/HostDetails')),
)
const HostEdit = Loadable(lazy(() => import('../pages/main/Hosts/HostEdit')))

const Projects = Loadable(lazy(() => import('../pages/main/Projects')))
const ProjectsList = Loadable(
  lazy(() => import('../pages/main/Projects/ProjectsList')),
)
const ProjectCreate = Loadable(
  lazy(() => import('../pages/main/Projects/ProjectCreate')),
)
const ProjectDetails = Loadable(
  lazy(() => import('../pages/main/Projects/ProjectDetails')),
)
const ProjectEdit = Loadable(
  lazy(() => import('../pages/main/Projects/ProjectEdit')),
)

const Schedules = Loadable(lazy(() => import('../pages/main/Schedules')))
const SchedulesList = Loadable(
  lazy(() => import('../pages/main/Schedules/SchedulesList')),
)
const ScheduleCreate = Loadable(
  lazy(() => import('../pages/main/Schedules/ScheduleCreate')),
)
const ScheduleDetails = Loadable(
  lazy(() => import('../pages/main/Schedules/ScheduleDetails')),
)
const ScheduleEdit = Loadable(
  lazy(() => import('../pages/main/Schedules/ScheduleEdit')),
)

const Templates = Loadable(lazy(() => import('../pages/main/Templates')))
const TemplatesList = Loadable(
  lazy(() => import('../pages/main/Templates/TemplatesList')),
)
const TemplateCreate = Loadable(
  lazy(() => import('../pages/main/Templates/TemplateCreate')),
)
const TemplateDetails = Loadable(
  lazy(() => import('../pages/main/Templates/TemplateDetails')),
)
const TemplateEdit = Loadable(
  lazy(() => import('../pages/main/Templates/TemplateEdit')),
)

const Users = Loadable(lazy(() => import('../pages/main/Users')))
const UsersList = Loadable(lazy(() => import('../pages/main/Users/UsersList')))
const UserCreate = Loadable(
  lazy(() => import('../pages/main/Users/UserCreate')),
)
const UserDetails = Loadable(
  lazy(() => import('../pages/main/Users/UserDetails')),
)
const UserEdit = Loadable(lazy(() => import('../pages/main/Users/UserEdit')))

const Teams = Loadable(lazy(() => import('../pages/main/Teams')))
const TeamsList = Loadable(lazy(() => import('../pages/main/Teams/TeamsList')))
const TeamCreate = Loadable(
  lazy(() => import('../pages/main/Teams/TeamCreate')),
)
const TeamDetails = Loadable(
  lazy(() => import('../pages/main/Teams/TeamDetails')),
)
const TeamEdit = Loadable(lazy(() => import('../pages/main/Teams/TeamEdit')))

const Organizations = Loadable(
  lazy(() => import('../pages/main/Organizations')),
)
const OrganizationsList = Loadable(
  lazy(() => import('../pages/main/Organizations/OrganizationsList')),
)
const OrganizationCreate = Loadable(
  lazy(() => import('../pages/main/Organizations/OrganizationCreate')),
)
const OrganizationDetails = Loadable(
  lazy(() => import('../pages/main/Organizations/OrganizationDetails')),
)
const OrganizationEdit = Loadable(
  lazy(() => import('../pages/main/Organizations/OrganizationEdit')),
)

const Settings = Loadable(lazy(() => import('../pages/main/Settings')))
const SettingsSystem = Loadable(
  lazy(() => import('../pages/main/Settings/SettingsSystem')),
)
const MyAccount = Loadable(
  lazy(() => import('../pages/main/Settings/MyAccount')),
)

export const MainRoutes: RouteObject = {
  path: '/',
  element: (
    <AuthGuard>
      <MainLayout />
    </AuthGuard>
  ),
  children: [
    {
      path: 'dashboard',
      children: [
        {
          path: 'default',
          element: <DashboardDefault />,
        },
        {
          path: 'analytics',
          element: <DashboardAnalytics />,
        },
      ],
    },
    {
      path: 'jobs',
      element: <Jobs />,
      children: [
        {
          path: 'list',
          element: <JobsList />,
        },
        {
          path: 'details/:id',
          element: <JobDetails />,
        },
      ],
    },
    {
      path: 'credentials',
      element: <Credentials />,
      children: [
        {
          path: 'list',
          element: <CredentialsList />,
        },
        {
          path: 'create',
          element: <CredentialCreate />,
        },
        {
          path: 'details/:id',
          element: <CredentialDetails />,
        },
        {
          path: 'edit/:id',
          element: <CredentialEdit />,
        },
      ],
    },
    {
      path: 'inventories',
      element: <Inventories />,
      children: [
        {
          path: 'list',
          element: <InventoriesList />,
        },
        {
          path: 'create',
          element: <InventoryCreate />,
        },
        {
          path: 'details/:id',
          element: <InventoryDetails />,
        },
        {
          path: 'edit/:id',
          element: <InventoryEdit />,
        },
      ],
    },
    {
      path: 'groups',
      element: <Groups />,
      children: [
        {
          path: 'list',
          element: <GroupsList />,
        },
        {
          path: 'create',
          element: <GroupCreate />,
        },
        {
          path: 'details/:id',
          element: <GroupDetails />,
        },
        {
          path: 'edit/:id',
          element: <GroupEdit />,
        },
      ],
    },
    {
      path: 'hosts',
      element: <Hosts />,
      children: [
        {
          path: 'list',
          element: <HostsList />,
        },
        {
          path: 'create',
          element: <HostCreate />,
        },
        {
          path: 'details/:id',
          element: <HostDetails />,
        },
        {
          path: 'edit/:id',
          element: <HostEdit />,
        },
      ],
    },
    {
      path: 'projects',
      element: <Projects />,
      children: [
        {
          path: 'list',
          element: <ProjectsList />,
        },
        {
          path: 'create',
          element: <ProjectCreate />,
        },
        {
          path: 'details/:id',
          element: <ProjectDetails />,
        },
        {
          path: 'edit/:id',
          element: <ProjectEdit />,
        },
      ],
    },
    {
      path: 'schedules',
      element: <Schedules />,
      children: [
        {
          path: 'list',
          element: <SchedulesList />,
        },
        {
          path: 'create',
          element: <ScheduleCreate />,
        },
        {
          path: 'details/:id',
          element: <ScheduleDetails />,
        },
        {
          path: 'edit/:id',
          element: <ScheduleEdit />,
        },
      ],
    },
    {
      path: 'templates',
      element: <Templates />,
      children: [
        {
          path: 'list',
          element: <TemplatesList />,
        },
        {
          path: 'create',
          element: <TemplateCreate />,
        },
        {
          path: 'details/:id',
          element: <TemplateDetails />,
        },
        {
          path: 'edit/:id',
          element: <TemplateEdit />,
        },
      ],
    },
    {
      path: 'users',
      element: <Users />,
      children: [
        {
          path: 'list',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <UsersList />
            </RolesGuard>
          ),
        },
        {
          path: 'create',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <UserCreate />
            </RolesGuard>
          ),
        },
        {
          path: 'details/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <UserDetails />
            </RolesGuard>
          ),
        },
        {
          path: 'edit/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <UserEdit />
            </RolesGuard>
          ),
        },
      ],
    },
    {
      path: 'teams',
      element: <Teams />,
      children: [
        {
          path: 'list',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <TeamsList />
            </RolesGuard>
          ),
        },
        {
          path: 'create',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <TeamCreate />
            </RolesGuard>
          ),
        },
        {
          path: 'details/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <TeamDetails />
            </RolesGuard>
          ),
        },
        {
          path: 'edit/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <TeamEdit />
            </RolesGuard>
          ),
        },
      ],
    },
    {
      path: 'organizations',
      element: <Organizations />,
      children: [
        {
          path: 'list',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <OrganizationsList />
            </RolesGuard>
          ),
        },
        {
          path: 'create',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <OrganizationCreate />
            </RolesGuard>
          ),
        },
        {
          path: 'details/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_AUDITOR}>
              <OrganizationDetails />
            </RolesGuard>
          ),
        },
        {
          path: 'edit/:id',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <OrganizationEdit />
            </RolesGuard>
          ),
        },
      ],
    },
    {
      path: 'settings',
      element: <Settings />,
      children: [
        {
          path: 'account',
          element: <MyAccount />,
        },
        {
          path: 'system',
          element: (
            <RolesGuard user_type={UserType.SYSTEM_ADMINISTRATOR}>
              <SettingsSystem />
            </RolesGuard>
          ),
        },
      ],
    },
  ],
}
