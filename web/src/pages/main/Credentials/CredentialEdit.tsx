import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormCredential } from '../../../components/forms/credential/FormCredential'
import { CredentialTeamsList } from '../../../components/views/credential/CredentialTeamsList'
import { CredentialUsersList } from '../../../components/views/credential/CredentialUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { credentialEditTabsOptions } from '../../../providers/CredentialProvider'
import { CredentialDataProps } from '../../../types/credential'
import { TabsOptionsProps } from '../../../types/tabs'

const CredentialEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<CredentialDataProps>(
    `api/credentials/${id}`,
  )

  const tabsPanel = [
    <FormCredential key={1} mode={'edit'} defaultValues={data} />,
    <CredentialUsersList key={2} credentialData={data} />,
    <CredentialTeamsList key={3} credentialData={data} />,
  ]

  const updatedTabs = credentialEditTabsOptions.map(
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

export default CredentialEdit
