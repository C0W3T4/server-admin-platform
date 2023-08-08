import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { CredentialTabDescription } from '../../../components/views/credential/CredentialTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { credentialDetailsTabsOptions } from '../../../providers/CredentialProvider'
import { CredentialDataProps } from '../../../types/credential'
import { TabsOptionsProps } from '../../../types/tabs'

const CredentialDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<CredentialDataProps>(
    `api/credentials/${id}`,
  )

  const tabsPanel = [<CredentialTabDescription key={1} defaultValues={data} />]

  const updatedTabs = credentialDetailsTabsOptions.map(
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

export default CredentialDetails
