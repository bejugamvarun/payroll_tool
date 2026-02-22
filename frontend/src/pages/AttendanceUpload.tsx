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
  Alert,
  LinearProgress,
  Stack,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { attendanceApi } from '../api/attendance';
import { collegesApi } from '../api/colleges';
import { College, AttendanceUpload } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const AttendanceUploadPage: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [colleges, setColleges] = useState<College[]>([]);
  const [uploads, setUploads] = useState<AttendanceUpload[]>([]);
  const [selectedCollege, setSelectedCollege] = useState<number>(0);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const fetchUploads = async () => {
    try {
      const data = await attendanceApi.getUploads();
      setUploads(data);
    } catch (error) {
      showError('Failed to load upload history');
      console.error(error);
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
    fetchUploads();
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file || !selectedCollege) {
      showError('Please select all required fields');
      return;
    }

    try {
      setUploading(true);
      await attendanceApi.upload(file, selectedCollege, month, year);
      showSuccess('Attendance uploaded successfully');
      setFile(null);
      fetchUploads();
    } catch (error) {
      showError('Failed to upload attendance');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'file_name', headerName: 'File Name', flex: 1, minWidth: 200 },
    {
      field: 'month',
      headerName: 'Month',
      width: 100,
      valueFormatter: (params) => `${params.value}/${uploads.find(u => u.id === params.id)?.year}`,
    },
    { field: 'records_count', headerName: 'Records', width: 100 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
    },
    {
      field: 'uploaded_at',
      headerName: 'Upload Date',
      width: 180,
      valueFormatter: (params) => format(new Date(params.value), 'dd MMM yyyy HH:mm'),
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Attendance Upload"
        subtitle="Upload monthly attendance data"
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Alert severity="info" sx={{ mb: 3 }}>
            Upload an Excel file with employee attendance data. Required columns: employee_code, date, status.
            Status values: PRESENT, ABSENT, HALF_DAY, WEEKEND_WORK, HOLIDAY, LEAVE.
          </Alert>

          <Stack spacing={2}>
            <Stack direction="row" spacing={2}>
              <FormControl sx={{ minWidth: 200 }}>
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

              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel>Month</InputLabel>
                <Select
                  value={month}
                  label="Month"
                  onChange={(e) => setMonth(e.target.value as number)}
                >
                  {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                    <MenuItem key={m} value={m}>
                      {new Date(2000, m - 1).toLocaleString('default', { month: 'long' })}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel>Year</InputLabel>
                <Select
                  value={year}
                  label="Year"
                  onChange={(e) => setYear(e.target.value as number)}
                >
                  {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map((y) => (
                    <MenuItem key={y} value={y}>
                      {y}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Stack>

            <Box>
              <input
                accept=".xlsx,.xls"
                style={{ display: 'none' }}
                id="attendance-file-upload"
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="attendance-file-upload">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<UploadIcon />}
                  fullWidth
                  sx={{ py: 2 }}
                >
                  {file ? file.name : 'Choose Excel File'}
                </Button>
              </label>
            </Box>

            {uploading && (
              <Box>
                <Typography variant="body2" gutterBottom>
                  Uploading...
                </Typography>
                <LinearProgress />
              </Box>
            )}

            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!file || !selectedCollege || uploading}
              size="large"
            >
              Upload Attendance
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Typography variant="h6" gutterBottom>
        Upload History
      </Typography>
      <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={uploads}
          columns={columns}
          pageSizeOptions={[10, 25]}
          initialState={{
            pagination: { paginationModel: { pageSize: 10 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  );
};

export default AttendanceUploadPage;
