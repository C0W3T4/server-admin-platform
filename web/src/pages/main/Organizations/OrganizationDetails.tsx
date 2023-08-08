import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { OrganizationTabDescription } from '../../../components/views/organization/OrganizationTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { organizationDetailsTabsOptions } from '../../../providers/OrganizationProvider'
import { OrganizationDataProps } from '../../../types/organization'
import { TabsOptionsProps } from '../../../types/tabs'

const OrganizationDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<OrganizationDataProps>(
    `api/organizations/${id}`,
  )

  const tabsPanel = [
    <OrganizationTabDescription key={1} defaultValues={data} />,
  ]

  const updatedTabs = organizationDetailsTabsOptions.map(
    (tab: TabsOptionsProps, index: number) => {
      return { ...tab, children: tabsPanel[index] }
    },
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        {!isLoading && <TabsNav tabsOptions={updatedTabs} />}
      </Grid>
    </Grid>
  )
}

export default OrganizationDetails
