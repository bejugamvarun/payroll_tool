import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Download as DownloadIcon, Assessment as ReportIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { reportsApi } from '../api/reports';
import { collegesApi } from '../api/colleges';
import { Report, ReportGenerateRequest, College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const Reports: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [reports, setReports] = useState<Report[]>([]);
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [formData, setFormData] = useState<ReportGenerateRequest>({
    report_type: 'PAYROLL_SUMMARY',
    month: new Date().getMonth() + 1,
    year: new Date().getFullYear(),
  });

  const fetchReports = async () => {
    try {
      setLoading(true);
      const data = await reportsApi.getAll();
      setReports(data);
    } catch (error) {
      showError('Failed to load reports');
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
      } catch (error) {
        console.error(error);
      }
    };
    fetchColleges();
    fetchReports();
  }, []);

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      await reportsApi.generate(formData);
      showSuccess('Report generated successfully');
      fetchReports();
    } catch (error) {
      showError('Failed to generate report');
      console.error(error);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (reportId: number, reportType: string) => {
    try {
      const blob = await reportsApi.download(reportId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${reportType}_${reportId}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showSuccess('Report downloaded successfully');
    } catch (error) {
      showError('Failed to download report');
      console.error(error);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'report_type', headerName: 'Report Type', flex: 1, minWidth: 200 },
    {
      field: 'month',
      headerName: 'Period',
      width: 150,
      valueGetter: (params) =>
        params.row.month && params.row.year
          ? `${new Date(0, params.row.month - 1).toLocaleString('default', { month: 'long' })} ${
              params.row.year
            }`
          : 'N/A',
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
          onClick={() => handleDownload(params.id as number, params.row.report_type)}
        >
          Download
        </Button>
      ),
    },
  ];

  return (
    <Box>
      <PageHeader title="Reports" subtitle="Generate and download payroll reports" />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Generate New Report
          </Typography>
          <Stack spacing={2} sx={{ mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={formData.report_type}
                label="Report Type"
                onChange={(e) => setFormData({ ...formData, report_type: e.target.value })}
              >
                <MenuItem value="PAYROLL_SUMMARY">Payroll Summary</MenuItem>
                <MenuItem value="EMPLOYEE_MASTER">Employee Master List</MenuItem>
                <MenuItem value="SALARY_REGISTER">Salary Register</MenuItem>
                <MenuItem value="ATTENDANCE_SUMMARY">Attendance Summary</MenuItem>
                <MenuItem value="LEAVE_BALANCE">Leave Balance Report</MenuItem>
                <MenuItem value="TAX_DEDUCTION">Tax Deduction Report</MenuItem>
              </Select>
            </FormControl>

            <Stack direction="row" spacing={2}>
              <FormControl sx={{ flex: 1 }}>
                <InputLabel>College (Optional)</InputLabel>
                <Select
                  value={formData.college_id || ''}
                  label="College (Optional)"
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      college_id: e.target.value ? (e.target.value as number) : undefined,
                    })
                  }
                >
                  <MenuItem value="">All Colleges</MenuItem>
                  {colleges.map((college) => (
                    <MenuItem key={college.id} value={college.id}>
                      {college.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl sx={{ flex: 1 }}>
                <InputLabel>Month</InputLabel>
                <Select
                  value={formData.month}
                  label="Month"
                  onChange={(e) => setFormData({ ...formData, month: e.target.value as number })}
                >
                  {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                    <MenuItem key={m} value={m}>
                      {new Date(2000, m - 1).toLocaleString('default', { month: 'long' })}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl sx={{ flex: 1 }}>
                <InputLabel>Year</InputLabel>
                <Select
                  value={formData.year}
                  label="Year"
                  onChange={(e) => setFormData({ ...formData, year: e.target.value as number })}
                >
                  {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map((y) => (
                    <MenuItem key={y} value={y}>
                      {y}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Stack>

            <Button
              variant="contained"
              startIcon={<ReportIcon />}
              onClick={handleGenerate}
              disabled={generating}
              size="large"
            >
              {generating ? 'Generating...' : 'Generate Report'}
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Typography variant="h6" gutterBottom>
        Report History
      </Typography>
      <Box sx={{ height: 500, width: '100%' }}>
        <DataGrid
          rows={reports}
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

export default Reports;
