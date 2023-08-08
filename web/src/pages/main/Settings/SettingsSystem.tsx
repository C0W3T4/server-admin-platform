import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormSystem } from '../../../components/forms/FormSystem'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { settingSystemTabsOptions } from '../../../providers/SettingProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { TowerDataProps } from '../../../types/tower'

const SettingsSystem = () => {
  const { data, setData, isLoading } =
    useAxiosGet<TowerDataProps>(`api/towers/owner`)

  const tabsPanel = [
    <FormSystem
      key={1}
      mode={'edit'}
      defaultValues={data}
      setNewData={setData}
    />,
  ]

  const updatedTabs = settingSystemTabsOptions.map(
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

export default SettingsSystem
