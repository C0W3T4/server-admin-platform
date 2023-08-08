import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { JobTabDescription } from '../../../components/views/job/JobTabDescription'
import { JobTabOutput } from '../../../components/views/job/JobTabOutput'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { jobDetailsTabsOptions } from '../../../providers/JobProvider'
import { JobDataProps } from '../../../types/job'
import { TabsOptionsProps } from '../../../types/tabs'

const JobDetails = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<JobDataProps>(
    `api/jobs/${id}`,
  )

  const tabsPanel = [
    <JobTabDescription key={1} defaultValues={data} setNewData={setData} />,
    <JobTabOutput key={2} defaultValues={data} setNewData={setData} />,
  ]

  const updatedTabs = jobDetailsTabsOptions.map(
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

export default JobDetails
