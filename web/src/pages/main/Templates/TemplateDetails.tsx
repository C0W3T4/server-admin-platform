import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { TemplateTabDescription } from '../../../components/views/template/TemplateTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { templateDetailsTabsOptions } from '../../../providers/TemplateProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { TemplateDataProps } from '../../../types/template'

const TemplateDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<TemplateDataProps>(
    `api/templates/${id}`,
  )

  const tabsPanel = [<TemplateTabDescription key={1} defaultValues={data} />]

  const updatedTabs = templateDetailsTabsOptions.map(
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

export default TemplateDetails
