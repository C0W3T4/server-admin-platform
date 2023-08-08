import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { ProjectTabDescription } from '../../../components/views/project/ProjectTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { projectDetailsTabsOptions } from '../../../providers/ProjectProvider'
import { ProjectDataProps } from '../../../types/project'
import { TabsOptionsProps } from '../../../types/tabs'

const ProjectDetails = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<ProjectDataProps>(
    `api/projects/${id}`,
  )

  const tabsPanel = [
    <ProjectTabDescription key={1} defaultValues={data} setNewData={setData} />,
  ]

  const updatedTabs = projectDetailsTabsOptions.map(
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

export default ProjectDetails
