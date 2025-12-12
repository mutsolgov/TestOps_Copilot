import axios from 'axios';
import { GenerationRequest, TestCase } from '../types';

const API_URL = 'http://localhost:8000/api/v1';

export const api = {
    generateTestCase: async (request: GenerationRequest): Promise<TestCase> => {
        const response = await axios.post<TestCase>(`${API_URL}/generate`, request);
        return response.data;
    }
};
