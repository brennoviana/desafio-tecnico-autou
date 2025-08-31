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

  const emailApi = new EmailApi();

  const showModal = () => {
    setOpen(true);
    form.resetFields();
    setFileList([]);
    setSubmitType('text');
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
              { min: 2, message: 'Título deve ter pelo menos 2 caracteres!' },
              { max: 255, message: 'Título deve ter no máximo 255 caracteres!' }
            ]}
          >
            <Input placeholder="Digite o título do email..." />
          </Form.Item>

          {submitType === 'text' ? (
            <Form.Item
              name="content"
              label="Conteúdo do Email"
              rules={[
                { required: true, message: 'Conteúdo é obrigatório!' },
                { min: 10, message: 'Conteúdo deve ter pelo menos 10 caracteres!' },
                { max: 10000, message: 'Conteúdo deve ter no máximo 10.000 caracteres!' }
              ]}
            >
              <TextArea 
                rows={8}
                placeholder="Digite o conteúdo do email..."
                showCount
                maxLength={10000}
              />
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