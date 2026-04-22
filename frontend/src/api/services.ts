import apiClient from './client';
import { ENDPOINTS } from '../config/api';
import { 
  Attendance, 
  CreateAttendanceDto, 
  UpdateAttendanceDto,
  AttendanceStats,
  Payment,
  CreatePaymentDto,
  UpdatePaymentDto,
  ProfitReport,
  Month,
  PaymentType,
  Reception,
  CreateReceptionDto,
  UpdateReceptionDto,
  MonthlyStats,
  Expense,
  CreateExpenseDto,
  UpdateExpenseDto,
  StudentInfo
} from '../types';

export const attendanceService = {
  getAttendanceStats: async (studentId?: number): Promise<AttendanceStats> => {
    const params = studentId ? { student_id: studentId } : {};
    return apiClient.get(ENDPOINTS.GET_ATTENDANCE_STATS, { params });
  },

  getAttendanceForAdmins: async (
    attendanceDate?: string,
    teacherId?: number,
    groupId?: number,
    studentId?: number
  ): Promise<Attendance[]> => {
    const params: Record<string, any> = {};
    if (attendanceDate) params.attendance_date = attendanceDate;
    if (teacherId) params.teacher_id = teacherId;
    if (groupId) params.group_id = groupId;
    if (studentId) params.student_id = studentId;
    return apiClient.get(ENDPOINTS.GET_ATTENDANCE_ADMINS, { params });
  },

  getAttendanceForTeachers: async (
    attendanceDate?: string,
    groupId?: number,
    studentId?: number
  ): Promise<Attendance[]> => {
    const params: Record<string, any> = {};
    if (attendanceDate) params.attendance_date = attendanceDate;
    if (groupId) params.group_id = groupId;
    if (studentId) params.student_id = studentId;
    return apiClient.get(ENDPOINTS.GET_ATTENDANCE_TEACHERS, { params });
  },

  createAttendance: async (data: CreateAttendanceDto): Promise<Attendance> => {
    return apiClient.post(ENDPOINTS.CREATE_ATTENDANCE, data);
  },

  updateAttendance: async (id: number, data: UpdateAttendanceDto): Promise<Attendance> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_ATTENDANCE}?attendance_id=${id}`, data);
  },

  deleteAttendance: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_ATTENDANCE}?attendance_id=${id}`);
  },
};

export const paymentService = {
  getProfit: async (year?: number, month?: number): Promise<ProfitReport> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_PROFIT, { params });
  },

  getAllPayments: async (courseId?: number): Promise<Payment[]> => {
    const params = courseId ? { course_id: courseId } : {};
    return apiClient.get(ENDPOINTS.GET_ALL_PAYMENTS, { params });
  },

  getMonthlySum: async (year?: number, month?: number): Promise<{ total: number }> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_MONTHLY_SUM, { params });
  },

  getTeacherPayments: async (): Promise<Payment[]> => {
    return apiClient.get(ENDPOINTS.GET_TEACHER_PAYMENTS);
  },

  createPayment: async (data: CreatePaymentDto): Promise<Payment> => {
    return apiClient.post(ENDPOINTS.CREATE_PAYMENT, data);
  },

  updatePayment: async (id: number, data: UpdatePaymentDto): Promise<Payment> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_PAYMENT}?ident=${id}`, data);
  },

  deletePayment: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_PAYMENT}?ident=${id}`);
  },
};

export const receptionService = {
  getReception: async (year?: number, month?: number): Promise<Reception[]> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_RECEPTION, { params });
  },

  getReceptionStatistics: async (statDate?: string): Promise<any> => {
    const params = statDate ? { stat_date: statDate } : {};
    return apiClient.get(ENDPOINTS.GET_RECEPTION_STATS, { params });
  },

  getMonthlyStatistics: async (year?: number, month?: number): Promise<MonthlyStats> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_MONTHLY_STATS, { params });
  },

  getTotalReception: async (year?: number, month?: number): Promise<{ total: number }> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_TOTAL_RECEPTION, { params });
  },

  createReception: async (data: CreateReceptionDto): Promise<Reception> => {
    return apiClient.post(ENDPOINTS.CREATE_RECEPTION, data);
  },

  updateReception: async (data: UpdateReceptionDto): Promise<Reception> => {
    return apiClient.put(ENDPOINTS.UPDATE_RECEPTION, data);
  },

  deleteReception: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_RECEPTION}?ident=${id}`);
  },
};

export const expenseService = {
  getExpenses: async (
    startDate?: string,
    endDate?: string,
    expenseType?: PaymentType
  ): Promise<Expense[]> => {
    const params: Record<string, any> = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    if (expenseType) params.expense_type = expenseType;
    return apiClient.get(ENDPOINTS.GET_EXPENSES, { params });
  },

  getExpenseSum: async (year?: number, month?: number): Promise<{ total: number }> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get(ENDPOINTS.GET_EXPENSE_SUM, { params });
  },

  createExpense: async (data: CreateExpenseDto): Promise<Expense> => {
    return apiClient.post(ENDPOINTS.CREATE_EXPENSE, data);
  },

  updateExpense: async (data: UpdateExpenseDto): Promise<Expense> => {
    return apiClient.put(ENDPOINTS.UPDATE_EXPENSE, data);
  },

  deleteExpense: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_EXPENSE}?ident=${id}`);
  },
};

export const infoService = {
  getInfo: async (studentId?: number): Promise<StudentInfo[]> => {
    const params = studentId ? { student_id: studentId } : {};
    return apiClient.get(ENDPOINTS.GET_INFO, { params });
  },

  createInfo: async (data: StudentInfo): Promise<StudentInfo> => {
    return apiClient.post(ENDPOINTS.CREATE_INFO, data);
  },

  updateInfo: async (id: number, data: StudentInfo): Promise<StudentInfo> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_INFO}?ident=${id}`, data);
  },

  deleteInfo: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_INFO}?ident=${id}`);
  },
};
