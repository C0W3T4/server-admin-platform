import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormProject } from '../../../components/forms/project/FormProject'
import { gridSpacing } from '../../../libs/redux/constants'
import { projectCreateTabsOptions } from '../../../providers/ProjectProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const ProjectCreate = () => {
  const tabsPanel = [<FormProject key={1} mode={'create'} />]

  const updatedTabs = projectCreateTabsOptions.map(
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

export default ProjectCreate
