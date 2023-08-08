import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormHost } from '../../../components/forms/host/FormHost'
import { gridSpacing } from '../../../libs/redux/constants'
import { hostCreateTabsOptions } from '../../../providers/HostProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const HostCreate = () => {
  const tabsPanel = [<FormHost key={1} mode={'create'} />]

  const updatedTabs = hostCreateTabsOptions.map(
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

export default HostCreate
