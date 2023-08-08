import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormInventory } from '../../../components/forms/inventory/FormInventory'
import { gridSpacing } from '../../../libs/redux/constants'
import { inventoryCreateTabsOptions } from '../../../providers/InventoryProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const InventoryCreate = () => {
  const tabsPanel = [<FormInventory key={1} mode={'create'} />]

  const updatedTabs = inventoryCreateTabsOptions.map(
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

export default InventoryCreate
