import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { ScheduleTabDescription } from '../../../components/views/schedule/ScheduleTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { scheduleDetailsTabsOptions } from '../../../providers/ScheduleProvider'
import { ScheduleDataProps } from '../../../types/schedule'
import { TabsOptionsProps } from '../../../types/tabs'

const ScheduleDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<ScheduleDataProps>(
    `api/schedules/${id}`,
  )

  const tabsPanel = [<ScheduleTabDescription key={1} defaultValues={data} />]

  const updatedTabs = scheduleDetailsTabsOptions.map(
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

export default ScheduleDetails
