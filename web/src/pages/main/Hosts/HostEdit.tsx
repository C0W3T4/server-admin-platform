import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormHost } from '../../../components/forms/host/FormHost'
import { HostTeamsList } from '../../../components/views/host/HostTeamsList'
import { HostUsersList } from '../../../components/views/host/HostUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { hostEditTabsOptions } from '../../../providers/HostProvider'
import { HostDataProps } from '../../../types/host'
import { TabsOptionsProps } from '../../../types/tabs'

const HostEdit = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<HostDataProps>(
    `api/hosts/${id}`,
  )

  const tabsPanel = [
    <FormHost
      key={1}
      mode={'edit'}
      defaultValues={data}
      setNewData={setData}
    />,
    <HostUsersList key={2} hostData={data} />,
    <HostTeamsList key={3} hostData={data} />,
  ]

  const updatedTabs = hostEditTabsOptions.map(
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

export default HostEdit
