import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormGroup } from '../../../components/forms/group/FormGroup'
import { gridSpacing } from '../../../libs/redux/constants'
import { groupCreateTabsOptions } from '../../../providers/GroupProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const GroupCreate = () => {
  const tabsPanel = [<FormGroup key={1} mode={'create'} />]

  const updatedTabs = groupCreateTabsOptions.map(
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

export default GroupCreate
