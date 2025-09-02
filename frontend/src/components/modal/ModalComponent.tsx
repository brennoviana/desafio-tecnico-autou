import React, { useState } from 'react';
import { Button, Modal, Form, Input, message, Upload, Space } from 'antd';
import { PlusOutlined, InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { EmailApi } from '../../api/email-api';

const { TextArea } = Input;
const { Dragger } = Upload;

interface EmailFormData {
  email_title: string;
  content: string;
}

interface ModalComponentProps {
  onEmailAdded?: () => void;
}

const ModalComponent: React.FC<ModalComponentProps> = ({ onEmailAdded }) => {
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [form] = Form.useForm<EmailFormData>();
  const [submitType, setSubmitType] = useState<'text' | 'file'>('text');
  const [fileList, setFileList] = useState<any[]>([]);
  const [charCount, setCharCount] = useState(0);

  const emailApi = new EmailApi();

  const countCharsWithoutSpaces = (text: string) => {
    return text.replace(/\s/g, '').length;
  };

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    setCharCount(countCharsWithoutSpaces(text));
  };

  const showModal = () => {
    setOpen(true);
    form.resetFields();
    setFileList([]);
    setSubmitType('text');
    setCharCount(0);
  };

  const handleOk = async () => {
    try {
      setConfirmLoading(true);
      
      if (submitType === 'text') {
        const values = await form.validateFields();
        
        await emailApi.createEmailText(values.email_title, values.content);

        message.success('Email processado com sucesso!');
        
      } else if (submitType === 'file') {
        const values = await form.validateFields(['email_title']);
        
        if (fileList.length === 0) {
          message.error('Selecione um arquivo');
          return;
        }

        const file = fileList[0];
        
        if (!file || !(file instanceof File)) {
          message.error('Arquivo inválido. Tente selecionar novamente.');
          return;
        }
        
        await emailApi.createEmailFile(values.email_title, file);

        message.success('Arquivo processado com sucesso!');
      }

      setOpen(false);
      form.resetFields();
      setFileList([]);
      
      if (onEmailAdded) {
        onEmailAdded();
      }
      
    } catch (error) {
      message.error('Erro ao processar email');
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setOpen(false);
    form.resetFields();
    setFileList([]);
  };

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    beforeUpload: (file) => {
      const isValidType = file.type === 'text/plain' || file.type === 'application/pdf';
      if (!isValidType) {
        message.error('Apenas arquivos .txt e .pdf são aceitos!');
        return false;
      }
      
      const isValidSize = file.size / 1024 / 1024 < 5;
      if (!isValidSize) {
        message.error('Arquivo deve ser menor que 5MB!');
        return false;
      }
      
      setFileList([file]);
      return false;
    },
    onRemove: () => {
      setFileList([]);
    },
  };

  return (
    <>
      <Button type="primary" icon={<PlusOutlined />} onClick={showModal}>
        Novo Email
      </Button>
      <Modal
        title="Processar Novo Email"
        open={open}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        width={600}
        okText="Processar"
        cancelText="Cancelar"
      >
        <Form
          form={form}
          layout="vertical"
          style={{ marginTop: 16 }}
        >
          <Form.Item
            label="Tipo de Submissão"
            style={{ marginBottom: 16 }}
          >
            <Space.Compact>
              <Button 
                type={submitType === 'text' ? 'primary' : 'default'}
                onClick={() => setSubmitType('text')}
              >
                Texto Direto
              </Button>
              <Button 
                type={submitType === 'file' ? 'primary' : 'default'}
                onClick={() => setSubmitType('file')}
              >
                Upload Arquivo
              </Button>
            </Space.Compact>
          </Form.Item>

          <Form.Item
            name="email_title"
            label="Título do Email"
            rules={[
              { required: true, message: 'Título é obrigatório!' },
              {
                validator: (_, value) => {
                  if (!value) return Promise.resolve();
                  const charCount = countCharsWithoutSpaces(value);
                  if (charCount < 2) {
                    return Promise.reject(new Error('Título deve ter pelo menos 2 caracteres (sem espaços)!'));
                  }
                  if (charCount > 255) {
                    return Promise.reject(new Error('Título deve ter no máximo 255 caracteres (sem espaços)!'));
                  }
                  return Promise.resolve();
                }
              }
            ]}
          >
            <Input 
              placeholder="Digite o título do email..." 
            />
          </Form.Item>

          {submitType === 'text' ? (
            <Form.Item
              name="content"
              label="Conteúdo do Email"
              rules={[
                { required: true, message: 'Conteúdo é obrigatório!' },
                {
                  validator: (_, value) => {
                    if (!value) return Promise.resolve();
                    const charCount = countCharsWithoutSpaces(value);
                    if (charCount < 10) {
                      return Promise.reject(new Error('Conteúdo deve ter pelo menos 10 caracteres (sem espaços)!'));
                    }
                    if (charCount > 10000) {
                      return Promise.reject(new Error('Conteúdo deve ter no máximo 10.000 caracteres (sem espaços)!'));
                    }
                    return Promise.resolve();
                  }
                }
              ]}
            >
              <div>
                <TextArea 
                  rows={8}
                  placeholder="Digite o conteúdo do email..."
                  maxLength={10000}
                  onChange={handleContentChange}
                />
                <div style={{ 
                  marginTop: 8, 
                  fontSize: '12px', 
                  color: '#8c8c8c',
                  textAlign: 'right' 
                }}>
                  {charCount} caracteres (sem espaços)
                </div>
              </div>
            </Form.Item>
          ) : (
            <Form.Item
              label="Arquivo do Email"
              rules={[
                { required: fileList.length === 0, message: 'Selecione um arquivo!' }
              ]}
            >
              <Dragger {...uploadProps}>
                <p className="ant-upload-drag-icon">
                  <InboxOutlined />
                </p>
                <p className="ant-upload-text">
                  Clique ou arraste o arquivo para esta área
                </p>
                <p className="ant-upload-hint">
                  Suporte para arquivos .txt e .pdf (máx. 5MB)
                </p>
              </Dragger>
            </Form.Item>
          )}
        </Form>
      </Modal>
    </>
  );
};

export default ModalComponent;