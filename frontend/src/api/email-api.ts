export class EmailApi  {
  private baseUrl: string;
  constructor() {
    this.baseUrl = import.meta.env.VITE_API_BASE_URL;
  }

  async getEmails(skip: number, limit: number) : Promise<EmailResponse> {
    const response = await fetch(`${this.baseUrl}/emails?skip=${skip}&limit=${limit}`);
    return response.json();
  }

  async searchEmails(skip: number, limit: number, email_title: string) : Promise<EmailResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      email_title: email_title
    });
    const response = await fetch(`${this.baseUrl}/emails?${params}`);
    return response.json();
  }

  async deleteEmails(ids: number[]): Promise<DeleteEmailsResponse> {
    const response = await fetch(`${this.baseUrl}/emails`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ids })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export interface EmailResponse {
  submissions: {
  id: number;
  email_title: string;
  message: string;
  type: string | "Texto puro" | "TXT" | "PDF";
  ai_classification: string;
  ai_suggested_reply: string;
  created_at: string;
  }[];
  total: number;
}

export interface DeleteEmailsResponse {
  deleted_count: number;
  deleted_ids: number[];
  not_found_ids?: number[];
}