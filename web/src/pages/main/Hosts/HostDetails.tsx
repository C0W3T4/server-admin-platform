import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { HostTabDescription } from '../../../components/views/host/HostTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { hostDetailsTabsOptions } from '../../../providers/HostProvider'
import { HostDataProps } from '../../../types/host'
import { TabsOptionsProps } from '../../../types/tabs'

const HostDetails = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<HostDataProps>(
    `api/hosts/${id}`,
  )

  const tabsPanel = [
    <HostTabDescription key={1} defaultValues={data} setNewData={setData} />,
  ]

  const updatedTabs = hostDetailsTabsOptions.map(
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

export default HostDetails
