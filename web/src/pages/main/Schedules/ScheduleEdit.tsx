import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormSchedule } from '../../../components/forms/schedule/FormSchedule'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { scheduleEditTabsOptions } from '../../../providers/ScheduleProvider'
import { ScheduleDataProps } from '../../../types/schedule'
import { TabsOptionsProps } from '../../../types/tabs'

const ScheduleEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<ScheduleDataProps>(
    `api/schedules/${id}`,
  )

  const tabsPanel = [
    <FormSchedule key={1} mode={'edit'} defaultValues={data} />,
    // <ScheduleTemplatesList key={2} scheduleData={data} />
  ]

  const updatedTabs = scheduleEditTabsOptions.map(
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

export default ScheduleEdit
