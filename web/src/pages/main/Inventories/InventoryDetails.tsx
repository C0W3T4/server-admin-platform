import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { InventoryTabDescription } from '../../../components/views/inventory/InventoryTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { inventoryDetailsTabsOptions } from '../../../providers/InventoryProvider'
import { InventoryDataProps } from '../../../types/inventory'
import { TabsOptionsProps } from '../../../types/tabs'

const InventoryDetails = () => {
  const { id } = useParams()

  const { data, setData, isLoading } = useAxiosGet<InventoryDataProps>(
    `api/inventories/${id}`,
  )

  const tabsPanel = [
    <InventoryTabDescription
      key={1}
      defaultValues={data}
      setNewData={setData}
    />,
  ]

  const updatedTabs = inventoryDetailsTabsOptions.map(
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

export default InventoryDetails
