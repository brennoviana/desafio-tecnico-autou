export class EmailApi  {
  private baseUrl: string;
  constructor() {
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
  }

  async getEmails(skip: number, limit: number) : Promise<EmailResponse> {
    const response = await fetch(`${this.baseUrl}/emails/?skip=${skip}&limit=${limit}`);
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

  async createEmailText(email_title: string, content: string): Promise<EmailSubmissionResponse> {
    const response = await fetch(`${this.baseUrl}/emails/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email_title, content })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async createEmailFile(email_title: string, file: File): Promise<EmailSubmissionResponse> {
    const formData = new FormData();
    formData.append('email_title', email_title);
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/emails/file`, {
      method: 'POST',
      body: formData // FormData não precisa de Content-Type header
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getEmailStats(): Promise<EmailStatsResponse> {
    const response = await fetch(`${this.baseUrl}/emails/stats`);
    
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

export interface EmailSubmissionResponse {
  id: number;
  email_title: string;
  message: string;
  type: string;
  ai_classification: string;
  ai_suggested_reply: string;
  created_at: string;
}

export interface DeleteEmailsResponse {
  deleted_count: number;
  deleted_ids: number[];
  not_found_ids?: number[];
}

export interface EmailStatsResponse {
  total: number;
  produtivos: number;
  improdutivos: number;
  nao_classificados: number;
  pdf: number;
  txt: number;
  texto_puro: number;
}