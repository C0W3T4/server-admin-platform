import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormTemplate } from '../../../components/forms/template/FormTemplate'
import { TemplateSchedulesList } from '../../../components/views/template/TemplateSchedulesList'
import { TemplateTeamsList } from '../../../components/views/template/TemplateTeamsList'
import { TemplateUsersList } from '../../../components/views/template/TemplateUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { templateEditTabsOptions } from '../../../providers/TemplateProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { TemplateDataProps } from '../../../types/template'

const TemplateEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<TemplateDataProps>(
    `api/templates/${id}`,
  )

  const tabsPanel = [
    <FormTemplate key={1} mode={'edit'} defaultValues={data} />,
    <TemplateUsersList key={2} templateData={data} />,
    <TemplateTeamsList key={3} templateData={data} />,
    <TemplateSchedulesList key={4} templateData={data} />,
  ]

  const updatedTabs = templateEditTabsOptions.map(
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

export default TemplateEdit
