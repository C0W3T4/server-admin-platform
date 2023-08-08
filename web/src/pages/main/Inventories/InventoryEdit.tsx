import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormInventory } from '../../../components/forms/inventory/FormInventory'
import { InventoryGroupsList } from '../../../components/views/inventory/InventoryGroupsList'
import { InventorySchedulesList } from '../../../components/views/inventory/InventorySchedulesList'
import { InventoryTeamsList } from '../../../components/views/inventory/InventoryTeamsList'
import { InventoryUsersList } from '../../../components/views/inventory/InventoryUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { inventoryEditTabsOptions } from '../../../providers/InventoryProvider'
import { InventoryDataProps } from '../../../types/inventory'
import { TabsOptionsProps } from '../../../types/tabs'

const InventoryEdit = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<InventoryDataProps>(
    `api/inventories/${id}`,
  )

  const tabsPanel = [
    <FormInventory
      key={1}
      mode={'edit'}
      defaultValues={data}
      setNewData={setData}
    />,
    <InventoryUsersList key={2} inventoryData={data} />,
    <InventoryTeamsList key={3} inventoryData={data} />,
    <InventoryGroupsList key={4} inventoryData={data} />,
    <InventorySchedulesList key={5} inventoryData={data} />,
  ]

  const updatedTabs = inventoryEditTabsOptions.map(
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

export default InventoryEdit
