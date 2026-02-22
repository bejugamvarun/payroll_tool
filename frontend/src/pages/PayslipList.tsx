import React, { useEffect, useState } from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Button,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Download as DownloadIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { payrollApi } from '../api/payroll';
import { payslipsApi } from '../api/payslips';
import { Payslip, PayrollCycle } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const PayslipList: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [payslips, setPayslips] = useState<Payslip[]>([]);
  const [cycles, setCycles] = useState<PayrollCycle[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCycle, setSelectedCycle] = useState<number | ''>('');

  const fetchCycles = async () => {
    try {
      const data = await payrollApi.getCycles();
      setCycles(data);
    } catch (error) {
      showError('Failed to load payroll cycles');
      console.error(error);
    }
  };

  const fetchPayslips = async () => {
    if (!selectedCycle) {
      setPayslips([]);
      return;
    }

    try {
      setLoading(true);
      const data = await payslipsApi.getForCycle(selectedCycle as number);
      setPayslips(data);
    } catch (error) {
      showError('Failed to load payslips');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCycles();
  }, []);

  useEffect(() => {
    fetchPayslips();
  }, [selectedCycle]);

  const handleDownloadSingle = async (payslipId: number) => {
    try {
      const blob = await payslipsApi.downloadSingle(payslipId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `payslip_${payslipId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showSuccess('Payslip downloaded successfully');
    } catch (error) {
      showError('Failed to download payslip');
      console.error(error);
    }
  };

  const handleDownloadBulk = async () => {
    if (!selectedCycle) return;

    try {
      const blob = await payslipsApi.downloadBulk(selectedCycle as number);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `payslips_cycle_${selectedCycle}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showSuccess('Payslips downloaded successfully');
    } catch (error) {
      showError('Failed to download payslips');
      console.error(error);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    {
      field: 'employee_name',
      headerName: 'Employee',
      flex: 1,
      minWidth: 200,
    },
    {
      field: 'employee_code',
      headerName: 'Code',
      width: 120,
    },
    {
      field: 'generated_at',
      headerName: 'Generated Date',
      width: 180,
      valueFormatter: (params) => format(new Date(params.value), 'dd MMM yyyy HH:mm'),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      renderCell: (params) => (
        <Button
          size="small"
          startIcon={<DownloadIcon />}
          onClick={() => handleDownloadSingle(params.id as number)}
        >
          Download
        </Button>
      ),
    },
  ];

  return (
    <Box>
      <PageHeader title="Payslips" subtitle="View and download employee payslips" />

      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <FormControl sx={{ minWidth: 300 }}>
          <InputLabel>Select Payroll Cycle</InputLabel>
          <Select
            value={selectedCycle}
            label="Select Payroll Cycle"
            onChange={(e) => setSelectedCycle(e.target.value as number | '')}
          >
            <MenuItem value="">Select a cycle</MenuItem>
            {cycles.map((cycle) => (
              <MenuItem key={cycle.id} value={cycle.id}>
                {new Date(0, cycle.month - 1).toLocaleString('default', { month: 'long' })}{' '}
                {cycle.year} - {cycle.status}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          variant="contained"
          startIcon={<DownloadIcon />}
          onClick={handleDownloadBulk}
          disabled={!selectedCycle || payslips.length === 0}
        >
          Download All (ZIP)
        </Button>
      </Stack>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={payslips}
          columns={columns}
          loading={loading}
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

export default PayslipList;
