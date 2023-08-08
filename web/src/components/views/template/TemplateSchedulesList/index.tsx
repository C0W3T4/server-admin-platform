import { DateRangeTwoTone, Delete, Search } from '@mui/icons-material'
import {
  Box,
  CardContent,
  Checkbox,
  Grid,
  IconButton,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
  Zoom,
  useTheme,
} from '@mui/material'
import { visuallyHidden } from '@mui/utils'
import { AxiosError, AxiosResponse } from 'axios'
import React, { ChangeEvent, SyntheticEvent, useEffect, useState } from 'react'
import { TbCirclePlus } from 'react-icons/tb'
import { FormattedMessage, useIntl } from 'react-intl'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useAxiosGet } from '../../../../hooks/useAxiosGet'
import useConfig from '../../../../hooks/useConfig'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { scheduleTypeMap } from '../../../../providers/ScheduleProvider'
import { templateSchedulesListTableHeadCells } from '../../../../providers/TemplateProvider'
import { ArrangementOrder, KeyedObject } from '../../../../types'
import { JobsScheduleInfoDataProps } from '../../../../types/schedule'
import {
  TemplateDataProps,
  TemplateSchedulesDataProps,
} from '../../../../types/template'
import { getComparator } from '../../../../utils/table/getComparator'
import { stableSort } from '../../../../utils/table/stableSort'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import { MainCard } from '../../../cards/MainCard'
import { FormTemplateSchedules } from '../../../forms/template/FormTemplateSchedules'

const iconSX = {
  width: 16,
  height: 16,
  verticalAlign: 'middle',
  mr: 0.5,
}

interface TemplateSchedulesListProps {
  templateData: TemplateDataProps | null
}

