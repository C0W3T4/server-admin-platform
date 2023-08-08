import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormSchedule } from '../../../components/forms/schedule/FormSchedule'
import { gridSpacing } from '../../../libs/redux/constants'
import { scheduleCreateTabsOptions } from '../../../providers/ScheduleProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const ScheduleCreate = () => {
  const tabsPanel = [<FormSchedule key={1} mode={'create'} />]

  const updatedTabs = scheduleCreateTabsOptions.map(
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

export default ScheduleCreate
