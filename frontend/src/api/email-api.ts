
export class EmailApi  {
  private baseUrl: string;
  constructor() {
    this.baseUrl = import.meta.env.VITE_API_BASE_URL;
  }

  async getEmails(skip: number, limit: number) {
    const response = await fetch(`${this.baseUrl}/emails?skip=${skip}&limit=${limit}`);
    return response.json();
  }
}

export interface EmailResponse {
  submissions: {
  id: string;
  email_title: string;
  message: string;
  type: string;
  ai_classification: string;
  ai_suggested_reply: string;
  createdAt: string;
  }[];
  total: number;
}