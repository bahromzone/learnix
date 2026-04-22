export const API_BASE_URL = 'http://localhost:8000';

export const ENDPOINTS = {
  // Auth
  LOGIN: '/login/token',
  REFRESH_TOKEN: '/login/refresh_token',
  
  // Users
  GET_OWN_PROFILE: '/user/get_own',
  UPDATE_OWN_PROFILE: '/user/update_own',
  UPLOAD_USER_IMAGE: '/user/upload-image',
  DELETE_OWN: '/user/delete_own',
  
  // Administrators
  GET_ALL_USERS: '/admistrator/get_all',
  GET_ALL_TEACHERS: '/admistrator/get_all_teacher',
  GET_TEACHER_COUNT: '/admistrator/get_all_teacher_count',
  CREATE_TEACHER: '/admistrator/create_teacher',
  CREATE_ADMIN: '/admistrator/create_admin',
  CREATE_BOSS: '/admistrator/create_boss',
  UPDATE_USER: '/admistrator/update_user',
  DELETE_USER: '/admistrator/delete_user',
  DELETE_TEACHER: '/admistrator/delete_teacher',
  
  // Courses
  GET_COURSES: '/course/get',
  GET_COURSE_COUNT: '/course/get_count',
  CREATE_COURSE: '/course/create',
  UPLOAD_COURSE_IMAGE: '/course/upload-image',
  UPDATE_COURSE: '/course/update',
  DELETE_COURSE: '/course/delete',
  
  // Groups
  GET_GROUPS: '/group/get',
  GET_GROUP_COUNT: '/group/get_count',
  CREATE_GROUP: '/group/create',
  UPDATE_GROUP_STATUS: '/group/update_status',
  UPDATE_GROUP: '/group/update',
  DELETE_GROUP: '/group/delete',
  
  // Students
  GET_ALL_STUDENTS: '/student/get_all_students',
  GET_DEBT_STUDENTS: '/student/get_debt_student',
  GET_OWN_STUDENTS: '/student/get_own_students',
  GET_STUDENT_COUNT: '/student/get_count',
  CREATE_STUDENT: '/student/create',
  UPDATE_STATUS: '/student/update_status',
  UPDATE_STUDENT: '/student/update',
  DELETE_STUDENT: '/student/delete',
  
  // Attendance
  GET_ATTENDANCE_STATS: '/attendance/get_attendances_statistics',
  GET_ATTENDANCE_ADMINS: '/attendance/get_attendances_for_admins',
  GET_ATTENDANCE_TEACHERS: '/attendance/get_attendances_for_teachers',
  CREATE_ATTENDANCE: '/attendance/create',
  UPDATE_ATTENDANCE: '/attendance/update',
  DELETE_ATTENDANCE: '/attendance/delete',
  
  // Payments
  GET_PROFIT: '/payment/profit',
  GET_ALL_PAYMENTS: '/payment/all',
  GET_MONTHLY_SUM: '/payment/monthly_sum',
  GET_TEACHER_PAYMENTS: '/payment/for_teacher',
  CREATE_PAYMENT: '/payment/create',
  UPDATE_PAYMENT: '/payment/update',
  DELETE_PAYMENT: '/payment/delete',
  
  // Reception
  GET_RECEPTION: '/reception/get',
  GET_RECEPTION_STATS: '/reception/get_statistics',
  GET_MONTHLY_STATS: '/reception/get_monthly_statistics',
  GET_TOTAL_RECEPTION: '/reception/get_total_reception_students',
  CREATE_RECEPTION: '/reception/create',
  UPDATE_RECEPTION: '/reception/update',
  DELETE_RECEPTION: '/reception/delete',
  
  // Expenses
  GET_EXPENSES: '/expense/get',
  GET_EXPENSE_SUM: '/expense/get_sum_expense',
  CREATE_EXPENSE: '/expense/create',
  UPDATE_EXPENSE: '/expense/update',
  DELETE_EXPENSE: '/expense/delete',
  
  // Info
  GET_INFO: '/info/get',
  CREATE_INFO: '/info/create',
  UPDATE_INFO: '/info/update',
  DELETE_INFO: '/info/delete',
};
