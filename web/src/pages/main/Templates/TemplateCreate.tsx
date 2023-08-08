import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormTemplate } from '../../../components/forms/template/FormTemplate'
import { gridSpacing } from '../../../libs/redux/constants'
import { templateCreateTabsOptions } from '../../../providers/TemplateProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const TemplateCreate = () => {
  const tabsPanel = [<FormTemplate key={1} mode={'create'} />]

  const updatedTabs = templateCreateTabsOptions.map(
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

export default TemplateCreate
