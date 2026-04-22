import apiClient from './client';
import { ENDPOINTS } from '../config/api';
import { 
  Course, 
  Group, 
  CreateGroupDto, 
  UpdateGroupDto,
  Student,
  CreateStudentDto,
  UpdateStudentDto,
  UpdateStatusDto,
  StudentCountStats,
  TeacherCountStats,
  CourseCountStats,
  GroupCountStats
} from '../types';

export const courseService = {
  getAllCourses: async (): Promise<Course[]> => {
    return apiClient.get<Course[]>(ENDPOINTS.GET_COURSES);
  },

  getCourseCount: async (): Promise<CourseCountStats> => {
    return apiClient.get(ENDPOINTS.GET_COURSE_COUNT);
  },

  createCourse: async (courseName: string): Promise<Course> => {
    return apiClient.post(ENDPOINTS.CREATE_COURSE, null, {
      params: { course_name: courseName },
    });
  },

  uploadCourseImage: async (id: number, file: File): Promise<{ message: string }> => {
    return apiClient.uploadFile(`${ENDPOINTS.UPLOAD_COURSE_IMAGE}?ident=${id}`, file);
  },

  updateCourse: async (id: number, newName: string): Promise<Course> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_COURSE}?ident=${id}`, null, {
      params: { new_name: newName },
    });
  },

  deleteCourse: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_COURSE}?ident=${id}`);
  },
};

export const groupService = {
  getAllGroups: async (courseId?: number): Promise<Group[]> => {
    const params = courseId ? { course_id: courseId } : {};
    return apiClient.get<Group[]>(ENDPOINTS.GET_GROUPS, { params });
  },

  getGroupCount: async (): Promise<GroupCountStats> => {
    return apiClient.get(ENDPOINTS.GET_GROUP_COUNT);
  },

  createGroup: async (data: CreateGroupDto): Promise<Group> => {
    return apiClient.post(ENDPOINTS.CREATE_GROUP, data);
  },

  updateGroupStatus: async (id: number): Promise<Group> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_GROUP_STATUS}?ident=${id}`);
  },

  updateGroup: async (id: number, data: UpdateGroupDto): Promise<Group> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_GROUP}?ident=${id}`, data);
  },

  deleteGroup: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_GROUP}?ident=${id}`);
  },
};

export const studentService = {
  getAllStudents: async (groupId?: number, status?: string): Promise<Student[]> => {
    const params: Record<string, any> = {};
    if (groupId) params.group_id = groupId;
    if (status) params.status = status;
    return apiClient.get<Student[]>(ENDPOINTS.GET_ALL_STUDENTS, { params });
  },

  getDebtStudents: async (year?: number, month?: string): Promise<Student[]> => {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    return apiClient.get<Student[]>(ENDPOINTS.GET_DEBT_STUDENTS, { params });
  },

  getOwnStudents: async (groupId?: number): Promise<Student[]> => {
    const params = groupId ? { group_id: groupId } : {};
    return apiClient.get<Student[]>(ENDPOINTS.GET_OWN_STUDENTS, { params });
  },

  getStudentCount: async (): Promise<StudentCountStats> => {
    return apiClient.get(ENDPOINTS.GET_STUDENT_COUNT);
  },

  createStudent: async (data: CreateStudentDto): Promise<Student> => {
    return apiClient.post(ENDPOINTS.CREATE_STUDENT, data);
  },

  updateStatus: async (data: UpdateStatusDto): Promise<Student> => {
    return apiClient.put(ENDPOINTS.UPDATE_STATUS, data);
  },

  updateStudent: async (id: number, data: UpdateStudentDto): Promise<Student> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_STUDENT}?ident=${id}`, data);
  },

  deleteStudent: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_STUDENT}?ident=${id}`);
  },
};

export const statsService = {
  getTeacherCount: async (): Promise<TeacherCountStats> => {
    return apiClient.get(ENDPOINTS.GET_TEACHER_COUNT);
  },

  getCourseCount: async (): Promise<CourseCountStats> => {
    return apiClient.get(ENDPOINTS.GET_COURSE_COUNT);
  },

  getGroupCount: async (): Promise<GroupCountStats> => {
    return apiClient.get(ENDPOINTS.GET_GROUP_COUNT);
  },

  getStudentCount: async (): Promise<StudentCountStats> => {
    return apiClient.get(ENDPOINTS.GET_STUDENT_COUNT);
  },
};
