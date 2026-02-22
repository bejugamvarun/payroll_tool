import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Chip,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Calculate as CalculateIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { payrollApi } from '../api/payroll';
import { collegesApi } from '../api/colleges';
import { PayrollCycle, College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const PayrollDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useSnackbar();
  const [cycles, setCycles] = useState<PayrollCycle[]>([]);
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [selectedCollege, setSelectedCollege] = useState<number>(0);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());

  const fetchCycles = async () => {
    try {
      setLoading(true);
      const data = await payrollApi.getCycles();
      setCycles(data);
    } catch (error) {
      showError('Failed to load payroll cycles');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchColleges = async () => {
      try {
        const data = await collegesApi.getAll();
        setColleges(data);
        if (data.length > 0) {
          setSelectedCollege(data[0].id);
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchColleges();
    fetchCycles();
  }, []);

  const handleCalculate = async () => {
    if (!selectedCollege) {
      showError('Please select a college');
      return;
    }

    try {
      setCalculating(true);
      await payrollApi.calculate(selectedCollege, month, year);
      showSuccess('Payroll calculated successfully');
      setDialogOpen(false);
      fetchCycles();
    } catch (error) {
      showError('Failed to calculate payroll');
      console.error(error);
    } finally {
      setCalculating(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'DRAFT':
        return 'default';
      case 'PROCESSING':
        return 'warning';
      case 'COMPLETED':
        return 'success';
      case 'LOCKED':
        return 'error';
      default:
        return 'default';
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    {
      field: 'month',
      headerName: 'Period',
      width: 150,
      valueGetter: (params) =>
        `${new Date(0, params.row.month - 1).toLocaleString('default', { month: 'long' })} ${
          params.row.year
        }`,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} color={getStatusColor(params.value)} size="small" />
      ),
    },
    { field: 'total_working_days', headerName: 'Working Days', width: 130 },
    {
      field: 'created_at',
      headerName: 'Created',
      width: 150,
      valueFormatter: (params) => format(new Date(params.value), 'dd MMM yyyy'),
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Payroll Management"
        subtitle="Manage payroll cycles and calculations"
        action={{
          label: 'Calculate Payroll',
          onClick: () => setDialogOpen(true),
          icon: <CalculateIcon />,
        }}
      />

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={cycles}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
          onRowClick={(params) => navigate(`/payroll/${params.id}`)}
          sx={{ cursor: 'pointer' }}
        />
      </Box>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Calculate Payroll</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 2 }}>
            <FormControl fullWidth required>
              <InputLabel>College</InputLabel>
              <Select
                value={selectedCollege}
                label="College"
                onChange={(e) => setSelectedCollege(e.target.value as number)}
              >
                {colleges.map((college) => (
                  <MenuItem key={college.id} value={college.id}>
                    {college.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth required>
              <InputLabel>Month</InputLabel>
              <Select value={month} label="Month" onChange={(e) => setMonth(e.target.value as number)}>
                {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                  <MenuItem key={m} value={m}>
                    {new Date(2000, m - 1).toLocaleString('default', { month: 'long' })}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth required>
              <InputLabel>Year</InputLabel>
              <Select value={year} label="Year" onChange={(e) => setYear(e.target.value as number)}>
                {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map((y) => (
                  <MenuItem key={y} value={y}>
                    {y}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCalculate} variant="contained" disabled={calculating}>
            {calculating ? 'Calculating...' : 'Calculate'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PayrollDashboard;
