import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Button,
  Chip,
  Stack,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, Lock as LockIcon, Receipt as ReceiptIcon } from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import PageHeader from '../components/common/PageHeader';
import { payrollApi } from '../api/payroll';
import { payslipsApi } from '../api/payslips';
import { PayrollCycle, PayrollEntry } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const PayrollCycleDetail: React.FC = () => {
  const { cycleId } = useParams<{ cycleId: string }>();
  const navigate = useNavigate();
  const { showSuccess, showError } = useSnackbar();
  const [cycle, setCycle] = useState<PayrollCycle | null>(null);
  const [entries, setEntries] = useState<PayrollEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      if (!cycleId) return;

      try {
        setLoading(true);
        const [cycleData, entriesData] = await Promise.all([
          payrollApi.getCycleById(parseInt(cycleId)),
          payrollApi.getEntries(parseInt(cycleId)),
        ]);
        setCycle(cycleData);
        setEntries(entriesData);
      } catch (error) {
        showError('Failed to load payroll cycle details');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [cycleId, showError]);

  const handleLockCycle = async () => {
    if (!cycleId || !window.confirm('Are you sure you want to lock this payroll cycle? This action cannot be undone.')) {
      return;
    }

    try {
      setProcessing(true);
      await payrollApi.lockCycle(parseInt(cycleId));
      showSuccess('Payroll cycle locked successfully');
      const updatedCycle = await payrollApi.getCycleById(parseInt(cycleId));
      setCycle(updatedCycle);
    } catch (error) {
      showError('Failed to lock payroll cycle');
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  const handleGeneratePayslips = async () => {
    if (!cycleId) return;

    try {
      setProcessing(true);
      const result = await payslipsApi.generateForCycle(parseInt(cycleId));
      showSuccess(`Generated ${result.generated} payslips successfully`);
    } catch (error) {
      showError('Failed to generate payslips');
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!cycle) {
    return <Typography>Payroll cycle not found</Typography>;
  }

  const columns: GridColDef[] = [
    { field: 'employee_code', headerName: 'Employee Code', width: 130 },
    { field: 'employee_name', headerName: 'Employee Name', flex: 1, minWidth: 200 },
    { field: 'days_present', headerName: 'Present', width: 90 },
    { field: 'days_absent', headerName: 'Absent', width: 90 },
    { field: 'paid_leaves_used', headerName: 'Paid Leaves', width: 110 },
    { field: 'comp_leaves_used', headerName: 'Comp Leaves', width: 110 },
    { field: 'unpaid_leaves', headerName: 'Unpaid', width: 90 },
    {
      field: 'loss_of_pay',
      headerName: 'LOP',
      width: 100,
      valueFormatter: (params) => `₹${params.value.toLocaleString()}`,
    },
    {
      field: 'gross_earnings',
      headerName: 'Gross',
      width: 120,
      valueFormatter: (params) => `₹${params.value.toLocaleString()}`,
    },
    {
      field: 'total_deductions',
      headerName: 'Deductions',
      width: 120,
      valueFormatter: (params) => `₹${params.value.toLocaleString()}`,
    },
    {
      field: 'net_pay',
      headerName: 'Net Pay',
      width: 120,
      valueFormatter: (params) => `₹${params.value.toLocaleString()}`,
    },
  ];

  return (
    <Box>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/payroll')} sx={{ mb: 2 }}>
        Back to Payroll
      </Button>

      <PageHeader
        title={`Payroll Cycle - ${new Date(0, cycle.month - 1).toLocaleString('default', {
          month: 'long',
        })} ${cycle.year}`}
        subtitle={`Status: ${cycle.status}`}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Chip label={cycle.status} color="primary" />
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="subtitle2" color="text.secondary">
                College
              </Typography>
              <Typography variant="body1">{cycle.college_name || `College ID: ${cycle.college_id}`}</Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="subtitle2" color="text.secondary">
                Total Working Days
              </Typography>
              <Typography variant="h5">{cycle.total_working_days}</Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="subtitle2" color="text.secondary">
                Created At
              </Typography>
              <Typography variant="body1">{format(new Date(cycle.created_at), 'dd MMM yyyy')}</Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="subtitle2" color="text.secondary">
                Updated At
              </Typography>
              <Typography variant="body1">{format(new Date(cycle.updated_at), 'dd MMM yyyy')}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <Button
          variant="contained"
          startIcon={<ReceiptIcon />}
          onClick={handleGeneratePayslips}
          disabled={processing || cycle.status === 'LOCKED'}
        >
          Generate Payslips
        </Button>
        <Button
          variant="outlined"
          startIcon={<LockIcon />}
          onClick={handleLockCycle}
          disabled={processing || cycle.status === 'LOCKED'}
        >
          Lock Cycle
        </Button>
      </Stack>

      <Typography variant="h6" gutterBottom>
        Payroll Entries
      </Typography>
      <Box sx={{ height: 500, width: '100%' }}>
        <DataGrid
          rows={entries}
          columns={columns}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  );
};

export default PayrollCycleDetail;