export const TemplateSchedulesList = ({
  templateData,
}: TemplateSchedulesListProps) => {
  const theme = useTheme()
  const { locale } = useConfig()
  const { formatMessage } = useIntl()
  const { id } = useParams()
  const navigate = useNavigate()

  const { showLoading, hideLoading } = useLoading()
  const [order, setOrder] = useState<ArrangementOrder>('asc')
  const [orderBy, setOrderBy] = useState<string>('template_schedule_id')
  const [selected, setSelected] = useState<string[]>([])
  const [page, setPage] = useState<number>(0)
  const [rowsPerPage, setRowsPerPage] = useState<number>(5)
  const [search, setSearch] = useState<string>('')
  const [rows, setRows] = useState<TemplateSchedulesDataProps[]>([])
  const [openDialog, setOpenDialog] = useState<boolean>(false)
  const [scheduleInfoData, setScheduleInfoData] = useState<
    JobsScheduleInfoDataProps[]
  >([])

  const { data, setData } = useAxiosGet<TemplateSchedulesDataProps[]>(
    `api/assigns/templates-schedules/${id}/schedules`,
  )

  const handleClickOpenDialog = () => setOpenDialog(true)
  const handleCloseDialog = () => setOpenDialog(false)

  const handleSearch = (
    event?: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>,
  ) => {
    const newString = event?.target.value
    setSearch(newString || '')

    if (newString) {
      const newRows = rows.filter((row: KeyedObject) => {
        let matches = true

        const properties = [
          'template_schedule_id',
          'name',
          'schedule_type',
          'next_date',
        ]
        let containsQuery = false

        properties.forEach((property) => {
          if (property === 'template_schedule_id' || property === 'next_date') {
            if (
              row[property]
                .toString()
                .toLowerCase()
                .includes(newString.toString().toLowerCase())
            ) {
              containsQuery = true
            }
          } else {
            if (
              row.schedule[property]
                .toString()
                .toLowerCase()
                .includes(newString.toString().toLowerCase())
            ) {
              containsQuery = true
            }
          }
        })

        if (!containsQuery) {
          matches = false
        }
        return matches
      })
      setRows(newRows)
    } else {
      setRows(data || [])
    }
  }

  const handleRequestSort = (
    _event: SyntheticEvent<Element, Event>,
    property: string,
  ) => {
    const isAsc = orderBy === property && order === 'asc'
    setOrder(isAsc ? 'desc' : 'asc')
    setOrderBy(property)
  }

  const handleSelectAllClick = (event?: ChangeEvent<HTMLInputElement>) => {
    if (event?.target.checked) {
      const newSelectedId = rows.map((row) => row.template_schedule_id)
      setSelected(newSelectedId)
      return
    }
    setSelected([])
  }

  const handleClick = (
    _event: React.MouseEvent<HTMLTableHeaderCellElement, MouseEvent>,
    name: string,
  ) => {
    const selectedIndex = selected.indexOf(name)
    let newSelected: string[] = []

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, name)
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1))
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1))
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1),
      )
    }

    setSelected(newSelected)
  }

  const handleChangePage = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent> | null,
    newPage: number,
  ) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (
    event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement> | undefined,
  ) => {
    event?.target.value && setRowsPerPage(parseInt(event?.target.value, 10))
    setPage(0)
  }

  const isSelected = (name: string) => selected.indexOf(name) !== -1
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0

  const deleteSchedule = async (selected: string[]) => {
    showLoading()
    await api
      .delete('api/assigns/templates-schedules', { data: selected })
      .then((response) => {
        if (response.status === 204) {
          setData(
            data!.filter(
              (templateSchedule) =>
                !selected.includes(templateSchedule.template_schedule_id),
            ),
          )
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.204" />,
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'success',
              },
              close: true,
            }),
          )
        }
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
      .finally(() => hideLoading())
  }

  const handleDelete = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    selected: string[],
  ) => deleteSchedule(selected)

  const getScheduleInfo = async () => {
    await api
      .get(`api/assigns/templates-schedules/${id}/schedules/info`)
      .then((response: AxiosResponse<JobsScheduleInfoDataProps[], unknown>) =>
        setScheduleInfoData(response.data),
      )
      .catch((error: AxiosError) => {
        setTimeout(() => {
          if (error.response?.status === 401) {
            navigate('/unauthorized', { replace: true })
          }
          if (error.response?.status === 403) {
            navigate('/forbidden', { replace: true })
          }
          if (error.response?.status === 422) {
            navigate('/not-found', { replace: true })
          }
          if (error.response?.status === 404) {
            dispatch(
              openSnackbar({
                open: true,
                message: formatMessage({ id: 'snackbar.message.error.noData' }),
                transition: 'SlideUp',
                variant: 'alert',
                alert: {
                  color: 'error',
                },
                close: true,
              }),
            )
          }
        }, 1)
      })
  }

  const handleGetScheduleInfo = () => getScheduleInfo()

  useEffect(() => {
    setRows(data || [])
    handleSelectAllClick()
    handleGetScheduleInfo()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data])

  return (
    <MainCard
      title={`${templateData!.name} -> ${formatMessage({
        id: 'templates.labels.schedules',
      })}`}
      content={false}
      secondary={<CardHeaderActions />}
    >
      <CardContent>
        <Grid
          container
          justifyContent="space-between"
          alignItems="center"
          spacing={2}
        >
          <Grid item xs={12} sm={6}>
            <TextField
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search color="info" fontSize="small" />
                  </InputAdornment>
                ),
              }}
              onChange={handleSearch}
              placeholder={formatMessage({
                id: 'templates.placeholders.searchSchedules',
              })}
              value={search}
              size="small"
            />
          </Grid>
          <Grid item xs={12} sm={6} sx={{ textAlign: 'right' }}>
            <Tooltip
              TransitionComponent={Zoom}
              title={<FormattedMessage id="tooltips.add" />}
            >
              <Link to="#" onClick={handleClickOpenDialog}>
                <IconButton size="large" color="secondary">
                  <TbCirclePlus />
                </IconButton>
              </Link>
            </Tooltip>
            <FormTemplateSchedules
              open={openDialog}
              handleCloseDialog={handleCloseDialog}
              data={templateData}
              setNewData={setData}
              oldData={data}
            />
          </Grid>
        </Grid>
      </CardContent>

      {/* table */}
      <TableContainer>
        <Table sx={{ minWidth: 750 }} aria-labelledby="tableTitle">
          {/* table header */}
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox" sx={{ pl: 3 }}>
                <Checkbox
                  color="primary"
                  indeterminate={
                    selected.length > 0 && selected.length < rows.length
                  }
                  checked={rows.length > 0 && selected.length === rows.length}
                  onChange={handleSelectAllClick}
                  inputProps={{
                    'aria-label': 'select all desserts',
                  }}
                />
              </TableCell>
              {selected.length > 0 && (
                <TableCell padding="none" colSpan={8}>
                  {/* table toolbar */}
                  <Toolbar
                    sx={{
                      p: 0,
                      pl: 1,
                      pr: 1,
                      ...(selected.length > 0 && {
                        color: (theme) => theme.palette.secondary.main,
                      }),
                    }}
                  >
                    {selected.length > 0 && (
                      <Typography color="inherit" variant="h4">
                        {selected.length}{' '}
                        <FormattedMessage id="table.labels.selected" />
                      </Typography>
                    )}
                    <Box sx={{ flexGrow: 1 }} />
                    {selected.length > 0 && (
                      <Tooltip
                        TransitionComponent={Zoom}
                        title={<FormattedMessage id="tooltips.delete" />}
                      >
                        <IconButton
                          size="large"
                          onClick={(event) => handleDelete(event, selected)}
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Toolbar>
                </TableCell>
              )}
              {selected.length <= 0 &&
                templateSchedulesListTableHeadCells.map((headCell) => (
                  <TableCell
                    key={headCell.id}
                    align={headCell.align}
                    padding={headCell.disablePadding ? 'none' : 'normal'}
                    sortDirection={orderBy === headCell.id ? order : false}
                  >
                    <TableSortLabel
                      active={orderBy === headCell.id}
                      direction={orderBy === headCell.id ? order : 'asc'}
                      onClick={(event) => handleRequestSort(event, headCell.id)}
                    >
                      <FormattedMessage id={headCell.label} />
                      {orderBy === headCell.id ? (
                        <Box component="span" sx={visuallyHidden}>
                          {order === 'desc'
                            ? 'sorted descending'
                            : 'sorted ascending'}
                        </Box>
                      ) : null}
                    </TableSortLabel>
                  </TableCell>
                ))}
            </TableRow>
          </TableHead>

          {/* table body */}
          <TableBody>
            {stableSort<TemplateSchedulesDataProps>(
              rows,
              getComparator(order, orderBy),
            )
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, index) => {
                /** Make sure no display bugs if row isn't an OrderData object */
                if (typeof row === 'number') return null

                const isItemSelected = isSelected(row.template_schedule_id)
                const labelId = `enhanced-table-checkbox-${index}`

                return (
                  <TableRow
                    hover
                    role="checkbox"
                    aria-checked={isItemSelected}
                    tabIndex={-1}
                    key={index}
                    selected={isItemSelected}
                  >
                    <TableCell
                      padding="checkbox"
                      sx={{ pl: 3 }}
                      onClick={(event) =>
                        handleClick(event, row.template_schedule_id)
                      }
                    >
                      <Checkbox
                        color="primary"
                        checked={isItemSelected}
                        inputProps={{
                          'aria-labelledby': labelId,
                        }}
                      />
                    </TableCell>
                    <TableCell
                      component="th"
                      id={labelId}
                      scope="row"
                      onClick={(event) =>
                        handleClick(event, row.template_schedule_id)
                      }
                      sx={{ cursor: 'pointer' }}
                    >
                      <Typography
                        variant="subtitle1"
                        sx={{
                          color:
                            theme.palette.mode === 'dark'
                              ? 'grey.600'
                              : 'grey.900',
                        }}
                      >
                        #{row.template_schedule_id}
                      </Typography>
                    </TableCell>
                    <TableCell align="left">{row.schedule.name}</TableCell>
                    <TableCell align="left">
                      {scheduleTypeMap.get(row.schedule.schedule_type)?.icon}
                      <FormattedMessage
                        id={
                          scheduleTypeMap.get(row.schedule.schedule_type)?.label
                        }
                      />
                    </TableCell>
                    <TableCell align="left">
                      {scheduleInfoData &&
                        scheduleInfoData.find(
                          (info) => info.cron_job_id === row.cron_job_id,
                        )?.next_date && (
                          <>
                            <DateRangeTwoTone sx={iconSX} color="info" />
                            {new Intl.DateTimeFormat(locale, {
                              dateStyle: 'short',
                              timeStyle: 'medium',
                            }).format(
                              new Date(
                                scheduleInfoData.find(
                                  (info) =>
                                    info.cron_job_id === row.cron_job_id,
                                )!.next_date,
                              ),
                            )}
                          </>
                        )}
                      {!scheduleInfoData && '-----'}
                    </TableCell>
                  </TableRow>
                )
              })}
            {(emptyRows > 0 || !data || data.length < 1) && (
              <TableRow hover>
                <TableCell colSpan={12} align="center">
                  <FormattedMessage id="errors.noData" />
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* table pagination */}
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </MainCard>
  )
}
