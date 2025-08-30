import React, { useEffect, useState } from 'react';
import { Button, Flex, Table } from 'antd';
import type { TableColumnsType, TableProps } from 'antd';
import ModalComponent from '../modal/ModalComponent';
import { EmailApi } from '../../api/email-api';

type TableRowSelection<T extends object = object> = TableProps<T>['rowSelection'];

interface EmailType {
  id: number;
  email_title: string;
  message: string;
  type: string;
  ai_classification: string;
  ai_suggested_reply: string;
  created_at: string;
  key?: number;
}

const columns: TableColumnsType<EmailType> = [
  { title: 'Título', dataIndex: 'email_title', sorter: (a, b) => a.email_title.localeCompare(b.email_title) },
  { title: 'Mensagem', dataIndex: 'message', sorter: (a, b) => a.message.localeCompare(b.message) },
  { title: 'Tipo', dataIndex: 'type', sorter: (a, b) => a.type.localeCompare(b.type) },
  { title: 'Classificação', dataIndex: 'ai_classification', sorter: (a, b) => a.ai_classification.localeCompare(b.ai_classification) },
  { title: 'Resposta Sugerida', dataIndex: 'ai_suggested_reply', sorter: (a, b) => a.ai_suggested_reply.localeCompare(b.ai_suggested_reply) },
  { 
    title: 'Criado Em', 
    dataIndex: 'created_at',
    sorter: (a, b) => a.created_at.localeCompare(b.created_at),
    render: (text: string) => {
      if (!text) return '-';
      return new Date(text).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
];

const emailApi = new EmailApi();

const MainComponent: React.FC = () => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState<EmailType[]>([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
    total: 0,
    showSizeChanger: true,
    pageSizeOptions: ['5', '10', '20', '50', '100'], 
    showTotal: (total: number, range: number[]) => 
      `${range[0]}-${range[1]} de ${total} itens`,
  });

  const fetchData = async (page: number = 1, pageSize: number = 5) => {
    setLoading(true);
    try {
      const skip = (page - 1) * pageSize;
      const data = await emailApi.getEmails(skip, pageSize);
      
      const dataWithKeys = data.submissions.map((item: EmailType) => ({
        ...item,
        key: item.id
      }));
      
      setDataSource(dataWithKeys);
      setPagination(prev => ({
        ...prev,
        current: page,
        pageSize: pageSize,
        total: data.total
      }));
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTableChange = (page: number, pageSize: number) => {
    fetchData(page, pageSize);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const start = () => {
    setLoading(true);
    setTimeout(() => {
      setSelectedRowKeys([]);
      setLoading(false);
    }, 1000);
  };

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    console.log('selectedRowKeys changed: ', newSelectedRowKeys);
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const rowSelection: TableRowSelection<EmailType> = {
    selectedRowKeys,
    onChange: onSelectChange,
  };

  const hasSelected = selectedRowKeys.length > 0;

  return (
    <Flex gap="middle" vertical>
      <Flex align="center" gap="middle">
        {hasSelected ? (
          <Button type="primary" onClick={start} disabled={!hasSelected} loading={loading}>
            Delete
          </Button>
          ) : (
            <ModalComponent />
        )}
        {hasSelected ? `Selected ${selectedRowKeys.length} items` : null}
      </Flex>
      <Table<EmailType>  
        bordered 
        rowSelection={rowSelection} 
        columns={columns} 
        dataSource={dataSource} 
        loading={loading}
        pagination={{
          ...pagination,
          onChange: handleTableChange,
          onShowSizeChange: handleTableChange,
          locale: {
            items_per_page: '/ página',
            page: 'página'
          }
        }}
      />
    </Flex>
  );
};

export default MainComponent;