export interface User {
  id: number;
  full_name: string;
  email: string;
  phone_number: number;
  role?: string;
  image_url?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  role?: string;
  id?: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

// Courses
export interface Course {
  id: number;
  name: string;
  image_url?: string;
  created_at?: string;
}

// Groups
export interface Group {
  id: number;
  name: string;
  period: number;
  price: number;
  course_id: number;
  teacher_id: number;
  status?: boolean;
  course?: Course;
  teacher?: User;
}

export interface CreateGroupDto {
  name: string;
  period: number;
  price: number;
  course_id: number;
  teacher_id: number;
}

export interface UpdateGroupDto extends CreateGroupDto {}

// Students
export type StudentStatus = 'active' | 'graduated' | 'inactive';

export interface Student {
  id: number;
  full_name: string;
  group_id: number;
  discount: number;
  phone_number: number;
  started_date: string;
  status: StudentStatus;
  group?: Group;
}

export interface CreateStudentDto {
  full_name: string;
  group_id: number;
  discount: number;
  phone_number: number;
  started_date: string;
}

export interface UpdateStudentDto extends CreateStudentDto {}

export interface UpdateStatusDto {
  student_id: number;
  status: StudentStatus;
}

// Attendance
export interface Attendance {
  id: number;
  date: string;
  student_id: number;
  group_id: number;
  description: string;
  status: boolean;
  student?: Student;
}

export interface CreateAttendanceDto {
  date: string;
  student_id: number;
  group_id: number;
  description: string;
  status: boolean;
}

export interface UpdateAttendanceDto extends CreateAttendanceDto {}

// Payments
export type PaymentType = 'cash' | 'click';
export type Month = 
  | 'January' | 'February' | 'March' | 'April' | 'May' | 'June'
  | 'July' | 'August' | 'September' | 'October' | 'November' | 'December';

export interface Payment {
  id: number;
  student_id: number;
  group_id: number;
  amount: number;
  month: Month;
  payment_type: PaymentType;
  payment_date: string;
  discount: number;
  student?: Student;
}

export interface CreatePaymentDto {
  student_id: number;
  group_id: number;
  amount: number;
  month: Month;
  payment_type: PaymentType;
  payment_date?: string;
  discount?: number;
}

export interface UpdatePaymentDto {
  amount: number;
  payment_type: PaymentType;
}

// Reception
export interface Reception {
  id: number;
  full_name: string;
  visit_date: string;
  phone_number: string;
  secondary_phone: string;
  source: string;
  course: string;
  free_days: string[];
  free_times: string[];
  address: string;
  status: string;
  additional_info: string;
}

export interface CreateReceptionDto {
  full_name: string;
  visit_date: string;
  phone_number: string;
  secondary_phone: string;
  source: string;
  course: string;
  free_days: string[];
  free_times: string[];
  address: string;
  status: string;
  additional_info: string;
}

export interface UpdateReceptionDto extends CreateReceptionDto {
  id: number;
}

// Expenses
export interface Expense {
  ident: number;
  date: string;
  amount: number;
  description: string;
  category: string;
  payment_type: PaymentType;
}

export interface CreateExpenseDto {
  date: string;
  amount: number;
  description: string;
  category: string;
  payment_type: PaymentType;
}

export interface UpdateExpenseDto extends CreateExpenseDto {
  ident: number;
}

// Info (Parent info)
export interface StudentInfo {
  id?: number;
  student_id: number;
  parent_name: string;
  parent_phone: string;
  address: string;
}

// Users
export interface CreateUserDto {
  full_name: string;
  password: string;
  email: string;
  phone_number: number;
}

export interface UpdateUserDto extends CreateUserDto {}

// Statistics & Reports
export interface StudentCountStats {
  active_count: number;
  inactive_count: number;
  graduated_count: number;
}

export interface TeacherCountStats {
  count: number;
}

export interface CourseCountStats {
  count: number;
}

export interface GroupCountStats {
  count: number;
}

export interface ProfitReport {
  total_income: number;
  total_expense: number;
  profit: number;
}

export interface MonthlyStats {
  year: number;
  month: number;
  data: any[];
}

export interface AttendanceStats {
  total_days: number;
  attended_days: number;
  attendance_rate: number;
}
