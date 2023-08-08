import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormProject } from '../../../components/forms/project/FormProject'
import { ProjectSchedulesList } from '../../../components/views/project/ProjectSchedulesList'
import { ProjectTeamsList } from '../../../components/views/project/ProjectTeamsList'
import { ProjectUsersList } from '../../../components/views/project/ProjectUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { projectEditTabsOptions } from '../../../providers/ProjectProvider'
import { ProjectDataProps } from '../../../types/project'
import { TabsOptionsProps } from '../../../types/tabs'

const ProjectEdit = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<ProjectDataProps>(
    `api/projects/${id}`,
  )

  const tabsPanel = [
    <FormProject
      key={1}
      mode={'edit'}
      defaultValues={data}
      setNewData={setData}
    />,
    <ProjectUsersList key={2} projectData={data} />,
    <ProjectTeamsList key={3} projectData={data} />,
    <ProjectSchedulesList key={4} projectData={data} />,
  ]

  const updatedTabs = projectEditTabsOptions.map(
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

export default ProjectEdit
