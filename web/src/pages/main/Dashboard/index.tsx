import { Grid } from '@mui/material'
import { AiOutlineCluster } from 'react-icons/ai'
import { FaUsers } from 'react-icons/fa'
import { IoMdGitNetwork } from 'react-icons/io'
import {
  TbBuilding,
  TbCalendarTime,
  TbFolders,
  TbKey,
  TbServer,
  TbTemplate,
  TbTiltShift,
} from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { TotalDarkCard } from '../../../components/cards/TotalDarkCard'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { DashboardTotalsProps } from '../../../types/dashboard'

const Dashboard = () => {
  const { data, isLoading } = useAxiosGet<DashboardTotalsProps>(
    `api/dashboards/totals`,
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/organizations/list"
              icon={TbBuilding}
              title={data?.total_organizations}
              subtitle={
                <FormattedMessage id="dashboards.labels.organizations" />
              }
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/teams/list"
              icon={FaUsers}
              title={data?.total_teams}
              subtitle={<FormattedMessage id="dashboards.labels.teams" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/credentials/list"
              icon={TbKey}
              title={data?.total_credentials}
              subtitle={<FormattedMessage id="dashboards.labels.credentials" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/inventories/list"
              icon={AiOutlineCluster}
              title={data?.total_inventories}
              subtitle={<FormattedMessage id="dashboards.labels.inventories" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/groups/list"
              icon={IoMdGitNetwork}
              title={data?.total_groups}
              subtitle={<FormattedMessage id="dashboards.labels.groups" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/hosts/list"
              icon={TbServer}
              title={data?.total_hosts}
              subtitle={<FormattedMessage id="dashboards.labels.hosts" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/projects/list"
              icon={TbFolders}
              title={data?.total_projects}
              subtitle={<FormattedMessage id="dashboards.labels.projects" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/templates/list"
              icon={TbTemplate}
              title={data?.total_templates}
              subtitle={<FormattedMessage id="dashboards.labels.templates" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/schedules/list"
              icon={TbCalendarTime}
              title={data?.total_schedules}
              subtitle={<FormattedMessage id="dashboards.labels.schedules" />}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={6} xl={4}>
            <TotalDarkCard
              isLoading={isLoading}
              link="/jobs/list"
              icon={TbTiltShift}
              title={data?.total_jobs}
              subtitle={<FormattedMessage id="dashboards.labels.jobs" />}
            />
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default Dashboard
