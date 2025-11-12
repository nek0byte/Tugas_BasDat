import axios from "axios";

const defaultBaseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: defaultBaseURL,
  timeout: 10000
});

export async function fetchStudents({ search = "", limit = 100, skip = 0 } = {}) {
  const params = {
    limit,
    skip
  };
  if (search) {
    params.search = search;
  }
  const { data } = await api.get("/students", { params });
  return data;
}

export async function fetchStudentById(id) {
  const { data } = await api.get(`/students/${id}`);
  return data;
}

export async function syncStudents() {
  const { data } = await api.post("/sync");
  return data;
}

