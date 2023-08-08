import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormOrganization } from '../../../components/forms/organization/FormOrganization'
import { OrganizationTeamsList } from '../../../components/views/organization/OrganizationTeamsList'
import { OrganizationUsersList } from '../../../components/views/organization/OrganizationUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { organizationEditTabsOptions } from '../../../providers/OrganizationProvider'
import { OrganizationDataProps } from '../../../types/organization'
import { TabsOptionsProps } from '../../../types/tabs'

const OrganizationEdit = () => {
  const { id } = useParams()

  const { data: organizationData, isLoading: organizationIsLoading } =
    useAxiosGet<OrganizationDataProps>(`api/organizations/${id}`)

  const tabsPanel = [
    <FormOrganization key={1} mode={'edit'} defaultValues={organizationData} />,
    <OrganizationUsersList key={2} organizationData={organizationData} />,
    <OrganizationTeamsList key={3} organizationData={organizationData} />,
  ]

  const updatedTabs = organizationEditTabsOptions.map(
    (tab: TabsOptionsProps, index: number) => {
      return { ...tab, children: tabsPanel[index] }
    },
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        {!organizationIsLoading && <TabsNav tabsOptions={updatedTabs} />}
      </Grid>
    </Grid>
  )
}

export default OrganizationEdit
