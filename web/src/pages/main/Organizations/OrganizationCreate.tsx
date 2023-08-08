import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormOrganization } from '../../../components/forms/organization/FormOrganization'
import { gridSpacing } from '../../../libs/redux/constants'
import { organizationCreateTabsOptions } from '../../../providers/OrganizationProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const OrganizationCreate = () => {
  const tabsPanel = [<FormOrganization key={1} mode={'create'} />]

  const updatedTabs = organizationCreateTabsOptions.map(
    (tab: TabsOptionsProps, index: number) => {
      return { ...tab, children: tabsPanel[index] }
    },
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <TabsNav tabsOptions={updatedTabs} />
      </Grid>
    </Grid>
  )
}

export default OrganizationCreate
